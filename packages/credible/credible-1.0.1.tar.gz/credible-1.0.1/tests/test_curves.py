# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy

import credible.curves


def test_hull_curve_off_origin():
    # we test if the hull creation for ROC curves works as expected.
    # (x, y) = (0.0, 0.0) - lower (0.0, 0.0); upper (+0.1, +0.2), 0 degrees
    # (x, y) = (0.3, 0.7) - lower (-0.1, -0.2); upper (+0.2, +0.1), 45 degrees
    # (x, y) = (1.0, 1.0) - lower (-0.1, -0.2); upper (0.0, 0.0), 90 degrees

    # first, we simulate the output data of curve_ci
    data = (
        [0.0, 0.3, 1.0],  # x
        [0.0, 0.7, 1.0],  # y
        [1.0, 0.5, 0.0],  # thresholds (not used)
        [0.0, 0.2, 0.9],  # lower x
        [0.0, 0.5, 0.8],  # lower y
        [0.1, 0.5, 1.0],  # upper x
        [0.2, 0.8, 1.0],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.1, 0.44142135623731, 1.0]
    exp_lower_y = [0.0, 0.55857864376269, 0.8]

    # upper curve
    exp_upper_x = [0.0, 0.229289321881345, 1.0]
    exp_upper_y = [0.0, 0.770710678118655, 1.0]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=False
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x >= data[0]
    )  # lower curve to the right of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x <= data[0]
    )  # upper curve to the left of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data


def test_hull_curve_off_origin_2():
    # same test as before, but we move the extremeties off the origin and the
    # (1,1) point, yet keeping the same extremeties on the x-axis and on the
    # (1,0)-(1,1) axis.

    # first, we simulate the output data of curve_ci
    data = (
        [0.1, 0.3, 1.0],  # x
        [0.0, 0.7, 0.8],  # y
        [1.0, 0.5, 0.0],  # thresholds (not used)
        [0.0, 0.2, 0.9],  # lower x
        [0.0, 0.5, 0.6],  # lower y
        [0.2, 0.5, 1.0],  # upper x
        [0.2, 0.8, 1.0],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.2, 0.44142135623731, 1.0]
    exp_lower_y = [0.0, 0.55857864376269, 0.6]

    # upper curve
    exp_upper_x = [0.0, 0.229289321881345, 1.0]
    exp_upper_y = [0.0, 0.770710678118655, 1.0]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=False
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x >= data[0]
    )  # lower curve to the right of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x <= data[0]
    )  # upper curve to the left of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data


def test_hull_curve_off_origin_3():
    # same test as the first one, but we move the extremeties off the x-axis and
    # (1,0)-(1,1) axis to emulate missing points.

    # first, we simulate the output data of curve_ci
    data = (
        [0.0, 0.3, 0.9],  # x
        [0.2, 0.7, 1.0],  # y
        [1.0, 0.5, 0.0],  # thresholds (not used)
        [0.0, 0.2, 0.8],  # lower x
        [0.0, 0.5, 0.8],  # lower y
        [0.1, 0.5, 1.0],  # upper x
        [0.4, 0.8, 1.0],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.099503719020999, 0.44142135623731, 0.919611613513818]
    exp_lower_y = [0.1800992561958, 0.55857864376269, 0.803883864861816]

    # upper curve
    exp_upper_x = [0.0, 0.229289321881345, 0.9]
    exp_upper_y = [0.2, 0.770710678118655, 1.0]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=False
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x >= data[0]
    )  # lower curve to the right of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x <= data[0]
    )  # upper curve to the left of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data


