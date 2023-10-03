# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Functors with standard confidence interval parameterisation."""

import functools

from ..utils import CIArrayFunctor, CIFunctor
from . import utils

clopper_pearson: CIFunctor = functools.partial(
    utils.clopper_pearson, coverage=0.95
)
clopper_pearson_array: CIArrayFunctor = functools.partial(
    utils._clopper_pearson_array, coverage=0.95
)

agresti_coull: CIFunctor = functools.partial(utils.agresti_coull, coverage=0.95)
agresti_coull_array: CIArrayFunctor = functools.partial(
    utils._agresti_coull_array, coverage=0.95
)

wilson: CIFunctor = functools.partial(utils.wilson, coverage=0.95)
wilson_array: CIArrayFunctor = functools.partial(
    utils._wilson_array, coverage=0.95
)
