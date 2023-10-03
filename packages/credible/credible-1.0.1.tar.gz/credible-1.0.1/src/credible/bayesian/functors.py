# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Functors with standard credible region parameterisation."""

import typing

import numpy
import numpy.typing

from ..utils import CIArrayFunctor, CIFunctor
from . import utils


def make_functor(fun, lambda_=1.0, coverage=0.95) -> CIFunctor:
    """Creates a functor that can operate across the library, with scalar
    inputs."""

    def inner(s: int, f: int) -> tuple[float, float, float]:
        retval = fun(s, f, lambda_=lambda_, coverage=coverage)
        return retval[1:]

    return inner


def make_array_functor(fun, lambda_=1.0, coverage=0.95) -> CIArrayFunctor:
    """Creates a functor that can operate across the library, with array-like
    inputs."""

    def inner(
        s: typing.Iterable[int], f: typing.Iterable[int]
    ) -> tuple[
        numpy.typing.NDArray[numpy.double],
        numpy.typing.NDArray[numpy.double],
        numpy.typing.NDArray[numpy.double],
    ]:
        retval = fun(s, f, lambda_=lambda_, coverage=coverage)
        return retval[1:]

    return inner


bayesian_flat: CIFunctor = make_functor(utils.beta)
bayesian_flat_array: CIArrayFunctor = make_array_functor(utils._beta_array)
bayesian_jeffreys: CIFunctor = make_functor(utils.beta, lambda_=0.5)
bayesian_jeffreys_array: CIArrayFunctor = make_array_functor(
    utils._beta_array, lambda_=0.5
)
