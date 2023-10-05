# Copyright (c) 2023 NEC Corporation. All Rights Reserved.

from logging import getLogger
from typing import List
import dis
import inspect
import itertools
import struct
import sys

import firefw as fire
from firefw import tracing

logger = getLogger(__name__)


def _is_intractive():
    import __main__ as main

    return not hasattr(main, "__file__")


def prohibit_reentrant(func):
    lock = False

    def wrapper(*args, **kwargs):
        nonlocal lock
        assert not lock
        lock = True
        try:
            ret = func(*args, **kwargs)
        finally:
            lock = False
        return ret

    return wrapper


# TODO: Accept multiple values to be evaluated. Those values should be return
# values of the MLIR function created.
#
# Since this function is not well designed on reentrant, we prohibit it.
@prohibit_reentrant
def evaluate(values: List[fire.Value], executor, package=None):
    """evaluates values.

    Args:
        values(List[fire.Value]): values to be evaluated
        executor: function to execute IR

    Returns:
        any: Evaluated result
    """

    for v in values:
        logger.debug("fire.evaluate: %s is_bound=%s", v, v.is_bound())

    if all([v.is_available() for v in values]):
        return [v.get_result() for v in values]

    if len(values) == 0:  # empty
        return []

    if any([v.is_available() for v in values]):
        raise RuntimeError("Some of values are already evaluated")

    with tracing.scope(tracing.Level.VERBOSE, "create_mlir_func"):
        source, input_values, output_values = create_mlir_func(
            values, package=package
        )

    ret = executor(source, input_values, output_values)

    if len(output_values) != len(ret):
        raise RuntimeError("Executor did not return enough number of returns")

    for output_value, obj in zip(output_values, ret):
        output_value.emplace(obj)

    return [v.get_result() for v in values]


# def print_refcounts(outs):
#     for value in outs:
#         if value.get_bound_obj() is None:
#             continue
#         # logger.debug('%s type=%s', value, type(value.get_bound_obj()))
#         # gc.collect()
#         logger.debug('%s#%x(#%x) refcount(obj)=%d %d refcount(value)=%d %d',
#                      value, id(value), id(value.get_bound_obj()),
#                      sys.getrefcount(value.get_bound_obj()),
#                      len(gc.get_referrers(value.get_bound_obj())),
#                      sys.getrefcount(value), len(gc.get_referrers(value)))
#         # logger.debug('Value.__dict__=%x', id(value.__dict__))
#
#         referrers = gc.get_referrers(value.get_bound_obj())
#         pretty = pprint.PrettyPrinter()
#         for r in referrers:
#             logger.debug('%s %x', type(r), id(r))
#             logger.debug(pretty.pformat(r))


def get_refcounts(outs):
    # for v in outs:
    #     logger.debug("%s: is_bound=%s", v, v.is_bound())
    # -1 because sys.getrefcount returns +1 for its argument
    return {
        v: sys.getrefcount(v.get_bound_obj()) - 1 if v.is_bound() else 0
        for v in outs
    }


def find_module_name(outs):
    """
    Returns module name where outs are belong to or None.

    All values in outs should be belong to the same module. If module name can
    not to be resolved, i.e. no value is bound to user-side object, returns
    None.
    """
    for v in outs:
        if v.is_bound():
            # TODO: obj.__class__.__module__?
            return v.get_bound_obj().__module__
    return None


def frame_generator(frame):
    """A generator of frame objects for the given frame and all outer
    frames.

    Unlike inspect.getouterframes() which returns FrameInfo objects,
    this generator returns frame objects.

    """

    while frame is not None:
        yield frame
        frame = frame.f_back


def get_frames(skip=0):
    """Get an iterator of frame objects.

    By default, this function returns an iterator of frame objects
    without a frame of this function itself. If `skip` is a positive
    integer, the first `skip` frames are skipped. If `skip` is
    negative, this function may behave unexpectedly.

    """

    f = inspect.currentframe()
    try:
        if f is None:  # pragma: no cover
            # if inspect.currentframe() is unavailable
            stack = inspect.stack()
            del stack[:1]
            frames = iter(info.frame for info in stack)
        else:
            frames = frame_generator(f.f_back)
    finally:
        del f

    # consume frames
    next(itertools.islice(frames, skip, skip), None)
    return frames


