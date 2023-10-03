# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Basic typing used throughout this package."""

import typing

import numpy.typing

CIFunctor: typing.TypeAlias = typing.Callable[
    [int, int], tuple[float, float, float]
]
"""A confidence-interval functor.

Exchangeable functors follow this prototype:

.. code:: python

   def f(successes: int, failures: int) -> tuple[float, float, float]:
       '''Returns best estimate, lower, and upper bounds of metric.'''
       pass

Functors allow evaluation of bayesian credible regions or confidence intervals
without coverage or :math:`\\lambda` parameterisation (implicit).  It works as
a partial function in which those parameters are predefined.
"""


CIArrayFunctor: typing.TypeAlias = typing.Callable[
    [typing.Iterable[int], typing.Iterable[int]],
    tuple[
        numpy.typing.NDArray[numpy.double],
        numpy.typing.NDArray[numpy.double],
        numpy.typing.NDArray[numpy.double],
    ],
]
"""A confidence-interval functor that works with arrays.

Functors allow evaluation of bayesian credible regions or confidence
intervals without coverage or :math:`\\lambda` parameterisation
(implicit).  It works as a partial function in which those parameters
are predefined.
"""


def as_int_arrays(
    input: typing.Sequence[int | typing.Iterable[int]],
) -> tuple[numpy.typing.NDArray[numpy.int_], ...]:
    """Converts integer sequences into arrays, and checks for matching lenghts.

    Uses :py:func:`numpy.asarray`, which only converts arguments if they are
    not already integer arrays.  We then use :py:func:`numpy.atleast_1d` to
    ensure all output arrays have at least 1 dimension.


    Parameters
    ----------
    input
        Integer sequences to be converted into numpy arrays of integers.


    Returns
    -------
        A tuple with input arrays converted.  All input arrays contain are at least
        one dimensional.


    Raises
    ------
    TypeError
        If the dimensions of the various arrays do not match.
    """

    retval = tuple(
        numpy.atleast_1d(numpy.asarray(k, dtype=numpy.int_)) for k in input
    )
    shapes = tuple(k.shape for k in retval)
    if len(set(shapes)) != 1:
        shape_str = ", ".join(
            [f"input[{i}].shape = {k}" for i, k in enumerate(shapes)]
        )
        raise TypeError(
            f"The number of dimensions on input arrays is different: {shape_str}"
        )
    return retval


def safe_divide(n: int | float, d: int | float) -> float:
    """Divides n by d.  Returns 0.0 in case of a division by zero.

    Parameters
    ----------
    n
        numerator
    d
        denominator


    Returns
    -------
        :math:`\\frac{n}{d}`` if :math:`d \\ne 0`, else 0.
    """

    return n / (d + (d == 0))
