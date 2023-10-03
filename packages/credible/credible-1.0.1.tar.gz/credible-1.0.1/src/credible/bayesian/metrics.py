# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Implementation of :py:mod:`Scikit-Learn compatible measures
<sklearn.metrics>` with bayesian credible regions."""

import typing

import numpy
import numpy.typing
import sklearn.metrics

from .. import curves
from ..utils import safe_divide
from . import functors, utils

NUMBER_MC_SAMPLES = 100000
"""Suggested number of samples to use for Monte Carlo simulations in this
package."""


def precision_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float, float]:
    r"""Precision **binary** classification score.

    AKA positive predictive value (PPV), mean, mode and credible intervals.  It
    corresponds arithmetically to ``tp/(tp+fp)``.  This function only supports
    **binary** classification problems.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  Changes in this value do not significantly affect the
        outcome, unless ``tp`` or ``fp`` are very small (close to 1).
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual precision, as would be returned by scikit-learn
        * The mode of the posterior distribution: It is typically close to
          the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    _, fp, _, tp = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    _, mode, lower, upper = utils.beta(tp, fp, lambda_, coverage)
    return safe_divide(tp, tp + fp), mode, lower, upper


def recall_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float, float]:
    r"""Recall **binary** classification score.

    AKA sensitivity, hit rate, or true positive rate (TPR), mean, mode and
    credible intervals.  It corresponds arithmetically to ``tp/(tp+fn)``.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  Changes in this value do not significantly affect the
        outcome, unless ``tp`` or ``fp`` are very small (close to 1).
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual recall, as would be returned by scikit-learn
        * The mode of the posterior distribution: this represents the best
          estimate of the recall *a posteriori*.  It is typically close to
          the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    _, _, fn, tp = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    _, mode, lower, upper = utils.beta(tp, fn, lambda_, coverage)
    return safe_divide(tp, tp + fn), mode, lower, upper


def specificity_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float, float]:
    r"""Specificity **binary** classification score.

    AKA selectivity or true negative rate (TNR), mean, mode and credible
    intervals.  It corresponds arithmetically to ``tn/(tn+fp)``.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  Changes in this value do not significantly affect the
        outcome, unless ``tp`` or ``fp`` are very small (close to 1).
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual specificity, as would be returned by scikit-learn
        * The mode of the posterior distribution: this represents the best
          estimate of the specificity *a posteriori*.  It is typically close to
          the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    tn, fp, _, _ = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    _, mode, lower, upper = utils.beta(tn, fp, lambda_, coverage)
    return safe_divide(tn, tn + fp), mode, lower, upper


def accuracy_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float, float]:
    r"""Accuracy **binary** classification score.

    See `Accuracy
    <https://en.wikipedia.org/wiki/Evaluation_of_binary_classifiers>`_. is the
    proportion of correct predictions (both true positives and true negatives)
    among the total number of pixels examined.  It corresponds arithmetically
    to ``(tp+tn)/(tp+tn+fp+fn)``.  This measure includes both true-negatives
    and positives in the numerator, what makes it sensitive to data or regions
    without annotations. AKA selectivity or true negative rate (TNR), mean,
    mode and credible intervals.  It corresponds arithmetically to
    ``tn/(tn+fp)``.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  Changes in this value do not significantly affect the
        outcome, unless ``tp`` or ``fp`` are very small (close to 1).
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual accuracy, as would be returned by scikit-learn
        * The mode of the posterior distribution: this represents the best
          estimate of the accuracy *a posteriori*.  It is typically close to
          the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    tn, fp, fn, tp = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    _, mode, lower, upper = utils.beta(tn + tp, fp + fn, lambda_, coverage)
    return safe_divide(tn + tp, tn + tp + fp + fn), mode, lower, upper