# TODO: Review with complex module tree. And consider to recieve user_frame
# from user.
def find_user_frame(outs, package):
    module_name = find_module_name(outs)

    logger.debug("find_user_frame: module_name=%s", module_name)
    if module_name:
        # Skip frames inside this file from find_user_frame() to evaluate()
        frames = list(get_frames(4))

        # Find the outermost frame which belongs to `module_name`
        last_index = -1
        for i, frame in enumerate(frames[:-1]):
            # logger.debug(frame)
            # logger.debug(inspect.getmodule(frame).__name__)
            module = inspect.getmodule(frame)

            if module is None:
                # When running on a debugger or ipython, outermost module could
                # be None. In this case, what we are looking for should be
                # already found.
                if last_index != -1:
                    break

                # we can not find user frame because inspect might return None
                # for the module for which pyarmor is used
                return None

            if package is not None:
                if module.__name__.startswith(package):
                    last_index = i
            elif module.__name__ == module_name:
                # logger.debug('Found module')
                last_index = i

        # one more outer frame is the user frame where evaluate is called.
        user_frame = frames[last_index + 1]
        # logger.debug('last_index=%d', last_index)
        logger.debug("find_user_frame: user_frame=%s", user_frame)
        return user_frame
    return None


def filter_outputs_by_frame(user_frame, refcounts):
    """Filter the output value which are bound only to local variables and
    those are never refered after the evaluation.

    Args:
        user_frame: stack frame where evaluation is started
        refcounts: dictionaly of value and its refcount
    """

    logger.debug("filter_outputs_by_frame")

    # for n, v in user_frame.f_locals.items():
    #     logger.debug('user_frame: %s #%x', n, id(v))

    f_locals = user_frame.f_locals
    outputs = []
    value_local_names = {}

    for value, refcount in refcounts.items():
        assert value.is_bound()
        obj = value.get_bound_obj()
        assert refcount > 1

        referrers = set()
        for name, var in f_locals.items():
            if var is obj:  # if local_name refers obj
                referrers.add(name)

        assert len(referrers) < refcount

        # 1 is from value. Check if all other refs are from locals.
        if len(referrers) == refcount - 1:
            logger.debug(
                "output %s#%x(#%x) is bound only to local vars: %s.",
                value,
                id(value),
                id(obj),
                referrers,
            )
            value_local_names[value] = referrers
        else:
            logger.debug(
                "output %s#%x(#%x) is refered from non-locals"
                " (output for safety)",
                value,
                id(value),
                id(obj),
            )
            outputs += [value]

    logger.debug("lineno=%d lasti=%d", user_frame.f_lineno, user_frame.f_lasti)

    later_uses = None  # None means later uses are not detected
    if not _is_intractive():
        # get uses after evaluation
        later_uses = set()
        has_jabs = False
        bytecode = dis.Bytecode(user_frame.f_code)

        insts_accessing_locals = [
            dis.opmap["LOAD_NAME"],
            dis.opmap["LOAD_FAST"],
        ]

        # for inst in bytecode:
        #     logger.debug(inst)

        # TODO: Learn bytecode and check more carefully.
        for inst in bytecode:
            if inst.offset >= user_frame.f_lasti:
                if inst.opcode in dis.hasjabs:
                    has_jabs = True
                    break
                if inst.opcode in insts_accessing_locals:
                    later_uses.add(inst.argval)

        logger.debug("later_uses: %s", list(set(later_uses)))

        if has_jabs:
            # jabs might be backedge. For safety, all values go into outputs.
            later_uses = None

    if later_uses is None:
        outputs += value_local_names.keys()
    else:
        for value, names in value_local_names.items():
            # if value is refered after evaluation, it should be an output.
            if later_uses.intersection(names):
                outputs += [value]

    logger.debug(
        "filter_outputs_by_frame: outputs: %s",
        ", ".join([str(v) for v in outputs]),
    )

    return outputs


