# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import numpy
import pytest
import sklearn.metrics

import credible.bayesian.metrics


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_precision_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    sklearn_value = sklearn.metrics.precision_score(y_true, y_pred)
    exact, mode, lower, upper = credible.bayesian.metrics.precision_score(
        y_true, y_pred
    )

    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(sklearn_value, mode), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0):
        assert lower < mode
    if not numpy.isclose(mode, 1.0):
        assert upper > mode


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_recall_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    sklearn_value = sklearn.metrics.recall_score(y_true, y_pred)
    exact, mode, lower, upper = credible.bayesian.metrics.recall_score(
        y_true, y_pred
    )

    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(sklearn_value, mode), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0):
        assert lower < mode
    if not numpy.isclose(mode, 1.0):
        assert upper > mode


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_specificity_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    tn, fp, _, _ = sklearn.metrics.confusion_matrix(y_true, y_pred).ravel()
    sklearn_value = tn / (tn + fp)

    exact, mode, lower, upper = credible.bayesian.metrics.specificity_score(
        y_true, y_pred
    )

    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(sklearn_value, mode), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0):
        assert lower < mode
    if not numpy.isclose(mode, 1.0):
        assert upper > mode


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_accuracy_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    sklearn_value = sklearn.metrics.accuracy_score(y_true, y_pred)
    exact, mode, lower, upper = credible.bayesian.metrics.accuracy_score(
        y_true, y_pred
    )

    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(sklearn_value, mode), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0):
        assert lower < mode
    if not numpy.isclose(mode, 1.0):
        assert upper > mode


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_jaccard_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    sklearn_value = sklearn.metrics.jaccard_score(y_true, y_pred)
    exact, mode, lower, upper = credible.bayesian.metrics.jaccard_score(
        y_true, y_pred
    )

    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(sklearn_value, mode), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0):
        assert lower < mode
    if not numpy.isclose(mode, 1.0):
        assert upper > mode


@pytest.mark.parametrize(
    "threshold",
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    ids=lambda x: f"thres={x}",
)
def test_f1_score(example_results, threshold):
    y_true, y_score = example_results
    y_pred = (y_score >= threshold).astype(int)

    sklearn_value = sklearn.metrics.f1_score(y_true, y_pred)
    exact, mode, lower, upper = credible.bayesian.metrics.f1_score(
        y_true, y_pred
    )

    # given the nature of the M-C processes involved in the output of
    # f1_score(), we relax comparisons here.
    assert numpy.isclose(sklearn_value, exact), f"{sklearn_value} != {exact}"
    assert numpy.isclose(
        sklearn_value, mode, atol=1e-2
    ), f"{sklearn_value} != {mode}"
    if not numpy.isclose(mode, 0.0, atol=1e-2):
        assert lower < mode
    if not numpy.isclose(mode, 1.0, atol=1e-2):
        assert upper > mode


def test_roc_curve(example_results):
    y_true, y_score = example_results

    sklearn_ref = sklearn.metrics.roc_curve(y_true, y_score)
    data = credible.bayesian.metrics.roc_curve(y_true, y_score)

    assert numpy.allclose(sklearn_ref[0], data[0])
    assert numpy.allclose(sklearn_ref[1], data[1])
    assert numpy.allclose(sklearn_ref[2], data[2])
    assert all(data[3] <= data[0])
    assert all(data[4] <= data[1])
    assert all(data[5] >= data[0])
    assert all(data[6] >= data[1])


def test_det_curve(example_results):
    y_true, y_score = example_results

    sklearn_ref = sklearn.metrics.det_curve(y_true, y_score)
    data = credible.bayesian.metrics.det_curve(y_true, y_score)

    assert numpy.allclose(sklearn_ref[0], data[0])
    assert numpy.allclose(sklearn_ref[1], data[1])
    assert numpy.allclose(sklearn_ref[2], data[2])
    assert all(data[3] <= data[0])
    assert all(data[4] <= data[1])
    assert all(data[5] >= data[0])
    assert all(data[6] >= data[1])


def test_precision_recall_curve(example_results):
    y_true, y_score = example_results

    sklearn_ref = sklearn.metrics.precision_recall_curve(y_true, y_score)
    data = credible.bayesian.metrics.precision_recall_curve(y_true, y_score)

    assert numpy.allclose(sklearn_ref[2], data[2])  # thresholds
    # sklearn always adds (precision: 1.0, recall: 0) points w/o adding a
    # threshold.
    # assert numpy.allclose(sklearn_ref[0], data[0])
    assert numpy.allclose(sklearn_ref[0][: len(data[0])], data[0])
    # assert numpy.allclose(sklearn_ref[1], data[1])
    assert numpy.allclose(sklearn_ref[1][: len(data[1])], data[1])
    assert all(data[3] <= data[0])
    assert all(data[4] <= data[1])
    assert all(data[5] >= data[0])
    assert all(data[6] >= data[1])


def test_auc_score(example_results):
    y_true, y_score = example_results

    sklearn_ref = sklearn.metrics.roc_auc_score(y_true, y_score)
    data = credible.bayesian.metrics.roc_auc_score(y_true, y_score)

    assert numpy.isclose(data[0], sklearn_ref)
    assert data[1] <= data[0]
    assert data[2] >= data[0]


def test_avg_precision_score(example_results):
    y_true, y_score = example_results

    sklearn_ref = sklearn.metrics.average_precision_score(y_true, y_score)
    data = credible.bayesian.metrics.average_precision_score(y_true, y_score)

    assert numpy.isclose(data[0], sklearn_ref)
    assert data[1] <= data[0]
    assert data[2] >= data[0]
