# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import matplotlib.pyplot as plt

import credible.bayesian.metrics
import credible.curves
import credible.plot


def test_roc(example_results, tmp_path):
    y_true, y_score = example_results

    with credible.plot.tight_layout(
        axis_labels=("False Positive Rate", "True Positive Rate")
    ):
        roc = credible.bayesian.metrics.roc_curve(y_true, y_score)
        lower, upper = credible.curves.curve_ci_hull(
            roc, extrapolate_from_origin=False
        )

        assert all(lower[0] >= roc[0])
        assert all(lower[1] <= roc[1])
        assert all(upper[0] <= roc[0])
        assert all(upper[1] >= roc[1])

        auc = credible.curves.area_under_the_curve(roc[:2])
        auc_lower = credible.curves.area_under_the_curve(lower)
        auc_upper = credible.curves.area_under_the_curve(upper)
        label = (
            f"System (AUC: {auc:.2f} - 95% CR: {auc_lower:.2f}-{auc_upper:.2f})"
        )
        objs = credible.plot.curve_ci(roc[:2], lower, upper)

        plt.legend((objs,), (label,), loc="best", fancybox=True, framealpha=0.7)

        output_path = tmp_path / "test.png"
        plt.savefig(output_path)
        assert output_path.exists()

        # compares to what sklearn does:
        # from sklearn.metrics import RocCurveDisplay

        # RocCurveDisplay.from_predictions(y_true, y_score)
        # ax = plt.gca()
        # ax.set_ylim([0.0, 1.0])
        # ax.set_xlim([0.0, 1.0])
        # output_path_ref = tmp_path / "sklearn.png"
        # plt.savefig(output_path_ref)

        # __import__("os").system(f"open {str(tmp_path)}")
        # __import__("pdb").set_trace()
        # pass


def test_precision_recall(example_results, tmp_path):
    y_true, y_score = example_results

    with credible.plot.tight_layout_f1iso(axis_labels=("Recall", "Precision")):
        curve = credible.bayesian.metrics.precision_recall_curve(
            y_true, y_score
        )
        lower, upper = credible.curves.curve_ci_hull(
            curve, extrapolate_from_origin=True
        )

        assert all(lower[0] <= curve[0])
        assert all(lower[1] <= curve[1])
        assert all(upper[0] >= curve[0])
        assert all(upper[1] >= curve[1])

        # calculates the average precision-recall
        auc = credible.curves.average_metric(curve[:2])
        auc_lower = credible.curves.average_metric(lower)
        auc_upper = credible.curves.average_metric(upper)

        label = (
            f"System (APR: {auc:.2f} - 95% CR: {auc_lower:.2f}-{auc_upper:.2f})"
        )
        objs = credible.plot.curve_ci(
            (curve[1], curve[0]),
            (lower[1], lower[0]),
            (upper[1], upper[0]),
            # avoid curve interpolation to sync with AP approach
            drawstyle="steps-post",
        )

        plt.legend((objs,), (label,), loc="best", fancybox=True, framealpha=0.7)

        output_path = tmp_path / "test.png"
        plt.savefig(output_path)
        assert output_path.exists()

        # compares to what sklearn does:
        # from sklearn.metrics import PrecisionRecallDisplay
        # PrecisionRecallDisplay.from_predictions(y_true, y_score)
        # ax = plt.gca()
        # ax.set_ylim([0.0, 1.0])
        # ax.set_xlim([0.0, 1.0])
        # output_path_ref = tmp_path / "sklearn.png"
        # plt.savefig(output_path_ref)
        #
        # __import__("os").system(f"open {str(tmp_path)}")
        # __import__("pdb").set_trace()
        # pass
