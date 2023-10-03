# SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from matplotlib import pyplot as plt

import credible.bayesian.functors
import credible.curves
import credible.frequentist.functors

samples = 100  # number of samples simulated
coverage = 0.95

flat = credible.curves.estimated_ci_coverage(
    credible.bayesian.functors.bayesian_flat_array, n=samples
)
bj = credible.curves.estimated_ci_coverage(
    credible.bayesian.functors.bayesian_jeffreys_array, n=samples
)
cp = credible.curves.estimated_ci_coverage(
    credible.frequentist.functors.clopper_pearson_array, n=samples
)
ac = credible.curves.estimated_ci_coverage(
    credible.frequentist.functors.agresti_coull_array, n=samples
)
wi = credible.curves.estimated_ci_coverage(
    credible.frequentist.functors.wilson_array, n=samples
)

plt.plot(wi[0], 100 * wi[1], color="black", label="CI: Wilson (1927)")
plt.plot(cp[0], 100 * cp[1], color="orange", label="CI: Clopper-Pearson (1934)")
plt.plot(ac[0], 100 * ac[1], color="purple", label="CI: Agresti-Coull (1998)")
plt.plot(
    flat[0], 100 * flat[1], color="blue", label="CR: Beta + Flat Prior (2005)"
)
plt.plot(
    bj[0], 100 * bj[1], color="green", label="CR: Beta + Jeffreys Prior (2005)"
)

# Styling
plt.ylabel(f"Coverage for {100*coverage:.0f}% CR/CI")
plt.xlabel("Success rate (p)")
plt.title(f"Estimated coverage n={samples}")
plt.ylim([75, 100])
plt.hlines(100 * coverage, bj[0][0], bj[0][-1], color="red", linestyle="dashed")
plt.grid()
plt.legend()
plt.show()