def pickup_outputs(outs, package) -> List[fire.Value]:
    """Pickup values that should be results of the function.

    Args:
        value: The value which a caller want to evaluate.
        outs: output values of ops to be executed.

    Returns:
        [Value]: function results.

    This method first picks values which are bound to user-side objects. Then
    checks if the values are refered after evaluation.

    If an output value is never refered after evaluation, we do not have to
    return a result of such value. It improves opportunity of optimizatons.
    This function finds such value and removes those from output values.
    """

    # Running gc might minimize refcounts, but it is costly, we do not run.
    # gc.collect()

    refcounts = get_refcounts(outs)
    logger.debug(
        "pickup_outputs: refcounts: %s%s",
        ", ".join([f"{k}:{refcounts[k]}" for k in list(refcounts)[:100]]),
        "..." if len(refcounts) > 100 else "",
    )

    # If count == 1, an object bound to a value is refered only from a value.
    # That means this object is never refered afterward.
    refcounts = {val: cnt for val, cnt in refcounts.items() if cnt > 1}
    # logger.debug('%s', type(outs))
    # logger.debug('%s', type(refcounts))
    # logger.debug('pickup_outputs: len(outs)=%d -> len(outputs)=%d',
    #              len(outs), len(refcounts))

    logger.debug("pickup_outputs: len(refcounts)=%s", len(refcounts))
    # If outputs has only one value, it should be a function result.
    # we avoid costly filter using stack frames.
    if len(refcounts) > 1:
        frame = find_user_frame(outs, package)
        # frame = None
        if frame is not None:
            outputs = filter_outputs_by_frame(frame, refcounts)
        else:
            logger.debug("pickup_outputs: frame not found")
            outputs = refcounts.keys()
    else:
        outputs = refcounts.keys()

    return list(outputs)


def get_ops(op, ops, opsset, indent=""):
    """Retuns ops which are required to evaluate op recursively"""
    # logger.debug('get_ops: %s%s', indent, op)

    for op0 in op.deps:
        # logger.debug('get_ops: %sdepends on: %s', indent, str(op0))
        if op0 not in opsset:
            evaluated = [v.is_available() for v in op0.outs]
            # all true or all false
            # assert all(evaluated) or not any(evaluated)
            if not any(evaluated):
                get_ops(op0, ops, opsset, indent + "  ")

    # logger.debug('get_ops: %s>> append %s', indent, op.opcode)
    ops.append(op)
    opsset.add(op)

    return ops


def create_constant(typ, value, name):
    if typ == "i1":
        i = 1 if value else 0
        return f"{name} = tfrt.constant.i1 {i}"
    if typ == "i32":
        return f"{name} = tfrt.constant.i32 {value}"
    if typ == "i64":
        return f"{name} = tfrt.constant.i64 {value}"
    if typ == "f32":
        hex_value = hex(struct.unpack(">L", struct.pack(">f", value))[0])
        return f"{name} = tfrt.constant.f32 {hex_value} // {value}"
    if typ == "f64":
        hex_value = hex(struct.unpack(">Q", struct.pack(">d", value))[0])
        return f"{name} = tfrt.constant.f64 {hex_value} // {value}"
    if typ == "!tfrt.string":
        # converting to raw-string for handling escapes correctly
        if "\\" in value:
            escaped = repr(value.replace('"', '\\"'))[1:-1]
        else:
            escaped = value.replace('"', '\\"')
        return (
            f'{name} = "fire.get_string"() {{ value = "{escaped}" }}'
            f" : () -> !tfrt.string"
        )
    return f"// UNHANDLED CONSTANT: {name} : {type(value)}"


def is_embeddable_constant(value: fire.Value):
    embeddables = ["f32", "f64", "i1", "i32", "i64", "!tfrt.string"]
    return value.mlir_type in embeddables


def convert_to_mlir_op(op: fire.core.Operation, unique_ins):
    # logger.debug('create_mlir_op: %s', op)
    ins = []
    attrs = []
    for v in op.ins:
        if v.is_attr():
            attrs += [v]
        elif v.is_available():
            key = id(v.get_result())
            assert key in unique_ins
            ins += [unique_ins[key].name()]
        else:
            ins += [v.name()]
    ins = ", ".join(ins)

    in_types = ", ".join([v.mlir_type for v in op.ins if not v.is_attr()])
    lhs = ""
    out_types = ""
    if op.outs:
        outs = ", ".join([v.name() for v in op.outs])
        out_types = "-> (" + ", ".join(v.mlir_type for v in op.outs) + ")"
        lhs = f"{outs} = "

    if attrs:
        cont = [
            f"{v.name()} = {v.get_result()} : {v.type().mlir_type}"
            for v in attrs
        ]
        attrs = " { " + ", ".join(cont) + " }"
    else:
        attrs = ""

    return f'{lhs}"{op.opcode}"({ins}){attrs} :({in_types}) {out_types}'


