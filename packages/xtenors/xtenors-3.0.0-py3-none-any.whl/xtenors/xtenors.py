

from __future__ import annotations

import abc
import typing

import operator
import itertools
import functools
import datetime
import calendar

import xtuples as xt

from .dates import *
from .units import *

# TODO: rename iteration as iterators for consistency

from . import conventions
from . import iterators
from . import calendars
from . import arithmetic
from . import adjustments

# ---------------------------------------------------------------


@cython.cfunc
@cython.returns(tuple[
    cython.int, cython.int, cython.int, cython.int
])
@cython.locals(
    s = cython.p_char,
    unit = cython.char,
    v = cython.int,
)
def parse_C(s):
    unit = s[-1]
    v = int(s[:-1])
    if unit == 'Y':
    # if unit == 89:
        return (v, 0, 0, 0)
    elif unit == 'M':
    # elif unit == 77:
        return (0, v, 0, 0)
    elif unit == 'D':
    # elif unit == 68:
        return (0, 0, 0, v)
    elif unit == 'W':
    # elif unit == 87:
        return (0, 0, v, 0)
    else:
        assert False, (unit, v)

@xt.nTuple.decorate()
class Tenor(typing.NamedTuple):

    s: str

    # deliberately no __add__
    # as what about iterator / overflow - forces one to be explicit
    
    Y: typing.Optional[int] = None
    M: typing.Optional[int] = None
    W: typing.Optional[int] = None
    D: typing.Optional[int] = None

    overflow: typing.Optional[conventions.Overflow] = None

    # h / m / s / ms / ... ?

    # adjust

    @classmethod
    def parse_py(cls, s: str, overflow = None) -> Tenor:
        unit = s[-1]
        v = int(s[:-1])
        if unit == 'Y':
            return Tenor(s, v, 0, 0, 0, overflow=overflow)
        elif unit == 'M':
            return Tenor(s, 0, v, 0, 0, overflow=overflow)
        elif unit == 'D':
            return Tenor(s, 0, 0, 0, v, overflow=overflow)
        elif unit == 'W':
            return Tenor(s, 0, 0, v, 0, overflow=overflow)
        else:
            assert False, (unit, v)

    @classmethod
    def parse_C(cls, s: str, overflow = None) -> Tenor:
        """
        >>> Tenor.parse("1D")
        Tenor(s='1D', Y=0, M=0, W=0, D=1, overflow=None)
        >>> Tenor.parse("1W")
        Tenor(s='1W', Y=0, M=0, W=1, D=0, overflow=None)
        >>> Tenor.parse("1M")
        Tenor(s='1M', Y=0, M=1, W=0, D=0, overflow=None)
        >>> Tenor.parse("1Y")
        Tenor(s='1Y', Y=1, M=0, W=0, D=0, overflow=None)
        """
        return Tenor(s, *parse_C(s), overflow = overflow)

    parse = parse_py

    def init(self):
        if (
            self.Y is None
            or self.M is None
            or self.W is None
            or self.D is None
        ):
            return self.parse_py(self.s, overflow=self.overflow)
        return self

    def add(
        self: Tenor,
        ddt: typing.Union[DDT, Tenor],
        iterator: typing.Optional[iterators. Iterator] = None,
        adjust: bool = False,
        overflow=None,
    ):
        """
        >>> Tenor("1D").add(datetime.date(2021, 1, 1))
        datetime.date(2021, 1, 2)
        """
        return add(
            ddt,
            self,
            iterator=iterator,
            adjust=adjust,
            overflow=(
                overflow if overflow is None else self.overflow
            )
        )

# ---------------------------------------------------------------

def add(
    left: typing.Union[DDT, Tenor],
    right: Tenor,
    iterator: typing.Optional[iterators. Iterator] = None,
    adjust: bool = False,
    overflow=None,
):
    if (
        isinstance(left, Tenor)
        and isinstance(right, Tenor)
    ):
        left = left.init()
        right = right.init()
        return Tenor(
            Y=left.Y+right.Y,
            M=left.M+right.M,
            W=left.W+right.W,
            D=left.D+right.D,
            overflow=(
                overflow if overflow is not None else left.overflow
            )
            #
        )
    elif (
        isinstance(left, (datetime.datetime, datetime.date))
        and isinstance(right, Tenor)
    ):
        ddt = left
        tenor = right.init()
    elif  (
        isinstance(right, (datetime.datetime, datetime.date))
        and isinstance(left, Tenor)
    ):
        ddt = right
        tenor = left.init()
    else:
        assert False, dict(left=left, right=right)
    res = arithmetic.add(
        ddt,
        years=tenor.Y,
        months=tenor.M,
        weeks=tenor.W,
        days=tenor.D,
        iterator=iterator,
        overflow=(
            overflow if overflow is not None else tenor.overflow
        )
    )
    return res if not adjust else adjustments.adjust(
        res, overflow=overflow
    )

# ---------------------------------------------------------------
