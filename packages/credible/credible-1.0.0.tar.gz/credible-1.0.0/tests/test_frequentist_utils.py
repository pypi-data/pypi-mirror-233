# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy

import credible.frequentist.utils


def test_clopper_pearson():
    assert numpy.allclose(
        (0.5, 0.01257911709342505, 0.98742088290657493),
        credible.frequentist.utils.clopper_pearson(1, 1),
    )

    assert numpy.allclose(
        (1.0, 0.69150289218123917, 1),
        credible.frequentist.utils.clopper_pearson(10, 0),
    )

    assert numpy.allclose(
        (0.0, 0, 0.30849710781876077),
        credible.frequentist.utils.clopper_pearson(0, 10),
    )


def test_agresti_coull():
    assert numpy.allclose(
        (0.5, 0.09453120573423074, 0.9054687942657693),
        credible.frequentist.utils.agresti_coull(1, 1),
    )

    assert numpy.allclose(
        (1.0, 0.6791126942494543, 1.0433545058876565),
        credible.frequentist.utils.agresti_coull(10, 0),
    )

    assert numpy.allclose(
        (0.0, -0.04335450588765652, 0.3208873057505457),
        credible.frequentist.utils.agresti_coull(0, 10),
    )


def test_wilson():
    assert numpy.allclose(
        (0.5, 0.09453120573423074, 0.9054687942657693),
        credible.frequentist.utils.wilson(1, 1),
    )

    assert numpy.allclose(
        (1.0, 0.7224672001371107, 0.9999999999999999),
        credible.frequentist.utils.wilson(10, 0),
    )

    assert numpy.allclose(
        (0.0, 0.0, 0.2775327998628892),
        credible.frequentist.utils.wilson(0, 10),
    )
