# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Implementation of :py:mod:`Scikit-Learn compatible measures
<sklearn.metrics>` with bayesian credible regions for k-folding experiments."""

import typing

import numpy
import numpy.typing
import sklearn.metrics

from . import utils
from .metrics import NUMBER_MC_SAMPLES


def precision_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
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
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The average precision, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    fp_array = cms[:, 1]
    tp_array = cms[:, 3]
    _, mode, lower, upper = utils.average_beta(
        tp_array, fp_array, lambda_, coverage, nb_samples
    )
    return (
        numpy.mean(tp_array / (tp_array + fp_array)).item(),
        mode,
        lower,
        upper,
    )


def recall_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
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
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The average recall, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    fn_array = cms[:, 2]
    tp_array = cms[:, 3]
    _, mode, lower, upper = utils.average_beta(
        tp_array, fn_array, lambda_, coverage, nb_samples
    )
    return (
        numpy.mean(tp_array / (tp_array + fn_array)).item(),
        mode,
        lower,
        upper,
    )


def specificity_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
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
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The average specificity, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    tn_array = cms[:, 0]
    fp_array = cms[:, 1]
    _, mode, lower, upper = utils.average_beta(
        tn_array, fp_array, lambda_, coverage, nb_samples
    )
    return (
        numpy.mean(tn_array / (tn_array + fp_array)).item(),
        mode,
        lower,
        upper,
    )


def accuracy_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
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
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The average accuracy, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    tn_array = cms[:, 0]
    fp_array = cms[:, 1]
    fn_array = cms[:, 2]
    tp_array = cms[:, 3]
    _, mode, lower, upper = utils.average_beta(
        tp_array + tn_array, fn_array + fp_array, lambda_, coverage, nb_samples
    )
    return (
        numpy.mean(
            (tp_array + tn_array) / (tn_array + fp_array + fn_array + tp_array)
        ).item(),
        mode,
        lower,
        upper,
    )


def jaccard_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
    lambda_: float = 1.0,
    coverage: float = 0.95,
    nb_samples: int = NUMBER_MC_SAMPLES,
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
    nb_samples
        number of generated variates for the M-C simulation


    Returns
    -------
        A tuple with 4 floating-point numbers:

        * The average jaccard score, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    fp_array = cms[:, 1]
    fn_array = cms[:, 2]
    tp_array = cms[:, 3]
    _, mode, lower, upper = utils.average_beta(
        tp_array, fp_array + fn_array, lambda_, coverage, nb_samples
    )
    return (
        numpy.mean(tp_array / (tp_array + fn_array + fp_array)).item(),
        mode,
        lower,
        upper,
    )


def f1_score(
    y_true: typing.Iterable[typing.Iterable[int]],
    y_pred: typing.Iterable[typing.Iterable[int]],
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

        * The average F1-score, as would be returned by scikit-learn
        * The mode of the posterior distribution
        * The lower value of the credible region/confidence interval
        * The upper value of the credible region/confidence interval
    """
    cms = numpy.asarray(
        [
            sklearn.metrics.confusion_matrix(i, j).ravel()
            for (i, j) in zip(y_true, y_pred)
        ],
        dtype=numpy.int_,
    )
    fp_array = cms[:, 1]
    fn_array = cms[:, 2]
    tp_array = cms[:, 3]
    variates = utils.average_f1_posterior(
        tp_array, fp_array, fn_array, lambda_, nb_samples
    )
    _, mode, lower, upper = utils.evaluate_statistics(
        variates, coverage, bins="auto"
    )
    return (
        numpy.mean(
            (2 * tp_array) / ((2 * tp_array) + fn_array + fp_array)
        ).item(),
        mode,
        lower,
        upper,
    )
