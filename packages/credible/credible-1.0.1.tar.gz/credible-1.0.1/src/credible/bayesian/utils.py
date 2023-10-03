# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Functions to evalute the (Bayesian) credible region of measures.

(Bayesian) credible region interpretation, with 95% coverage: The probability
that the true proportion will lie within the 95% credible interval is 0.95.

Contrary to frequentist approaches, in which one can only say that if the test
were repeated an infinite number of times, and one constructed a confidence
interval each time, then X% of the confidence intervals would contain the true
rate, here we can say that given our observed data, there is a X% probability
that the true value of :math:`k/n` falls within the provided interval.

See a discussion in `Five Confidence Intervals for Proportions That You
Should Know About <ci-evaluation_>`_ for a study on coverage for most common
methods.

.. note::

   For a disambiguation with `Confidence Interval <confidence-interval_>`_ (the
   frequentist approach), read `Credible Regions or Intervals
   <credible-interval_>`_.

.. include:: ../links.rst
"""

import typing

import numpy
import numpy.random
import numpy.typing
import scipy.special

from ..utils import as_int_arrays


def _beta_ndarray(
    successes: numpy.typing.NDArray[numpy.integer],
    failures: numpy.typing.NDArray[numpy.integer],
    lambda_: float,
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`beta`, for multiple systems."""

    # we return the equally-tailed range
    right = (1.0 - coverage) / 2  # half-width in each side
    lower = scipy.special.betaincinv(
        successes + lambda_, failures + lambda_, right
    )
    upper = scipy.special.betaincinv(
        successes + lambda_, failures + lambda_, 1.0 - right
    )

    # evaluate mean and mode (https://en.wikipedia.org/wiki/Beta_distribution)
    alpha = successes + lambda_
    beta = failures + lambda_

    mean = numpy.nan_to_num(alpha / (alpha + beta))

    # the mode of a beta distribution is a bit tricky
    mode = numpy.zeros_like(lower)
    cond = (alpha > 1) & (beta > 1)
    mode[cond] = (alpha[cond] - 1) / (alpha[cond] + beta[cond] - 2)
    # In the case of precision, if the threshold is close to 1.0, both TP
    # and FP can be zero, which may cause this condition to be reached, if
    # the prior is exactly 1 (flat prior).  This is a weird situation,
    # because effectively we are trying to compute the posterior when the
    # total number of experiments is zero.  So, only the prior counts - but
    # the prior is flat, so we should just pick a value.  We choose the
    # middle of the range.
    # conda = alpha == 1 and beta == 1
    # mode[cond] = 0.0
    # conda = alpha <= 1 and beta > 1
    # mode[cond] = 0.0
    mode[(alpha > 1) & (beta <= 1)] = 1.0
    # else: #elif alpha < 1 and beta < 1:
    # in the case of precision, if the threshold is close to 1.0, both TP
    # and FP can be zero, which may cause this condition to be reached, if
    # the prior is smaller than 1.  This is a weird situation, because
    # effectively we are trying to compute the posterior when the total
    # number of experiments is zero.  So, only the prior counts - but the
    # prior is bimodal, so we should just pick a value.  We choose the
    # left of the range.
    # n.b.: could also be 1.0 as the prior is bimodal
    # mode[alpha < 1 and beta < 1] = 0.0

    return mean, mode, lower, upper


def _beta_array(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    lambda_: float,
    coverage: float,
) -> tuple[
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
    numpy.typing.NDArray[numpy.double],
]:
    """:py:func:`beta`, for multiple systems."""
    successes_array, failures_array = as_int_arrays((successes, failures))
    return _beta_ndarray(successes_array, failures_array, lambda_, coverage)


