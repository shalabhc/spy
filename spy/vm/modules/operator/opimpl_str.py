from typing import TYPE_CHECKING

from spy.errors import SPyError
from spy.vm.primitive import (
    W_I8,
    W_I32,
    W_I64,
    W_U8,
    W_U32,
    W_U64,
    W_Bool,
    W_Complex128,
)
from spy.vm.str import W_Str

from . import OP

if TYPE_CHECKING:
    from spy.vm.vm import SPyVM


@OP.builtin_func
def w_str_eq(vm: "SPyVM", w_a: W_Str, w_b: W_Str) -> W_Bool:
    assert isinstance(w_a, W_Str)
    assert isinstance(w_b, W_Str)
    res = vm.ll.call("spy_str_eq", w_a.ptr, w_b.ptr)
    return vm.wrap(bool(res))


@OP.builtin_func
def w_str_ne(vm: "SPyVM", w_a: W_Str, w_b: W_Str) -> W_Bool:
    assert isinstance(w_a, W_Str)
    assert isinstance(w_b, W_Str)
    res = vm.ll.call("spy_str_eq", w_a.ptr, w_b.ptr)
    return vm.wrap(bool(not res))


@OP.builtin_func
def w_str_find_byte(vm: "SPyVM", w_s: W_Str, w_ch: W_U8, w_start: W_I32) -> W_I32:
    # libc memchr-backed single-byte search (spy_str_find_byte in libspy/str.c)
    assert isinstance(w_s, W_Str)
    idx = vm.ll.call("spy_str_find_byte", w_s.ptr, vm.unwrap(w_ch), vm.unwrap(w_start))
    return vm.wrap(idx)


@OP.builtin_func
def w_str_find_sub(vm: "SPyVM", w_h: W_Str, w_needle: W_Str, w_start: W_I32) -> W_I32:
    # libc memmem-backed substring search (spy_str_find_sub in libspy/str.c)
    assert isinstance(w_h, W_Str)
    assert isinstance(w_needle, W_Str)
    idx = vm.ll.call("spy_str_find_sub", w_h.ptr, w_needle.ptr, vm.unwrap(w_start))
    return vm.wrap(idx)


def _parse_int(vm: "SPyVM", w_s: W_Str) -> int:
    s = vm.unwrap(w_s)
    try:
        return int(s)
    except ValueError:
        raise SPyError("W_ValueError", f"invalid literal for int() with base 10: {s!r}")


def _check_range(val: int, lo: int, hi: int, tname: str) -> None:
    if val < lo or val > hi:
        raise SPyError(
            "W_OverflowError", f"{tname} value {val} out of range [{lo}, {hi}]"
        )


@OP.builtin_func
def w_str_to_i32(vm: "SPyVM", w_s: W_Str) -> W_I32:
    val = _parse_int(vm, w_s)
    _check_range(val, -(2**31), 2**31 - 1, "i32")
    return W_I32(val)


@OP.builtin_func
def w_str_to_u32(vm: "SPyVM", w_s: W_Str) -> W_U32:
    val = _parse_int(vm, w_s)
    _check_range(val, 0, 2**32 - 1, "u32")
    return W_U32(val)


@OP.builtin_func
def w_str_to_i8(vm: "SPyVM", w_s: W_Str) -> W_I8:
    val = _parse_int(vm, w_s)
    _check_range(val, -128, 127, "i8")
    return W_I8(val)


@OP.builtin_func
def w_str_to_u8(vm: "SPyVM", w_s: W_Str) -> W_U8:
    val = _parse_int(vm, w_s)
    _check_range(val, 0, 255, "u8")
    return W_U8(val)


@OP.builtin_func
def w_str_to_i64(vm: "SPyVM", w_s: W_Str) -> W_I64:
    val = _parse_int(vm, w_s)
    _check_range(val, -(2**63), 2**63 - 1, "i64")
    return W_I64(val)


@OP.builtin_func
def w_str_to_u64(vm: "SPyVM", w_s: W_Str) -> W_U64:
    val = _parse_int(vm, w_s)
    _check_range(val, 0, 2**64 - 1, "u64")
    return W_U64(val)


@OP.builtin_func
def w_str_to_complex128(vm: "SPyVM", w_x: W_Str) -> W_Complex128:
    res = vm.ll.call("spy_str_to_complex128", w_x.ptr)
    return W_Complex128(complex(*res))
