from __future__ import annotations

import reprlib

from typing import Any

from mknodes.utils import log


logger = log.get_logger(__name__)


class LengthLimitRepr(reprlib.Repr):
    def repr_type(self, obj, level):
        return obj.__name__

    def repr_module(self, obj, level):
        return obj.__name__

    def repr_function(self, obj, level):
        return obj.__name__


limit_repr = LengthLimitRepr()
limit_repr.maxlist = 10
limit_repr.maxstring = 80


def get_repr(
    _obj: Any,
    *args: Any,
    _shorten: bool = True,
    _filter_empty: bool = False,
    _filter_false: bool = False,
    **kwargs: Any,
) -> str:
    """Get a suitable __repr__ string for an object.

    Args:
        _obj: The object to get a repr for.
        _shorten: Whether to shorten the repr.
        *args: Arguments for the repr
        **kwargs: Keyword arguments for the repr
    """
    my_repr = limit_repr.repr if _shorten else repr
    classname = type(_obj).__name__
    parts = [my_repr(val) for val in args]
    kw_parts = []
    for k, v in kwargs.items():
        if _filter_empty and (v is None or v == "" or v == {}):
            continue
        if _filter_false and v is False:
            continue

        import mknodes

        match v:
            case (mknodes.MkNode(), *_):
                name = "[...]"
            case _:
                name = my_repr(v)
        kw_parts.append(f"{k}={name}")
    sig = ", ".join(parts + kw_parts)
    return f"{classname}({sig})"


def dataclass_repr(instance):
    """Return repr for dataclass, filtered by non-default values."""
    import dataclasses

    from operator import attrgetter

    nodef_f_vals = (
        (f.name, attrgetter(f.name)(instance))
        for f in dataclasses.fields(instance)
        if attrgetter(f.name)(instance) != f.default
    )

    nodef_f_repr = ", ".join(f"{name}={value!r}" for name, value in nodef_f_vals)
    return f"{instance.__class__.__name__}({nodef_f_repr})"


if __name__ == "__main__":
    strings = get_repr([str(i) for i in range(1000)])
    print(limit_repr.repr(strings))