def beta(
    successes: int, failures: int, lambda_: float, coverage: float
) -> tuple[float, float, float, float]:
    r"""Returns the mode, upper and lower bounds of the equal-tailed credible
    region of a probability estimate following Bernoulli trials.

    This technique is (not) very conservative - in most of the cases, coverage
    closer to the extremes (0 or 1) is lower than expected (but still greater
    than 85%).

    This implementation is based on [GOUTTE-2005]_.  It assumes :math:`k`
    successes and :math:`l` failures (:math:`n = k+l` total trials) are issued
    from a series of Bernoulli trials (likelihood is binomial).  The posterior
    is derivated using the Bayes Theorem with a beta prior.  As there is no
    reason to favour high vs.  low precision, we use a symmetric Beta prior
    (:math:`\alpha=\beta`):

    .. math::

       P(p|k,n) &= \frac{P(k,n|p)P(p)}{P(k,n)} \\
       P(p|k,n) &= \frac{\frac{n!}{k!(n-k)!}p^{k}(1-p)^{n-k}P(p)}{P(k)} \\
       P(p|k,n) &= \frac{1}{B(k+\alpha, n-k+\beta)}p^{k+\alpha-1}(1-p)^{n-k+\beta-1} \\
       P(p|k,n) &= \frac{1}{B(k+\alpha, n-k+\alpha)}p^{k+\alpha-1}(1-p)^{n-k+\alpha-1}

    The mode for this posterior (also the maximum a posteriori) is:

    .. math::

       \text{mode}(p) = \frac{k+\lambda-1}{n+2\lambda-2}

    Concretely, the prior may be flat (all rates are equally likely,
    :math:`\lambda=1`) or we may use Jeoffrey's prior (:math:`\lambda=0.5`),
    that is invariant through re-parameterisation.  Jeffrey's prior indicate
    that rates close to zero or one are more likely.

    The mode above works if :math:`k+{\alpha},n-k+{\alpha} > 1`, which is
    usually the case for a resonably well tunned system, with more than a few
    samples for analysis.  In the limit of the system performance, :math:`k`
    may be 0, which will make the mode become zero.

    For our purposes, it may be more suitable to represent :math:`n = k + l`,
    with :math:`k`, the number of successes and :math:`l`, the number of
    failures in the binomial experiment, and find this more suitable
    representation:

    .. math::

       P(p|k,l) &= \frac{1}{B(k+\alpha, l+\alpha)}p^{k+\alpha-1}(1-p)^{l+\alpha-1} \\
       \text{mode}(p) &= \frac{k+\lambda-1}{k+l+2\lambda-2}

    This can be mapped to most rates calculated in the context of binary
    classification this way:

    * Precision or Positive-Predictive Value (PPV): p = TP/(TP+FP), so k=TP, l=FP
    * Recall, Sensitivity, or True Positive Rate: r = TP/(TP+FN), so k=TP, l=FN
    * Specificity or True Negative Rage: s = TN/(TN+FP), so k=TN, l=FP
    * Accuracy: acc = TP+TN/(TP+TN+FP+FN), so k=TP+TN, l=FP+FN
    * Jaccard: j = TP/(TP+FP+FN), so k=TP, l=FP+FN

    .. note:: **Important**

       To calculate the limits given the required coverage, we use the
       incomplete **inverse** (regularized, or normalized) beta function,
       :any:`scipy.special.betaincinv` instead of :any:`scipy.special.betainc`.
       The latter requires we provide the bounds and returns the coverage,
       whereas here we are interested in the *inverse* behaviour.


    Parameters
    ----------
    successes
        Number of successes (``k``) observed on the experiment.
    failures
        Number of failures (``l``) observed on the experiment.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  If unsure, use 0.5.
    coverage
        A floating-point number between 0 and 1.0 indicating the
        coverage you're expecting.  A value of 0.95 will ensure 95%
        of the area under the probability density of the posterior
        is covered by the returned equal-tailed interval.


    Returns
    -------
        A tuple containing 4 floating point numbers representing:

        * mean: The mean of the posterior distribution
        * mode: The mode of the posterior distribution
        * lower: The lower bounds of the credible region
        * upper: The upper bounds of the credible region

        If the input was a 1-D array with multiple experiments, then the return
        value of this function is also composed of 1-D arrays, representing the
        mean, mode, lower and upper bounds of the various credible regions
        defined for each of the success/failure tuples on the input.


    Raises
    ------
    TypeError
        If the dimensions of ``successes`` and ``failures`` do not match, or in
        case the input types are unsupported.
    """
    retval = _beta_array([successes], [failures], lambda_, coverage)
    return (
        retval[0].item(),
        retval[1].item(),
        retval[2].item(),
        retval[3].item(),
    )


