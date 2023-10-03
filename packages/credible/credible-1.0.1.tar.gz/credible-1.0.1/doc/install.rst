.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _credible.install:

==============
 Installation
==============

We support two installation modes, through pip_, or mamba_ (conda).


.. tab:: pip

   Stable, from PyPI:

   .. code:: sh

      pip install credible

   Latest beta, from GitLab package registry:

   .. code:: sh

      pip install --pre --index-url https://gitlab.idiap.ch/api/v4/groups/software/-/packages/pypi/simple --extra-index-url https://pypi.org/simple credible

   .. tip::

      To avoid long command-lines you may configure pip to define the indexes and
      package search priorities as you like.


.. tab:: mamba/conda

   Stable:

   .. code:: sh

      mamba install -c conda-forge credible

   Latest beta:

   .. code:: sh

      mamba install -c https://www.idiap.ch/software/biosignal/conda/label/beta -c conda-forge credible


.. include:: links.rst
