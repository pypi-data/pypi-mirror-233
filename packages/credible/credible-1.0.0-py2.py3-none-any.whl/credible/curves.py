# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Curve plotting support.

Code in this module expresses classic performance curves for system performance
evaluation as sets of coordinates.  Use the module :py:mod:`.plot` to make
graphical representations.

.. include:: ../links.rst
"""

import enum
import typing

import numpy
import numpy.linalg
import numpy.typing
import sklearn.metrics

from .utils import CIArrayFunctor, CIFunctor


class AxisType(enum.Enum):
    r"""Supported types for metrics that have binomial distributions.

    This enumeration contains a list of metrics (rates) that have binomial
    distributions.  For each available entry, we define the successes (``k``)
    and failures (``l``) such that the metric can be calculated as such:

    .. math::

       metric = \frac{k}{k+l}

    Keys with the same (integer) value represent synonyms.

    Definitions are taken from
    https://en.wikipedia.org/wiki/Confusion_matrix.
    """

    TPR = (1, "true positive rate", "tpr")
    REC = (1, "recall", "rec")
    SEN = (1, "sensitivity", "sen")
    TNR = (2, "true negative rate", "tnr")
    SPEC = (2, "specificity", "spec")
    SEL = (2, "selectivity", "sel")
    FNR = (3, "false negative rate", "fnr")
    FPR = (4, "false positive rate", "fpr")
    PREC = (5, "precision", "prec")
    PPV = (5, "positive predictive value", "ppv")
    NPV = (6, "negative predictive value", "npv")

    def __init__(self, key: int, fullname: str, abbreviation: str):
        self.key = key
        self.fullname = fullname
        self.abbreviation = abbreviation

    def make_cm_functor(
        self, ci_functor: CIFunctor
    ) -> typing.Callable[
        [numpy.typing.NDArray[numpy.int_]], tuple[float, float, float]
    ]:
        """Returns callable to treat binary confusion matrices and produce
        curve and confidence intervals.

        This method will take a confidence interval functor and will wrap it
        over a complete confusion-matrix functor that produces the metric
        estimates, lower and upper confidence intervals, in this order.


        Parameters
        ----------
        ci_functor
            Functor to evaluate the rate, lower and upper confidence intervals
            from (binomial) successes and failures.


        Returns
        -------
            A functor that can operate directly from the confusion matrix
            outputs (instead of success and failures), with the same return
            values as the input functor.
        """
        successes = failures = -1
        match self.key:
            # Notice scikit-learn order:
            # tn, fp, fn, tp = confusion_matrix(...).ravel()
            # From https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
            case 1:  # tpr
                successes = 3  # tp
                failures = 2  # fn
            case 2:  # tnr
                successes = 0  # tn
                failures = 1  # fp
            case 3:  # fnr
                successes = 2  # fn
                failures = 3  # tp
            case 4:  # fpr
                successes = 1  # fp
                failures = 0  # tn
            case 5:  # precision
                successes = 3  # tp
                failures = 1  # fp
            case 6:  # npv
                successes = 0  # tn
                failures = 2  # fn

        return lambda x: ci_functor(x[successes], x[failures])


def curve_ci(
    y_true: typing.Iterable[int],
    y_score: typing.Iterable[float],
    axes: tuple[AxisType, AxisType],
    ci_functor: CIFunctor,
    skl_functor_name: typing.Literal["roc", "det", "pr"],
) -> tuple[
    numpy.typing.NDArray[numpy.double],  # axes[0] rate
    numpy.typing.NDArray[numpy.double],  # axes[1] rate
    numpy.typing.NDArray[numpy.double],  # thresholds
    numpy.typing.NDArray[numpy.double],  # axes[0] lower ci
    numpy.typing.NDArray[numpy.double],  # axes[1] lower ci
    numpy.typing.NDArray[numpy.double],  # axes[0] upper ci
    numpy.typing.NDArray[numpy.double],  # axes[1] upper ci
]:
    """Calculates points and confidence intervals of an arbitrary performance
    curve.

    This function can calculate the rates and confidence intervals of an
    user-configurable ROC-style curve.


    Parameters
    ----------
    y_true
        Ground truth (correct) labels.
    y_score
        Target scores, can either be probability estimates of the positive
        class, confidence values, or non-thresholded measure of decisions (as
        returned by “decision_function” on some classifiers).
    n_points
        The number of points, in which the ROC curve are calculated, which are
        distributed uniformly in the range ``[min(negatives, positives),
        max(negatives, positives)]``
    axes
        Which axes to calculate the curve for.  Note not all combinations make
        sense (no checks are performed).  You should avoid computing a curve,
        for example, of TPR against FNR as these rates are complementary to
        1.0.
    ci_functor
        A callable to be used to calculate the estimate, lower, and upper
        bounds for the measures of interest on each of the axes.  This callable
        will receive (binomial, integer) successes and failures, and produce
        the rate, lower and upper bounds respecctively.
    skl_functor_name
        The name of a callable from scikit-learn to calculate basic thresholds
        for the target curve.  Use one of:

        * ``roc``: :py:func:`sklearn.metrics.roc_curve`
        * ``det``: :py:func:`sklearn.metrics.det_curve`
        * ``pr``: :py:func:`sklearn.metrics.precision_recall_curve`


    Returns
    -------
        Seven 1-D floating point arrays corresponding to:

        * The selected metric for the first axis
        * The selected metric for the second axis
        * The thresholds used to evaluated the selected metrics, in decreasing
          order.
        * The lower confidence interval for the selected metric for the first
          axis
        * The lower confidence interval selected metric for the second axis
        * The upper confidence interval for the selected metric for the first
          axis
        * The upper confidence interval selected metric for the second axis
    """
    # finally, we do the computing of the curve
    y_true_array = numpy.asarray(y_true, dtype=numpy.int_)
    y_score_array = numpy.asarray(y_score, dtype=numpy.double)

    skl_functor = sklearn.metrics.roc_curve
    match skl_functor_name:
        case "roc":
            skl_functor = sklearn.metrics.roc_curve
        case "det":
            skl_functor = sklearn.metrics.det_curve
        case "pr":
            skl_functor = sklearn.metrics.precision_recall_curve
    _, _, thresholds = skl_functor(y_true_array, y_score_array)

    cm_per_threshold = [
        sklearn.metrics.confusion_matrix(y_true_array, (y_score_array >= t))
        .ravel()
        .astype(numpy.int_)
        for t in thresholds
    ]

    # convert confusion-matrices per threshold into rate, lower, and upper
    # values per threshold
    op0 = axes[0].make_cm_functor(ci_functor)
    ax0 = numpy.asarray([op0(k) for k in cm_per_threshold], dtype=numpy.double)
    op1 = axes[1].make_cm_functor(ci_functor)
    ax1 = numpy.asarray([op1(k) for k in cm_per_threshold], dtype=numpy.double)

    # ensure we have no lower that is higher than the values and vice-versa
    ax0[:, 1] = numpy.min((ax0[:, 0], ax0[:, 1]), axis=0)
    ax0[:, 2] = numpy.max((ax0[:, 0], ax0[:, 2]), axis=0)
    ax1[:, 1] = numpy.min((ax1[:, 0], ax1[:, 1]), axis=0)
    ax1[:, 2] = numpy.max((ax1[:, 0], ax1[:, 2]), axis=0)

    return (
        ax0[:, 0],
        ax1[:, 0],
        thresholds,
        ax0[:, 1],
        ax1[:, 1],
        ax0[:, 2],
        ax1[:, 2],
    )


def curve_ci_hull(
    curve: tuple[
        typing.Iterable[float],  # axes[0] rate
        typing.Iterable[float],  # axes[1] rate
        typing.Iterable[float],  # thresholds (ignored)
        typing.Iterable[float],  # axes[0] lower ci
        typing.Iterable[float],  # axes[1] lower ci
        typing.Iterable[float],  # axes[0] upper ci
        typing.Iterable[float],  # axes[1] upper ci
    ],
    extrapolate_from_origin: bool = True,
) -> tuple[
    tuple[
        numpy.typing.NDArray[numpy.double], numpy.typing.NDArray[numpy.double]
    ],
    tuple[
        numpy.typing.NDArray[numpy.double], numpy.typing.NDArray[numpy.double]
    ],
]:
    """Calculates lower and upper confidence intervals of a curve.

    This function calculates the hulls for 2 curves that are formed from points
    defining the lower and upper bounds of the curve's credible/confidence
    intervals for each measured threshold.

    It returns the curve (no changes), as well as the lower and upper bounds of
    the (central) curve.

    To calculate the upper and lower curves, we do not consider the extremities
    of the upper and lower bounds, as those points would translate to
    pessimistic estimations of the true confidence interval bounds.  Instead,
    we simply find the intersection of a straight line from the origin (0,0)
    and the ellipse 90-degree sector inscribed in the appropriate quarter of a
    rectangle centered at the ROC point, and its lower and upper bound CI
    estimates on both directions (horizontal and vertical).  If
    ``extrapolate_from_origin`` is set to ``False``, then intersections are
    created from ``(x, y) = (1, 0)``.


    Parameters
    ----------
    curve
        Seven 1-D floating point arrays corresponding to:

        * The selected metric for the first axis
        * The selected metric for the second axis
        * The thresholds (in decreasing order, as produced by scikit-learn)
        * The lower confidence interval for the selected metric for the first
          axis
        * The lower confidence interval selected metric for the second axis
        * The upper confidence interval for the selected metric for the first
          axis
        * The upper confidence interval selected metric for the second axis
    extrapolate_from_origin
        To calculate the upper hull, we consider two distinct cases: if
        ``extrapolate_from_origin`` is ``True`` (default), then we consider the
        curve starts (or finishes) at coordinate ``(x,y) = (1,0)`` and finishes
        (or starts) at ``(x,y) = (0,1)``.  This is the case if the user is
        plotting TPR against TNR or FPR against FNR.  If
        ``extrapolate_from_origin`` is ``False``, then we consider the curve
        starts (or finishes) at ``(x,y) = (0,0)``, and finishes (or starts) at
        ``(x,y) = (1,1)``.

        If ``extrapolate_from_origin`` is ``True`` (default), each point of the
        curve to extrapolates to the right and upper points defined by the
        upper bounds of the credible/confidence intervals, and to the left and
        lower points defined by the lower bounds of the intervals.

        If ``extrapolate_from_origin`` is ``False``, each point of the curve to
        extrapolates to the left and upper points defined by the upper bounds
        of the credible/confidence intervals, and to the right and lower points
        defined by the lower bounds of the intervals.


    Returns
    -------
        Two curves as follows:

        * lower: Two 1D arrays of floats that expresses the lower-bound of
          curve, for the first and second coordinates respectively.
        * upper: Two 1D arrays of floats that expresses the upper-bound of
          curve, for the first and second coordinates respectively.
    """

    def _ellipse_intersect(
        a: numpy.typing.NDArray[numpy.double],
        b: numpy.typing.NDArray[numpy.double],
        i: numpy.typing.NDArray[numpy.double],
        j: numpy.typing.NDArray[numpy.double],
        quadrant: typing.Literal["tl", "tr", "bl", "br"],
    ) -> tuple[
        numpy.typing.NDArray[numpy.double], numpy.typing.NDArray[numpy.double]
    ]:
        r"""Calculates the intersection of a line, passing at the center of the
        ellipse, and the ellipse itself.

        See: https://mathworld.wolfram.com/Ellipse-LineIntersection.html

        .. math::

           x &= \frac{1}{\sqrt{\frac{1}{a^2}+\frac{j^2}{b^2 i^2}}} \\
           y &= x \frac{j}{i}


        Parameters
        ----------
        a
            Width of the ellipse
        b
            Height of the ellipse
        i
            Width of the reference vector (to compute angle)
        j
            Height of the reference vector (to compute angle)
        quadrant
            The quadrant applicable to the vector direction: either "tl"
            (top-left), "tr" (top-right), "bl" (bottom-left) or "br"
            (bottom-right).


        Returns
        -------
            A tuple containing the x and y coordinates of the curve
        """

        # radius calculation, without direction
        eps = 1e-8
        num = (a**2) * (b**2) * (i**2)
        den = ((b**2) * (i**2)) + ((a**2) * (j**2))
        x = numpy.sqrt(
            numpy.divide(num, den, out=numpy.zeros_like(a), where=(den > eps))
        )
        y = numpy.divide(x * j, i, out=numpy.zeros_like(a), where=(i > eps))

        # when close to the x-axis, just re-use the ellipse width
        x = numpy.where(j < eps, a, x)
        # when close to the (1,0)-(1,1)-axis, just re-use the ellipse height
        y = numpy.where(i < eps, b, y)

        match quadrant:
            case "tr":  # add on both directions
                return (i + x, j + y)
            case "tl":  # add on y direction, subtract on x
                # n.b.: we use (1-i) to recover the original spatial
                # coordinates (see below on the call to this function)
                return ((1 - i) - x, j + y)
            case "bl":  # subtract on both directions
                return (i - x, j - y)
            case "br":  # subtract on y direction, add on x
                # n.b.: we use (1-i) to recover the original spatial
                # coordinates (see below on the call to this function)
                return ((1 - i) + x, j - y)

    (x, y, _, x_low, y_low, x_high, y_high) = tuple(
        numpy.asarray(k, dtype=numpy.double) for k in curve
    )

    if extrapolate_from_origin:  # sectors are lower left or upper right
        # N.B.: distance to origin is approximately symmetric considering the
        # whole curve

        # (x, y) -> (x_low, y_low)
        lower_x, lower_y = _ellipse_intersect(
            numpy.abs(x_low - x),  # width of ellipse
            numpy.abs(y_low - y),  # height of ellipse
            x,  # width of reference vector (only angle matters)
            y,  # height of reference vector (only angle matters)
            "bl",
        )
        # (x, y) -> (x_high, y_high)
        upper_x, upper_y = _ellipse_intersect(
            numpy.abs(x_high - x),  # width of ellipse
            numpy.abs(y_high - y),  # height of ellipse
            x,  # width of reference vector (only angle matters)
            y,  # height of reference vector (only angle matters)
            "tr",
        )

    else:  # sectors are lower right or upper left
        # N.B.: angles must be taken with respect to (1,0) and not (0,0) as the
        # curve is facing the other direction.

        # (x, y) -> (x_high, y_low)
        lower_x, lower_y = _ellipse_intersect(
            numpy.abs(x_high - x),  # width of ellipse
            numpy.abs(y_low - y),  # height of ellipse
            1 - x,  # width of reference vector (only angle matters)
            y,  # height of reference vector (only angle matters)
            "br",
        )
        # (x, y) -> (x_low, y_high)
        upper_x, upper_y = _ellipse_intersect(
            numpy.abs(x_low - x),  # width of ellipse
            numpy.abs(y_high - y),  # height of ellipse
            1 - x,  # width of reference vector (only angle matters)
            y,  # height of reference vector (only angle matters)
            "tl",
        )

    return (lower_x, lower_y), (upper_x, upper_y)


def area_under_the_curve(
    curve: tuple[
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
    ]
) -> float:
    """Calculates the area under a curve using a trapezoidal rule.

    Parameters
    ----------
    curve
        A tuple with 2 1D sequences of floating point numbers representing the
        first and second coordinate of the curve whose you want to evaluate AUC
        for.

    Returns
    -------
        The area under the curve (floating point scalar).
    """

    return numpy.abs(numpy.trapz(curve[1], curve[0]))


def average_metric(
    curve: tuple[
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
    ]
) -> float:
    r"""Calculates the area under a curve using a rectangle rule.

    Typically used to calculate the average precision (AP) as in:
    https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)#Average_precision

    .. math::
       \text{AP} &= \sum_n (R_n - R_{n-1}) P_n \\
       \text{AP} &= \sum_n (curve1[n] - curve1[n-1]) curve0[n]

    According to the scikit-learn documentation for
    :py:func:`sklearn.metrics.average_precision_score`, this implementation
    *"is different from computing the area under the precision-recall curve
    with the trapezoidal rule, which uses linear interpolation and can be too
    optimistic"*.

    .. note::

        Due to differences in the way this package computes the
        precision-recall curve (does not add an extra (1.0, 0.0) at the end of
        the PR curve like sklearn does, see documentation for
        :py:func:`sklearn.metrics.precision_recall_curve`), we compensate this
        here.


    Parameters
    ----------
    curve
        A tuple with 2 1D sequences of floating point numbers representing the
        first and second coordinate of the curve whose you want to evaluate AUC
        for.


    Returns
    -------
        The area under the curve (floating point scalar).
    """
    return -sum(numpy.diff(numpy.append(curve[1], 0.0)) * curve[0])


def estimated_ci_coverage(
    ci_functor: CIArrayFunctor,
    n: int = 100,
) -> numpy.typing.NDArray[numpy.double]:
    """Returns the approximate coverage of a credible region or confidence
    interval estimator.

    Reference: `This blog post <ci-evaluation_>`_.


    Parameters
    ----------
    f : object
        A callable that accepts ``k``, the number of successes (1D integer
        numpy.ndarray), ``l`` (1D integer numpy.ndarray), the number of
        failures to account for in the estimation of the interval/region.  This
        function must return two float parameters only corresponding to the
        lower and upper bounds of the credible region or confidence interval
        being estimated.
    n
        The number of bernoulli trials to consider on the binomial
        distribution.  This represents the total number of samples you'd have
        for your experiment.


    Returns
    -------
        The actual coverage curve, you can expect.  The first row corresponds
        to the values of ``p`` that were probed.  The second row, the actual
        coverage considering a simulated binomial distribution with size ``n``.
    """

    coverage = []
    size = 10000  # how many experiments to do at each try
    r = numpy.arange(1 / n, 1.0, step=1 / n)

    for p in r:
        k = numpy.random.binomial(n=n, p=p, size=size)
        _, lower, upper = ci_functor(k, n - k)
        covered = numpy.asarray((lower < p) & (p < upper), dtype=float)
        coverage.append(covered.mean())

    return numpy.vstack((r, numpy.asarray(coverage, dtype=float)))