def beta_posterior(
    successes: int, failures: int, lambda_: float, nb_samples: int
) -> numpy.typing.NDArray[numpy.double]:
    r"""Simulates the beta posterior of a system with the provided markings.

    This implementation is based on [GOUTTE-2005]_, Equation 7.

    Figures of merit that are supported by this procedure are those which have
    the form :math:`v = k / (k + l)` (successes over successes plus failures):

    * Precision or Positive-Predictive Value (PPV): :math:`p = TP/(TP+FP)`, so
      :math:`k=TP`, :math:`l=FP`
    * Recall, Sensitivity, or True Positive Rate: :math:`r = TP/(TP+FN)`, so
      :math:`k=TP`, :math:`l=FN`
    * Specificity or True Negative Rage: :math:`s = TN/(TN+FP)`, so :math:`k=TN`,
      :math:`l=FP`
    * Accuracy: :math:`acc = TP+TN/(TP+TN+FP+FN)`, so :math:`k=TP+TN`,
      :math:`l=FP+FN`
    * Jaccard Index: :math:`j = TP/(TP+FP+FN)`, so :math:`k=TP`, :math:`l=FP+FN`

    Parameters
    ----------
    successes
        Number of successes (``k``) observed on the experiment.  May be a
        scalar of any integral type, or an array of integral values indicating
        a series of experiments to calculate the credible regions for.
    failures
        Number of failures (``l``) observed on the experiment.  May be a scalar
        of any integral type, or an array of integral values indicating a
        series of experiments to calculate the credible regions for.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    nb_samples
        number of generated gamma distribution values


    Returns
    -------
        Variates: An array with size ``nb_samples`` containing a realization of
        Equation 7 from [GOUTTE-2005]_.  If ``successes`` and ``failures`` are
        sequences of arrays, then returns a 2D array where each row represents
        one set of realisations.


    Raises
    ------
    TypeError
        If the dimensions of ``successes`` and ``failures`` do not match.
    """
    return numpy.random.beta(
        a=successes + lambda_, b=failures + lambda_, size=nb_samples
    )


def average_beta_posterior(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    lambda_: float,
    nb_samples: int,
) -> numpy.typing.NDArray[numpy.double]:
    r"""Simulates the average beta posterior of many systems.

    This implementation is based on [GOUTTE-2005]_, Equation 7.

    Figures of merit that are supported by this procedure are those which have
    the form :math:`v = k / (k + l)` (successes over successes plus failures):

    * Precision or Positive-Predictive Value (PPV): :math:`p = TP/(TP+FP)`, so
      :math:`k=TP`, :math:`l=FP`
    * Recall, Sensitivity, or True Positive Rate: :math:`r = TP/(TP+FN)`, so
      :math:`k=TP`, :math:`l=FN`
    * Specificity or True Negative Rate: :math:`s = TN/(TN+FP)`, so :math:`k=TN`,
      :math:`l=FP`
    * Accuracy: :math:`acc = TP+TN/(TP+TN+FP+FN)`, so :math:`k=TP+TN`,
      :math:`l=FP+FN`
    * Jaccard Index: :math:`j = TP/(TP+FP+FN)`, so :math:`k=TP`, :math:`l=FP+FN`


    Parameters
    ----------
    successes
        Sequence of integers expressing the number of successes (``k``)
        observed on the various experiments whose metric is to be averaged.
    failures
        Sequence of integers expressing the number of failures (``l``)
        observed on the various experiments whose metric is to be averaged.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    nb_samples
        number of generated gamma distribution values


    Returns
    -------
        Variates: An array with size ``nb_samples`` containing a realization of
        Equation 7 from [GOUTTE-2005]_, considering the averaging of all input
        systems.
    """
    successes_array, failures_array = as_int_arrays((successes, failures))

    if successes_array.ndim == 0:
        successes_array = numpy.atleast_1d(successes_array)
        failures_array = numpy.atleast_1d(failures_array)

    return numpy.mean(
        [
            beta_posterior(kk, ll, lambda_, nb_samples)
            for kk, ll in zip(successes_array, failures_array)
        ],
        axis=0,
    )


