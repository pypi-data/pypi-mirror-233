.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _credible:

===========================================================
 Scikit-Learn compatible metrics with confidence intervals
===========================================================

This library contains implementations of some scikit-learn metrics with
credible (or confidence) intervals. A `Credible Interval <credible-interval_>`_
or region (for multi-dimensional cases) for parameter :math:`x` consists of a
lower estimate :math:`L`, and an upper estimate :math:`U`, such that the
probability of the true value being within the interval estimate is equal to an
arbitrary :math:`\alpha` (:math:`0 < \alpha < 1`, typically 0.95).


Documentation
-------------

.. toctree::
   :maxdepth: 2

   install
   ci
   api
   references


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. include:: links.rst