def test_hull_curve_on_origin():
    # we test if the hull creation for DET curves works as expected.
    # (x, y) = (0.0, 1.0) - lower (0.0, -0.2); upper (0.1, 0.0), 90 degrees
    # (x, y) = (0.7, 0.7) - lower (-0.1, -0.2); upper (+0.2, +0.1), 45 degrees
    # (x, y) = (1.0, 0.0) - lower (-0.1, 0.0); upper (0.0, 0.2), 0 degrees

    # first, we simulate the output data of curve_ci
    data = (
        [0.0, 0.7, 1.0],  # x
        [1.0, 0.7, 0.0],  # y
        [0.0, 0.5, 1.0],  # thresholds (not used)
        [0.0, 0.6, 0.9],  # lower x
        [0.8, 0.5, 0.0],  # lower y
        [0.1, 0.9, 1.0],  # upper x
        [1.0, 0.8, 0.2],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.0, 0.610557280900008, 0.9]
    exp_lower_y = [0.8, 0.610557280900008, 0.0]

    # upper curve
    exp_upper_x = [0.0, 0.789442719099992, 1.0]
    exp_upper_y = [1.0, 0.789442719099992, 0.0]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=True
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x <= data[0]
    )  # lower curve to the left of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x >= data[0]
    )  # upper curve to the right of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data


def test_hull_curve_on_origin_2():
    # same test as before, but we move the extremeties off the (0,1) and the
    # (1,0) point, yet keeping the same extremeties on the x and y-axes.

    # first, we simulate the output data of curve_ci
    data = (
        [0.0, 0.7, 0.9],  # x
        [0.8, 0.7, 0.0],  # y
        [0.0, 0.5, 1.0],  # thresholds (not used)
        [0.0, 0.6, 0.8],  # lower x
        [0.6, 0.5, 0.0],  # lower y
        [0.1, 0.9, 1.0],  # upper x
        [1.0, 0.8, 0.2],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.0, 0.610557280900008, 0.8]
    exp_lower_y = [0.6, 0.610557280900008, 0.0]

    # upper curve
    exp_upper_x = [0.0, 0.789442719099992, 1.0]
    exp_upper_y = [1.0, 0.789442719099992, 0.0]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=True
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x <= data[0]
    )  # lower curve to the left of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x >= data[0]
    )  # upper curve to the right of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data


def test_hull_curve_on_origin_3():
    # same test as before, but we move the extremeties off the (0,1) and the
    # (1,0) point, but also off both x and y axes.

    # first, we simulate the output data of curve_ci
    data = (
        [0.1, 0.7, 1.0],  # x
        [1.0, 0.7, 0.2],  # y
        [0.0, 0.5, 1.0],  # thresholds (not used)
        [0.0, 0.6, 0.9],  # lower x
        [0.8, 0.5, 0.0],  # lower y
        [0.2, 0.9, 1.0],  # upper x
        [1.0, 0.8, 0.4],  # upper y
    )

    # bottom curve
    exp_lower_x = [0.080388386486182, 0.610557280900008, 0.900496280979001]
    exp_lower_y = [0.803883864861816, 0.610557280900008, 0.1800992561958]

    # upper curve
    exp_upper_x = [0.1, 0.789442719099992, 1.0]
    exp_upper_y = [1.0, 0.789442719099992, 0.2]

    lower, upper = credible.curves.curve_ci_hull(
        data, extrapolate_from_origin=True
    )

    assert numpy.allclose(exp_lower_x, lower[0]), f"{exp_lower_x} != {lower[0]}"
    assert numpy.allclose(exp_lower_y, lower[1]), f"{exp_lower_y} != {lower[1]}"

    assert numpy.allclose(exp_upper_x, upper[0]), f"{exp_upper_x} != {upper[0]}"
    assert numpy.allclose(exp_upper_y, upper[1]), f"{exp_upper_y} != {upper[1]}"

    assert numpy.alltrue(
        exp_lower_x <= data[0]
    )  # lower curve to the left of data
    assert numpy.alltrue(exp_lower_y <= data[1])  # lower curve below data
    assert numpy.alltrue(
        exp_upper_x >= data[0]
    )  # upper curve to the right of data
    assert numpy.alltrue(exp_upper_y >= data[1])  # upper curve above data
