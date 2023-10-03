# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import itertools

import numpy
import scipy.special
import scipy.stats

import credible.bayesian.utils


def test_bayesian_precision_comparison():
    # system 1 performance
    TP1 = 10
    # FN1 = 5
    # TN1 = 5
    FP1 = 10

    # system 2 performance
    TP2 = 3
    # FN2 = 3
    # TN1 = 4
    FP2 = 2

    nb_samples = 10000  # Sample size, higher makes it more precise
    lambda_ = 0.5  # use 1.0 for a flat prior, or 0.5 for Jeffrey's prior

    numpy.random.seed(42)  # for the monte-carlo simulation
    prob = credible.bayesian.utils.compare_beta_posteriors(
        TP2, FP2, TP1, FP1, lambda_, nb_samples
    )

    assert numpy.allclose(prob, 0.6547)


def test_bayesian_recall_comparison():
    # system 1 performance
    TP1 = 10
    FN1 = 5
    # TN1 = 5
    # FP1 = 10

    # system 2 performance
    TP2 = 3
    FN2 = 3
    # TN1 = 4
    # FP2 = 2

    nb_samples = 10000  # Sample size, higher makes it more precise
    lambda_ = 0.5  # use 1.0 for a flat prior, or 0.5 for Jeffrey's prior

    # recall: TP / TP + FN, k=TP, l=FN

    # now we calculate what is the probability that system 2's recall
    # measurement is better than system 1
    numpy.random.seed(42)  # for the monte-carlo simulation
    prob = credible.bayesian.utils.compare_beta_posteriors(
        TP2, FN2, TP1, FN1, lambda_, nb_samples
    )

    assert numpy.allclose(prob, 0.2390)


def test_bayesian_f1_comparison():
    # system 1 performance
    TP1 = 10
    FN1 = 5
    # TN1 = 5
    FP1 = 10

    # system 2 performance
    TP2 = 3
    FN2 = 3
    # TN1 = 4
    FP2 = 2

    nb_samples = 100000  # Sample size, higher makes it more precise
    lambda_ = 0.5  # use 1.0 for a flat prior, or 0.5 for Jeffrey's prior

    # now we calculate what is the probability that system 2's recall
    # measurement is better than system 1
    numpy.random.seed(42)
    prob = credible.bayesian.utils.compare_f1_scores(
        TP2, FP2, FN2, TP1, FP1, FN1, lambda_, nb_samples
    )

    assert numpy.allclose(prob, 0.42571)


def test_bayesian_system_comparison():
    numpy.random.seed(1234)
    nb_samples = 50

    # expected output of the system
    labels = numpy.ones(nb_samples, dtype=bool)
    ratio = 0.2
    labels[: int(numpy.ceil(ratio * nb_samples))] = 0
    numpy.random.shuffle(labels)

    # system1 has 10% error, so we flip its bits by that amount randomly
    flip_probability = numpy.random.choice(
        [False, True], p=[0.9, 0.1], size=labels.shape
    )
    system1_output = numpy.logical_xor(labels, flip_probability)
    system1_acc = numpy.count_nonzero(
        ~numpy.logical_xor(system1_output, labels)
    ) / len(labels)

    # system2 has 20% error, so we flip its bits by that amount randomly
    flip_probability = numpy.random.choice(
        [False, True], p=[0.85, 0.15], size=labels.shape
    )
    system2_output = numpy.logical_xor(labels, flip_probability)
    system2_acc = numpy.count_nonzero(
        ~numpy.logical_xor(system2_output, labels)
    ) / len(labels)

    assert numpy.allclose(system1_acc, 0.88)
    assert numpy.allclose(system2_acc, 0.82)

    # calculate when systems agree and disagree
    n1 = numpy.count_nonzero(
        (~numpy.logical_xor(system1_output, labels))  # correct for system 1
        & numpy.logical_xor(system2_output, labels)  # incorrect for system 2
    )
    n2 = numpy.count_nonzero(
        (~numpy.logical_xor(system2_output, labels))  # correct for system 2
        & numpy.logical_xor(system1_output, labels)  # incorrect for system 1
    )
    n3 = nb_samples - n1 - n2
    assert n1 == 8
    assert n2 == 5
    assert n3 == 37
    assert n1 + n2 + n3 == nb_samples
    prob = credible.bayesian.utils.compare_systems(
        [n1, n2, n3], [0.5, 0.5, 0.5], 1000000
    )
    assert numpy.allclose(prob, 0.79665)


def test_beta_coverage():
    # tests if the returned value by beta() corresponds to the correct total
    # requested area using scipy.special.beatinc()

    A = [50, 10, 1000]
    B = [100, 5, 100]
    Prior = [1.0, 0.5]
    Coverage = [0.80, 0.90, 0.95]

    # just does a bunch of different combinatorics and check our implementation
    for a, b, prior, coverage in itertools.product(A, B, Prior, Coverage):
        # print(a, b, prior, coverage)

        _, _, lower, upper = credible.bayesian.utils.beta(a, b, prior, coverage)

        # scipy.special.betainc should return a very similar result
        area_low = scipy.special.betainc(a + prior, b + prior, lower)
        area_high = scipy.special.betainc(a + prior, b + prior, upper)
        assert numpy.isclose(
            (area_low, area_high), ((1 - coverage) / 2, (1 + coverage) / 2)
        ).all()