def evaluate_statistics(
    variates: typing.Iterable[float],
    coverage: float,
    bins: int | str,
) -> tuple[float, float, float, float]:
    """Evaluates the left and right margins for a given M-C distribution.

    Parameters
    ----------
    variates
        A 1-D array containing the simulated variates
    coverage
        A number, between 0 and 1 to indicate the desired coverage.  Typically,
        this number is set to 0.95 (95% coverage).
    bins
        Histogram binning for defining the mode of the original distribution
        where variates where sampled from.  A larger number of bins will make
        it unlikely to discover the true mode.  You may also pass any of the
        string method names defined at :py:func:`numpy.histogram_bin_edges`.  A
        method such as ``doane`` should work fine in most cases.


    Returns
    -------
        statistics: mean, (a rough estimated of the) mode and lower and upper
        bounds of the credible intervals for the input simulation.

        .. note::

           Mode estimation depends on the number of input ``variates``, and
           histogram binning (``bins``).  Using :py:func:`scipy.stats.mode` can
           only evaluate most common value, which is **not reliable** for
           continuous variables.
    """

    left_half = (1 - coverage) / 2  # size of excluded (half) area
    variates_array = numpy.asarray(variates, dtype=numpy.double)
    sorted_variates = numpy.sort(variates_array)

    # n.b.: we return the equally tailed range

    # calculates position of score which would exclude the left_half (left)
    lower_index = int(round(len(variates_array) * left_half))

    # calculates position of score which would exclude the right_half (right)
    upper_index = int(round(len(variates_array) * (1 - left_half)))

    lower = sorted_variates[lower_index - 1]
    upper = sorted_variates[upper_index - 1]

    # we evaluate the histogram and get the maximum value from there
    hist, ranges = numpy.histogram(variates_array, bins=bins)
    idx = numpy.argmax(hist)
    mode = (ranges[idx] + ranges[idx + 1]) / 2

    return (
        numpy.mean(variates_array).item(),
        mode,
        lower,
        upper,
    )


def average_beta(
    successes: typing.Iterable[int],
    failures: typing.Iterable[int],
    lambda_: float,
    coverage: float,
    nb_samples: int,
) -> tuple[float, float, float, float]:
    r"""The mean, mode, upper and lower bounds of the credible region of an
    average of measures with beta posteriors.

    This implementation is based on [GOUTTE-2005]_.


    Parameters
    ----------
    successes
        Sequence of integers expressing the number of successes (``k``)
        observed on the various experiments whose metric is to be averaged.
    failures
        Sequence of integers expressing the number of failures (``l``)
        observed on the various experiments whose metric is to be averaged.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        statistics: mean, mode, lower and upper bounds of the credible interval
        for the provided coverage.
    """

    variates = average_beta_posterior(successes, failures, lambda_, nb_samples)
    return evaluate_statistics(variates, coverage, "auto")


