# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Frequentist confidence interval estimation.

(Frequentist) confidence interval interpretation, with 95% coverage: **If we
are to take several independent random samples from the population and
construct confidence intervals from each of the sample data, then 95 out of 100
confidence intervals will contain the true mean (true proportion, in this
context of proportion)**.

See a discussion in `Five Confidence Intervals for Proportions That You
Should Know About <ci-evaluation_>`_.

.. include:: ../links.rst
"""

import typing

import numpy
import numpy.typing
import scipy.stats

from ..utils import as_int_arrays


def _clopper_pearson_ndarray(
    successes: numpy.typing.NDArray[numpy.integer],
    failures: numpy.typing.NDArray[numpy.integer],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`clopper_pearson`, for multiple systems."""
    right = (1.0 - coverage) / 2  # half-width in each side
    lower = scipy.stats.beta.ppf(right, successes, failures + 1)
    upper = scipy.stats.beta.ppf(1 - right, successes + 1, failures)
    lower = numpy.nan_to_num(lower, nan=0.0)
    upper = numpy.nan_to_num(upper, nan=1.0)
    return successes / (successes + failures), lower, upper


def _clopper_pearson_array(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`clopper_pearson`, for multiple systems."""
    successes_array, failures_array = as_int_arrays((successes, failures))
    return _clopper_pearson_ndarray(successes_array, failures_array, coverage)


def clopper_pearson(
    successes: int, failures: int, coverage: float = 0.95
) -> tuple[float, float, float]:
    """Calculates the "exact" confidence interval for proportion estimates.

    The Clopper-Pearson interval method is used for estimating the confidence
    intervals.  This implementation is based on [CLOPPER-1934]_.  This
    technique is **very** conservative - in most of the cases, coverage is
    greater than the required value, which may imply in too large confidence
    intervals.


    Parameters
    ----------
    successes
        Number of successes observed on the experiment.
    failures
        Number of failures observed on the experiment.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% coverage.


    Returns
    -------
        The estimated ratio between successes, and total trials (successes plus
        failures), lower and upper bounds of the confidence interval, in this
        order.


    Raises
    ------
    TypeError
        If the dimensions of ``successes`` and ``failures`` do not match, or in
        case the input types are unsupported.
    """
    retval = _clopper_pearson_array([successes], [failures], coverage)
    return (retval[0].item(), retval[1].item(), retval[2].item())


def _agresti_coull_ndarray(
    successes: numpy.typing.NDArray[numpy.integer],
    failures: numpy.typing.NDArray[numpy.integer],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`agresti_coull`, for multiple systems."""
    right = (1.0 - coverage) / 2  # half-width in each side
    crit = scipy.stats.norm.isf(right)
    kl_c = (successes + failures) + crit**2
    q_c = (successes + crit**2 / 2.0) / kl_c
    std_c = numpy.sqrt(q_c * (1.0 - q_c) / kl_c)
    dist = crit * std_c
    lower = q_c - dist
    upper = q_c + dist

    lower = numpy.nan_to_num(lower, nan=0.0)
    upper = numpy.nan_to_num(upper, nan=1.0)

    return successes / (successes + failures), lower, upper


def _agresti_coull_array(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`agresti_coull`, for multiple systems."""
    successes_array, failures_array = as_int_arrays((successes, failures))
    return _agresti_coull_ndarray(successes_array, failures_array, coverage)


def agresti_coull(
    successes: int, failures: int, coverage: float = 0.95
) -> tuple[float, float, float]:
    """Calculates the confidence interval for proportion estimates.

    The Agresti-Coull interval method is used for estimating the confidence
    intervals.  This implementation is based on [AGRESTI-1998]_.  This
    technique is conservative - in most of the cases, coverage is greater
    than the required value, which may imply a larger confidence interval that
    required.

    This function is considered a good choice for the frequentist approach, if
    you cannot use :py:func:`clopper_pearson`.


    Parameters
    ----------
    successes
        Number of successes observed on the experiment.
    failures
        Number of failures observed on the experiment.
    coverage
        A floating-point number between 0 and 1.0 indicating the
        coverage you're expecting.  A value of 0.95 will ensure 95% coverage.


    Returns
    -------
        The estimated ratio between successes, and total trials (successes plus
        failures), lower and upper bounds of the confidence interval, in this
        order.


    Raises
    ------
    TypeError
        If the dimensions of ``successes`` and ``failures`` do not match, or in
        case the input types are unsupported.
    """
    retval = _agresti_coull_array([successes], [failures], coverage)
    return (retval[0].item(), retval[1].item(), retval[2].item())


def _wilson_ndarray(
    successes: numpy.typing.NDArray[numpy.integer],
    failures: numpy.typing.NDArray[numpy.integer],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`wilson`, for multiple systems."""
    right = (1.0 - coverage) / 2  # half-width in each side
    n = successes + failures
    p = successes / n
    crit = scipy.stats.norm.isf(right)
    crit2 = crit**2
    denom = 1 + (crit2 / n)
    center = (p + crit2 / (2 * n)) / denom
    dist = crit * numpy.sqrt(p * (1.0 - p) / n + crit2 / (4.0 * n**2))
    dist = dist / denom
    lower = center - dist
    upper = center + dist

    lower = numpy.nan_to_num(lower, nan=0.0)
    upper = numpy.nan_to_num(upper, nan=1.0)

    return successes / (successes + failures), lower, upper


def _wilson_array(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`wilson`, for multiple systems."""
    successes_array, failures_array = as_int_arrays((successes, failures))
    return _wilson_ndarray(successes_array, failures_array, coverage)


def wilson(
    successes: int, failures: int, coverage: float = 0.95
) -> tuple[float, float, float]:
    """Calculates the confidence interval for proportion estimates.

    The Wilson interval method is used for estimating the confidence intervals.
    This implementation is based on [WILSON-1927]_.  This implementation does
    **not** contain the continuity correction.  It is as conservative in the
    extremes of the domain as the bayesian approach and can be a good default,
    if :py:func:`clopper_pearson` cannot be used.

    This function is considered the best "default" for the frequentist
    approach as it is not too conservative and assumes a resonable value
    through out the range.


    Parameters
    ----------
    successes
        Number of successes observed on the experiment.
    failures
        Number of failures observed on the experiment.
    coverage
        A floating-point number between 0 and 1.0 indicating the
        coverage you're expecting.  A value of 0.95 will ensure 95% coverage.


    Returns
    -------
        The estimated ratio between successes, and total trials (successes plus
        failures), lower and upper bounds of the confidence interval, in this
        order.


    Raises
    ------
    TypeError
        If the dimensions of ``successes`` and ``failures`` do not match, or in
        case the input types are unsupported.
    """
    retval = _wilson_array([successes], [failures], coverage)
    return (retval[0].item(), retval[1].item(), retval[2].item())