def create_mlir_ops(values, package):
    """
    Args:
        values:         values to be evaluated.

    Returns:
        mlir_ops:      ops in function body as array of  string in mlir format.
        input_values:  values given as function arguments.
        output_values: values retured as function results.
    """
    assert len(values) > 0
    root_ops = [v.get_def() for v in values]

    logger.debug("create_mlir_ops: start to collect ops to be evaluated")
    ops = []
    opsset = set()
    for op in root_ops:
        if op not in ops:
            ops = get_ops(op, ops, opsset)
    logger.debug("create_mlir_ops: finish to collect ops to be evaluated")

    # Since ops going to be evaluated are not needed to evaluated again,
    # those are removed from a builder.
    # We use builder of first value because all ops have the same builder.
    builder = values[0].get_def().builder
    builder.remove_ops(opsset)

    ins = [v for op in ops for v in op.ins]
    outs = [v for op in ops for v in op.outs]

    # Different input values might have the same result.  We instanciates one
    # value for each result. unique_ins collects values having the same result.
    unique_ins = {}
    for v in [v for v in ins if v.is_available() and not v.is_attr()]:
        key = id(v.get_result())
        if key not in unique_ins:
            unique_ins[key] = v

    logger.debug(
        "create_mlir_ops: outs: (%s) %s%s",
        len(outs),
        [str(v) for v in outs[:100]],
        "" if len(outs) < 100 else "...",
    )

    # Decide output_values
    output_values = pickup_outputs(outs, package)

    logger.debug(
        "create_mlir_ops: output_values: (%s) %s%s",
        len(output_values),
        [str(v) for v in output_values[:100]],
        "" if len(output_values) < 100 else "...",
    )

    # pickup_outputs does not pickup values which are not bound to user
    # objects (value.is_bound()=False). But `value` is requested to be
    # evaluated by a user of this method, it is added to output_values.
    for v in values:
        if v not in output_values:
            output_values += [v]

    # Add values which are inputs of remaining ops in irbuilder, which are
    # created but not required to evaluate `values`. Such ops might be evaluate
    # afterward, the values have to be returned.
    # Ex:
    #   v0 = op0(...)
    #   v1 = op1(v0, ...)
    #   v2 = op2(v0, ...)
    # When evaluating v2, `v1 = op1(v0, ...)` is not evlauated because v2 dose
    # not depend on v1. v0 have to be returned because it might be used when
    # op1 is evaluated.
    for op in builder.get_ops():
        tmp = [v for v in outs if v in op.ins and v not in output_values]
        output_values += tmp

    # Add all outputs of ops which output values in output_vallues.
    for ov in output_values:
        op = ov.get_def()
        tmp = [v for v in op.outs if v not in output_values]
        output_values += tmp

    # Embed inputs to IR or add to input_values
    input_values = []
    load_const_ops = []
    for v in unique_ins.values():
        if is_embeddable_constant(v):
            load_const_ops.append(
                create_constant(v.mlir_type, v.get_result(), v.name())
            )
        else:
            input_values.append(v)

    mlir_ops = load_const_ops
    for op in ops:
        mlir_ops.append(convert_to_mlir_op(op, unique_ins))

    logger.debug(
        "create_mlir_ops: input_values: (%d) %s%s",
        len(input_values),
        [str(v) for v in input_values[:100]],
        "..." if len(input_values) > 100 else "",
    )
    logger.debug(
        "create_mlir_ops: output_values: (%d) %s%s",
        len(output_values),
        [str(v) for v in output_values[:100]],
        "..." if len(output_values) > 100 else "",
    )

    return mlir_ops, input_values, output_values


# TODO: Move to irbuilder.py?
def create_mlir_func(values, *, fname="main", package=None):
    logger.debug("create_mlir_func")

    mlir_ops, input_values, output_values = create_mlir_ops(values, package)

    # Create Function

    formal_args = ", ".join(
        [f"{v.name()}: {v.mlir_type}" for v in input_values]
    )
    return_values = ", ".join([f"{v.name()}" for v in output_values])
    return_types = ", ".join([f"{v.mlir_type}" for v in output_values])

    # vim python-mode dose not like `{{`, we use `+ '{'`.
    lines = []
    lines.append(
        f"  func.func @{fname}({formal_args}) -> ({return_types})" + " {"
    )
    lines += ("    " + line for line in mlir_ops)
    lines.append(f"    tfrt.return {return_values} : {return_types}")
    lines.append("  }")

    return "\n".join(lines), input_values, output_values