def jaccard_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float, float]:
    r"""Jaccard **binary** classification score.

    See `Jaccard Index or Similarity
    <https://en.wikipedia.org/wiki/Jaccard_index>`_.  It corresponds
    arithmetically to ``tp/(tp+fp+fn)``.  The Jaccard index depends on a
    TP-only numerator, similarly to the F1 score.  For regions where there are
    no annotations, the Jaccard index will always be zero, irrespective of the
    model output.  Accuracy may be a better proxy if one needs to consider the
    true abscence of annotations in a region as part of the measure.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.  Changes in this value do not significantly affect the
        outcome, unless ``tp`` or ``fp`` are very small (close to 1).
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you're expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual jaccard score, as would be returned by scikit-learn
        * The mode of the posterior distribution: this represents the best
          estimate of the jaccard score *a posteriori*.  It is typically close
          to the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    _, fp, fn, tp = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    _, mode, lower, upper = utils.beta(tp, fp + fn, lambda_, coverage)
    return safe_divide(tp, tp + fp + fn), mode, lower, upper


def f1_score(
    y_true: typing.Iterable[int],
    y_pred: typing.Iterable[int],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
) -> tuple[float, float, float, float]:
    r"""Returns the mean, mode, upper and lower bounds of the credible region of
    the F1 score.

    See `F1-score <https://en.wikipedia.org/wiki/F1_score>`_.  It corresponds
    arithmetically to ``2*P*R/(P+R)`` or ``2*tp/(2*tp+fp+fn)``.  The F1 or Dice
    score depends on a TP-only numerator, similarly to the Jaccard index.  For
    regions where there are no annotations, the F1-score will always be zero,
    irrespective of the model output. Accuracy may be a better proxy if one
    needs to consider the true abscence of annotations in a region as part of
    the measure.

    This implementation is based on [GOUTTE-2005]_.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_pred
        Predicted labels, as returned by a classifier.
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.
    nb_samples
        number of generated gamma distribution values


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The actual F1 score, as would be returned by scikit-learn
        * The mode of the posterior distribution: this represents the best
          estimate of the F1 score *a posteriori*.  It is typically close
          to the value estimated by scikit-learn.
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """

    _, fp, fn, tp = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    # builds a Monte Carlo simulation of the F1 posterior distribution
    variates = utils.f1_posterior(tp, fp, fn, lambda_, nb_samples)
    # evaluates mean, mode, lower and upper bounds for the confidence interval
    # of interest.
    _, mode, lower, upper = utils.evaluate_statistics(
        variates, coverage, "auto"
    )

    # from matplotlib import pyplot as plt
    # plt.hist(variates, bins="auto", alpha=0.3, label="Variates")
    # plt.axvline(_, color="red", label="mean")
    # plt.axvline(mode, color="blue", label="mode")
    # plt.axvline(
    #     safe_divide(2 * tp, (2 * tp) + fp + fn), color="green", label="est."
    # )
    # plt.legend(loc="best")
    # plt.title("F1-Score variates (i.i.d. samples)")
    # plt.show()

    return safe_divide(2 * tp, (2 * tp) + fp + fn), mode, lower, upper


def roc_curve(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[
    numpy.typing.NDArray[numpy.double],  # fpr
    numpy.typing.NDArray[numpy.double],  # tpr
    numpy.typing.NDArray[numpy.double],  # thresholds
    numpy.typing.NDArray[numpy.double],  # fpr lower ci
    numpy.typing.NDArray[numpy.double],  # tpr lower ci
    numpy.typing.NDArray[numpy.double],  # fpr upper ci
    numpy.typing.NDArray[numpy.double],  # tpr upper ci
]:
    r"""Compute Receiver operating characteristic (ROC).

    Approximately follows API of :py:func:`sklearn.metrics.roc_curve`.

    .. important::

       The returned credible regions are not immediately usable for plots or
       the evaluation of the area under the curve, only as point estimates for
       individual thresholds.  To plot, feed the output of this funtion to
       :py:func:`.curves.curve_ci_hull` and use the lower and upper estimates
       provided by that function instead.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        Seven 1-D floating point arrays corresponding to:

        * FPR (false positive rates)
        * TPR (true positive rates)
        * The thresholds used to evaluated the selected metrics
        * The lower confidence interval for the FPR
        * The lower confidence interval for the TPR
        * The upper confidence interval for the FPR
        * The upper confidence interval for the TPR
    """
    return curves.curve_ci(
        numpy.asarray(y_true, dtype=numpy.int_),
        numpy.asarray(y_score, dtype=numpy.double),
        (curves.AxisType.FPR, curves.AxisType.TPR),
        functors.make_functor(utils.beta, lambda_=lambda_, coverage=coverage),
        "roc",
    )


def roc_auc_score(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float]:
    r"""Calculates the area under the ROC (FPR vs TPR) curve.

    This function mimics the scikit-learn API, except it also returns lower and
    upper bounds considering the credible regions defined in each threshold.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 3 floats:

        * the area under the ROC (FPR vs. TPR) curve
        * the lower bound considering the credible region defined by
          ``lambda_`` and ``coverage`` parameters.
        * the upper bound considering the credible region defined by
          ``lambda_`` and ``coverage`` parameters.
    """
    data = roc_curve(y_true, y_score, lambda_, coverage)
    # calculates lower and upper bounds based on CIs for each point (threshold)
    # of the curve
    lower, upper = curves.curve_ci_hull(
        curve=data,
        extrapolate_from_origin=False,  # should extrapolate from (x=1, y=0)
    )
    return (
        curves.area_under_the_curve(data[:2]),
        curves.area_under_the_curve(lower),
        curves.area_under_the_curve(upper),
    )


def det_curve(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[
    numpy.typing.NDArray[numpy.double],  # fpr
    numpy.typing.NDArray[numpy.double],  # fnr
    numpy.typing.NDArray[numpy.double],  # thresholds
    numpy.typing.NDArray[numpy.double],  # fpr lower ci
    numpy.typing.NDArray[numpy.double],  # fnr lower ci
    numpy.typing.NDArray[numpy.double],  # fpr upper ci
    numpy.typing.NDArray[numpy.double],  # fnr upper ci
]:
    r"""Computes the Detection Error-Tradeoff (DET) curve.

    Approximately follows API of :py:func:`sklearn.metrics.det_curve`.

    .. important::

       The returned credible regions are not immediately usable for plots or
       the evaluation of the area under the curve, only as point estimates for
       individual thresholds.  To plot, feed the output of this funtion to
       :py:func:`.curves.curve_ci_hull` and use the lower and upper estimates
       provided by that function instead.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        Seven 1-D floating point arrays corresponding to:

        * FPR (false positive rates)
        * FNR (false negative rates)
        * The thresholds used to evaluated the selected metrics
        * The lower confidence interval for the FPR
        * The lower confidence interval for the FNR
        * The upper confidence interval for the FPR
        * The upper confidence interval for the FNR
    """

    return curves.curve_ci(
        numpy.asarray(y_true, dtype=numpy.int_),
        numpy.asarray(y_score, dtype=numpy.double),
        (curves.AxisType.FPR, curves.AxisType.FNR),
        functors.make_functor(utils.beta, lambda_=lambda_, coverage=coverage),
        "det",
    )


def precision_recall_curve(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[
    numpy.typing.NDArray[numpy.double],  # precision
    numpy.typing.NDArray[numpy.double],  # redcall
    numpy.typing.NDArray[numpy.double],  # thresholds
    numpy.typing.NDArray[numpy.double],  # precision lower ci
    numpy.typing.NDArray[numpy.double],  # recall lower ci
    numpy.typing.NDArray[numpy.double],  # precision upper ci
    numpy.typing.NDArray[numpy.double],  # recall upper ci
]:
    r"""Computes Precision-Recall (PR) curve.

    Approximately follows API of
    :py:func:`sklearn.metrics.precision_recall_curve`.

    .. note::

        This package computes the precision-recall curve in a similar, but
        slightly different way than scikit-learn.  It does not add an extra
        (1.0, 0.0) at the end of the PR curve.  (c.f.: documentation for
        :py:func:`sklearn.metrics.precision_recall_curve`).

    .. important::

       The returned credible regions are not immediately usable for plots or
       the evaluation of the area under the curve, only as point estimates for
       individual thresholds.  To plot, feed the output of this funtion to
       :py:func:`.curves.curve_ci_hull` and use the lower and upper estimates
       provided by that function instead.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        Seven 1-D floating point arrays corresponding to:

        * Precision
        * Recall
        * The thresholds used to evaluated the selected metrics
        * The lower confidence interval for the Precision
        * The lower confidence interval for the Recall
        * The upper confidence interval for the Precision
        * The upper confidence interval for the Recall
    """

    return curves.curve_ci(
        numpy.asarray(y_true, dtype=numpy.int_),
        numpy.asarray(y_score, dtype=numpy.double),
        (curves.AxisType.PREC, curves.AxisType.REC),
        functors.make_functor(utils.beta, lambda_=lambda_, coverage=coverage),
        "pr",
    )


def average_precision_score(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    lambda_: float = 1.0,
    coverage: float = 0.95,
) -> tuple[float, float, float]:
    r"""Computes average precision (AP) from prediction scores.

    This function mimics the scikit-learn API, except it also returns lower and
    upper bounds considering the credible regions defined in each threshold.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    lambda_
        The parameterisation of the Beta prior to consider. Use
        :math:`\lambda=1` for a flat prior.  Use :math:`\lambda=0.5` for
        Jeffrey's prior.
    coverage
        A floating-point number between 0 and 1.0 indicating the coverage
        you are expecting.  A value of 0.95 will ensure 95% of the area under
        the probability density of the posterior is covered by the returned
        equal-tailed interval.


    Returns
    -------
        A tuple with 3 floats:

        * the area under the ROC (FPR vs. TPR) curve
        * the lower bound considering the credible region defined by
          ``lambda_`` and ``coverage`` parameters.
        * the upper bound considering the credible region defined by
          ``lambda_`` and ``coverage`` parameters.
    """
    data = precision_recall_curve(y_true, y_score, lambda_, coverage)
    # calculates lower and upper bounds based on CIs for each point (threshold)
    # of the curve
    lower, upper = curves.curve_ci_hull(
        curve=data,
        extrapolate_from_origin=True,  # should extrapolate from (x=0, y=0)
    )
    return (
        curves.average_metric(data[:2]),
        curves.average_metric(lower),
        curves.average_metric(upper),
    )
