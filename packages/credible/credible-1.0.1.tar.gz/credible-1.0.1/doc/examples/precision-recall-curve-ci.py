# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import numpy

from matplotlib import pyplot as plt

import credible.bayesian.metrics
import credible.curves
import credible.plot

# We simulate scores for 2 hypothethical systems.
# Scores are beta distributed for a "perfect" example
nb_samples1 = 200  # Sample size, higher makes it more precise (thinner CI)
a1 = 6
b1 = 10

nb_samples2 = 100  # Sample size, higher makes it more precise (thinner CI)
a2 = 7
b2 = 10
numpy.random.seed(42)

y_true1 = numpy.concatenate(
    (
        numpy.zeros((nb_samples1,), dtype=int),
        numpy.ones((nb_samples1,), dtype=int),
    )
)
y_score1 = numpy.concatenate(
    (
        numpy.random.beta(a=a1, b=b1, size=nb_samples1),
        numpy.random.beta(a=b1, b=a1, size=nb_samples1),
    )
)

y_true2 = numpy.concatenate(
    (
        numpy.zeros((nb_samples2,), dtype=int),
        numpy.ones((nb_samples2,), dtype=int),
    )
)
y_score2 = numpy.concatenate(
    (
        numpy.random.beta(a=a2, b=b2, size=nb_samples2),
        numpy.random.beta(a=b2, b=a2, size=nb_samples2),
    )
)

# Plotting scores (example):
# negatives1 = y_score1[y_true1 == 0]
# ph = plt.hist(negatives1, bins=100, alpha=0.3, label="Negatives")
# plt.hist(negatives1, bins=100, color=h1[2][0].get_facecolor()[:3], histtype="step")
# positives1 = y_score1[y_true1 == 1]
# nh = plt.hist(positives1, bins=100, alpha=0.3, label="Positives")
# plt.hist(positives1, bins=100, color=h1[2][0].get_facecolor()[:3], histtype="step")
# plt.title("Scores (i.i.d. samples)")

with credible.plot.tight_layout_f1iso(axis_labels=("Recall", "Precision")):
    pr1 = credible.bayesian.metrics.precision_recall_curve(y_true1, y_score1)
    lower1, upper1 = credible.curves.curve_ci_hull(
        pr1, extrapolate_from_origin=True
    )
    avp1 = credible.bayesian.metrics.average_precision_score(y_true1, y_score1)
    label1 = (
        f"System 1 (AP: {avp1[0]:.2f} - 95% CI: {avp1[1]:.2f}-{avp1[2]:.2f})"
    )
    objs1 = credible.plot.curve_ci(
        (pr1[1], pr1[0]),
        (lower1[1], lower1[0]),
        (upper1[1], upper1[0]),
        # avoid curve interpolation to sync with AP approach
        drawstyle="steps-post",
    )

    pr2 = credible.bayesian.metrics.precision_recall_curve(y_true2, y_score2)
    lower2, upper2 = credible.curves.curve_ci_hull(
        pr2, extrapolate_from_origin=True
    )
    avp2 = credible.bayesian.metrics.average_precision_score(y_true2, y_score2)
    label2 = (
        f"System 1 (AP: {avp2[0]:.2f} - 95% CI: {avp2[1]:.2f}-{avp2[2]:.2f})"
    )
    objs2 = credible.plot.curve_ci(
        (pr2[1], pr2[0]),
        (lower2[1], lower2[0]),
        (upper2[1], upper2[0]),
        # avoid curve interpolation to sync with AP approach
        drawstyle="steps-post",
    )

    plt.legend(
        (objs1, objs2),
        (label1, label2),
        loc="best",
        fancybox=True,
        framealpha=0.7,
    )

plt.show()