def compare_beta_posteriors(
    k1: int, l1: int, k2: int, l2: int, lambda_: float, nb_samples: int
) -> float:
    r"""Returns the probability that system 1 is better than system 2 for a
    given figure of merit.

    This implementation is based on [GOUTTE-2005]_.

    Figures of merit that are supported by this procedure are those which have
    the form :math:`v = k / (k + l)`:

    * Precision or Positive-Predictive Value (PPV): :math:`p = TP/(TP+FP)`, so
      :math:`k=TP`, :math:`l=FP`
    * Recall, Sensitivity, or True Positive Rate: :math:`r = TP/(TP+FN)`, so
      :math:`k=TP`, :math:`l=FN`
    * Specificity or True Negative Rage: :math:`s = TN/(TN+FP)`, so :math:`k=TN`,
      :math:`l=FP`
    * Accuracy: :math:`acc = TP+TN/(TP+TN+FP+FN)`, so :math:`k=TP+TN`,
      :math:`l=FP+FN`
    * Jaccard Index: :math:`j = TP/(TP+FP+FN)`, so :math:`k=TP`, :math:`l=FP+FN`


    Parameters
    ----------
    k1
        Number of successes for the first system.  See various definitions
        above.
    l1
        Number of failures for the first system.  See various definitions
        above.
    k2
        Number of successes for the second system.  See various definitions
        above.  Must be syntatically equal to ``k1``.
    l2
        Number of failures for the second system.  See various definitions
        above.  Must be syntatically equal to ``l1``.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  If unsure, use 0.5.
    nb_samples
        number of generated beta distribution values


    Returns
    -------
        A number between 0.0 and 1.0 that describes the probability that the
        first system has a bigger measurement than the second.
    """

    v1 = beta_posterior(k1, l1, lambda_, nb_samples)
    v2 = beta_posterior(k2, l2, lambda_, nb_samples)
    return numpy.count_nonzero(v1 > v2) / nb_samples


def f1_posterior(
    tp: int, fp: int, fn: int, lambda_: float, nb_samples: int
) -> numpy.typing.NDArray[numpy.double]:
    r"""Simulates the F1-score posterior of a system with the provided markings.

    This implementation is based on [GOUTTE-2005]_, Equation 11.

    Parameters
    ----------
    tp
        True positive count, AKA "hit", as an integer scalar.
    fp
        False positive count, AKA "false alarm", or "Type I error".
    fn
        False Negative count, AKA "miss", or "Type II error", as a scalar
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  If unsure, use 0.5.
    nb_samples
        number of generated gamma distribution values.


    Returns
    -------
        variates: An array with size ``nb_samples`` containing a realization of
        Equation 11 of [GOUTTE-2005]_.
    """
    u = numpy.random.gamma(shape=(tp + lambda_), scale=2.0, size=nb_samples)
    v = numpy.random.gamma(
        shape=(fp + fn + (2 * lambda_)),
        scale=1.0,
        size=nb_samples,
    )
    return u / (u + v)


def average_f1_posterior(
    tp: typing.Iterable[int],
    fp: typing.Iterable[int],
    fn: typing.Iterable[int],
    lambda_: float,
    nb_samples: int,
) -> numpy.typing.NDArray[numpy.double]:
    r"""Simulates the F1-score posterior of an average system with the provided
    markings.

    This implementation is based on [GOUTTE-2005]_, Equation 11.

    Parameters
    ----------
    tp
        Arrays containing true positive counts, AKA "hit", for all systems to
        be considered on the average
    fp
        Arrays containing false positive counts, AKA "false alarm", or "Type I
        error" for all systems to be considered on the average
    fn
        Arrays containing false Negative counts, AKA "miss", or "Type II
        error" for all systems to be considered on the average
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  If unsure, use 0.5.
    nb_samples
        number of generated gamma distribution values


    Returns
    -------
        variates: An array with size ``nb_samples`` containing a realization of
        Equation 11 from [GOUTTE-2005]_.
    """
    tp_array, fp_array, fn_array = as_int_arrays((tp, fp, fn))
    return numpy.mean(
        [
            numpy.asarray(
                f1_posterior(tp_, fp_, fn_, lambda_, nb_samples),
                dtype=numpy.double,
            )
            for tp_, fp_, fn_ in zip(tp_array, fp_array, fn_array)
        ],
        axis=0,
    )


