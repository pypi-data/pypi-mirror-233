# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import matplotlib
import numpy
import pytest

matplotlib.use("agg")


@pytest.fixture
def example_results():
    # We simulate scores for a hypothethical system using a beta distribution
    # (bounded)

    numpy.random.seed(42)

    nb_samples1 = 200  # Sample size, higher makes it more precise (thinner CI)
    a1 = 6
    b1 = 10

    y_true = numpy.concatenate(
        (
            numpy.zeros((nb_samples1,), dtype=int),
            numpy.ones((nb_samples1,), dtype=int),
        )
    )
    y_score = numpy.concatenate(
        (
            numpy.random.beta(a=a1, b=b1, size=nb_samples1),
            numpy.random.beta(a=b1, b=a1, size=nb_samples1),
        )
    )

    # Plotting scores (example):
    # from matplotlib import pyplot as plt
    # negatives = y_score[y_true == 0]
    # plt.hist(negatives, bins=100, alpha=0.3, label="Negatives")
    # plt.hist(negatives, bins=100, histtype="step")
    # positives = y_score[y_true == 1]
    # plt.hist(positives, bins=100, alpha=0.3, label="Positives")
    # plt.hist(positives, bins=100, histtype="step")
    # plt.title("Scores (i.i.d. samples)")
    # plt.show()

    return y_true, y_score
