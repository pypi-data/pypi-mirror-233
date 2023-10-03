# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Plotting support for our curves."""

import contextlib
import typing

import matplotlib.figure
import matplotlib.lines
import matplotlib.patches
import numpy
import numpy.typing


@contextlib.contextmanager
def tight_layout(
    axis_labels: tuple[str, str], title: str | None = None
) -> typing.Generator[
    tuple[matplotlib.figure.Figure, matplotlib.figure.Axes], None, None
]:
    """Generates a somewhat fancy canvas to draw ROC/DET-style curves.

    Works like a context manager, yielding a figure and an axes set in which
    the ROC curves should be added to.  Once the context is finished,
    :py:func:`matplotlib.pyplot.tight_layout()` is called.


    Parameters
    ----------
    axis_labels
        Labels for the x and y axes, in this order.
    title
        Optional title to add to this plot


    Yields
    ------
        A 2-tuple containing the following entries:

        * figure: The figure that should be finally returned to the user
        * axes: An axis set where to precision-recall plots should be added to
    """

    from matplotlib import pyplot

    fig, ax = pyplot.subplots(1)
    ax = typing.cast(matplotlib.figure.Axes, ax)

    # Names and bounds
    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.0])

    if title is not None:
        ax.set_title(title)

    ax.grid(linestyle="--", linewidth=1, color="gray", alpha=0.3)

    # we should see some of axes 1 axes
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_position(("data", -0.015))
    ax.spines["bottom"].set_position(("data", -0.015))

    # yield execution, lets user draw ROC plots, and the legend before
    # tighteneing the layout
    yield fig, ax  # type: ignore

    pyplot.tight_layout()


@contextlib.contextmanager
def tight_layout_f1iso(
    axis_labels: tuple[str, str], title: str | None = None
) -> typing.Generator[
    tuple[matplotlib.figure.Figure, matplotlib.figure.Axes], None, None
]:
    """Generates a somewhat fancy canvas to draw Precision-Recall-style curves.

    Works like a context manager, yielding a figure and an axes set in which
    the PR curves should be added to.  Once the context is finished,
    :py:func:`matplotlib.pyplot.tight_layout()` is called.

    The generated figure canvas contains F1-iso lines on the background.


    Parameters
    ----------
    axis_labels
        Labels for the x and y axes, in this order.
    title
        Optional title to add to this plot


    Yields
    ------
        A 2-tuple containing the following entries:

        * figure: The figure that should be finally returned to the user
        * axes: An axis set where to precision-recall plots should be added to
    """

    from matplotlib import pyplot

    with tight_layout(axis_labels=axis_labels, title=title) as (fig, ax):
        ax2 = ax.twinx()

        # Annotates plot with F1-score iso-lines
        f_scores = numpy.linspace(0.1, 0.9, num=9)
        tick_locs = []
        tick_labels = []
        for f_score in f_scores:
            x = numpy.linspace(0.01, 1)
            y = f_score * x / (2 * x - f_score)
            (_,) = pyplot.plot(x[y >= 0], y[y >= 0], color="green", alpha=0.1)
            tick_locs.append(y[-1])
            tick_labels.append("%.1f" % f_score)
        ax2.tick_params(axis="y", which="both", pad=0, right=False, left=False)
        ax2.set_ylabel("iso-F", color="green", alpha=0.3)
        ax2.set_ylim([0.0, 1.0])
        ax2.yaxis.set_label_coords(1.015, 0.97)
        ax2.set_yticks(tick_locs)  # notice these are invisible
        for k in ax2.set_yticklabels(tick_labels):
            k.set_color("green")
            k.set_alpha(0.3)
            k.set_size(8)

        # we shouldn't see any of axes 2 axes
        ax2.spines["right"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)

        # yield execution, lets user draw precision-recall plots, and the legend
        # before tighteneing the layout
        yield fig, ax  # type: ignore


def curve_ci(
    curve: tuple[
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
    ],
    lower: tuple[
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
    ],
    upper: tuple[
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
        typing.Sequence[float] | numpy.typing.NDArray[numpy.double],
    ],
    alpha_multiplier: float = 0.3,
    **kwargs,
) -> tuple[matplotlib.lines.Line2D, matplotlib.patches.Polygon]:
    """Plots the ROC curve with confidence interval bounds.

    This method will call ``matplotlib`` to plot the ROC curve for a system
    which contains a particular set of negatives and positives scores,
    including its credible/confidence interval bounds. We use the standard
    :py:func:`matplotlib.pyplot.plot` command. All parameters passed with
    exception of the three first parameters of this method will be directly
    passed to the plot command.

    .. note::

      This function does not initiate and save the figure instance, it only
      issues the plotting command. You are the responsible for setting up and
      saving the figure as you see fit.


    Parameters
    ----------
    curve
        Tuple with two floating point array-like structures that define the
        first (x; horizontal) and second (y; vertical) coordinates to be
        plotted.
    lower
        Tuple with two floating point array-like structures that define the
        first (x; horizontal) and second (y; vertical) coordinates of the lower
        bounding confidence curve (after hull expansion) of ``curve``.
    upper
        Tuple with two floating point array-like structures that define the
        first (x; horizontal) and second (y; vertical) coordinates of the upper
        bounding confidence curve (after hull expansion) of ``curve``.
    alpha_multiplier
        A value between 0.0 and 1.0 to express the amount of transparence to be
        applied to the confidence/credible margins.  This will be used to
        multiply the ``alpha`` channel of the line itself.  If the default is
        unchanged, then this is the value of the alpha channel on the margins.
    **kwargs
        Extra plotting parameters, which are passed directly to
        :py:func:`matplotlib.pyplot.plot`.


    Returns
    -------
        A 2-tuple with the line and fill objects drawing the curve.
    """

    from matplotlib import pyplot

    (line,) = pyplot.plot(curve[0], curve[1], **kwargs)
    color = line.get_color()
    alpha = (
        alpha_multiplier
        if line.get_alpha() is None
        else alpha_multiplier * line.get_alpha()
    )
    (fill,) = pyplot.fill(
        # we concatenate the points so that the formed polygon
        # is structurally coherent (vertices are in the right order)
        numpy.append(upper[0], lower[0][::-1]),
        numpy.append(upper[1], lower[1][::-1]),
        # we use the color/alpha from user settings
        color=color,
        alpha=alpha,
    )
    return (line, fill)