def compare_f1_scores(
    tp1: int,
    fp1: int,
    fn1: int,
    tp2: int,
    fp2: int,
    fn2: int,
    lambda_: float,
    nb_samples: int,
) -> float:
    r"""Returns the probability that the F1-score from 1 system is bigger than
    the F1-score of a second system.

    This implementation is based on [GOUTTE-2005]_.


    Parameters
    ----------
    tp1
        True positive count, AKA "hit" for the first system.
    fp1
        False positive count, AKA "false alarm", or "Type I error" for the
        first system.
    fn1
        False Negative count, AKA "miss", or "Type II error", for the first
        system.
    tp2
        True positive count, AKA "hit" for the second system.
    fp2
        False positive count, AKA "false alarm", or "Type I error" for the
        second system.
    fn2
        False Negative count, AKA "miss", or "Type II error", for the second
        system.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    nb_samples
        number of generated gamma distribution values


    Returns
    -------

        prob: A number between 0.0 and 1.0 that describes the probability that
        the first system has a bigger F1-score than the second.
    """

    f1 = f1_posterior(tp1, fp1, fn1, lambda_, nb_samples)
    f2 = f1_posterior(tp2, fp2, fn2, lambda_, nb_samples)
    return numpy.count_nonzero(f1 > f2) / nb_samples


def compare_systems(
    n: typing.Sequence[int], lambda_: typing.Sequence[float], nb_samples: int
) -> float:
    r"""Compares 2 system (binary) outputs using a Dirichlet posterior.

    This function returns the empyrical probability that a system (1) is better
    another system (2), based on their binary outputs.  The comparison is
    carried-out as described in [GOUTTE-2005]_, equations 16 and 19, via a
    Monte-Carlo simulation, since the integral of the probability cannot be
    resolved analytically.

    To do so, we compute the probability that :math:`P(\pi_1 > \pi_2)`, i.e.,
    the probability that system 1 gives the expected output while system 2 does
    not, is greater than the probability that system 1 is incorrect while
    system 2 gives the correct answer.  It assumes, therefore, systems 1 and 2
    are tuned (thresholded), and provide binary outputs that can be compared to
    generate 3 numbers:

    * :math:`n_1`: The measured number of times system 1 provides the correct
      answer, whereas system 2 does not
    * :math:`n_2`: The measured number of times system 2 provides the correct
      answer, whereas system 1 does not
    * :math:`n_3`: The measured number of times system 1 and 2 agree, giving
      the same answer (wrong or write, it does not matter)

    Notice that :math:`\pi_1 = \frac{n_1}{n_1 + n_2 + n_3}`, and so,
    analogously, you may calculate :math:`\pi_2` and :math:`\pi_3`.

    We then plug these numbers to simulate a Dirichlet (generalisation of the
    Beta distribution for multiple variables) by setting:

    * :math:`\alpha_1 = n_1 + \lambda_1`
    * :math:`\alpha_2 = n_2 + \lambda_2`
    * :math:`\alpha_3 = n_2 + \lambda_3`

    Where each :math:`\lambda_i` correspond to the prior to be imputed to that
    particular variable.  We typically select :math:`\lambda_1 = \lambda_2`,

    Parameters
    ----------
    n
        A triple with 3 integers representing :math:`n_1`, :math:`n_2` and
        :math:`n_3`.
    lambda_
        A tuple with length 3, containing floating point numbers describing the
        parameterisation of the Dirichlet priors to consider.  Use
        :math:`\lambda_i=0.5` for Jeffrey's prior.
    nb_samples
        number of generated dirichlet distribution values (make this high, for
        a higher precision on the simulation).


    Returns
    -------
        probability: A number between 0.0 and 1.0 that describes the
        probability that the first system is better than the second one.
    """
    assert len(n) == 3
    assert len(lambda_) == 3
    samples = numpy.random.dirichlet(
        numpy.array(n) + numpy.array(lambda_), size=nb_samples
    )
    return numpy.count_nonzero(samples[:, 0] > samples[:, 1]) / nb_samples
