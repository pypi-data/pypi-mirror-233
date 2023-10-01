from __future__ import annotations

import numpy as np
from numba import float32, float64

from utilities._numbagg.decorators import ndmovingexp


@ndmovingexp(
    [(float32[:], float32, float32[:]), (float64[:], float64, float64[:])]
)
def move_exp_nanmean(a, alpha, out):
    # Inspired by pandas:
    # https://github.com/pandas-dev/pandas/blob/1.2.x/pandas/_libs/window/aggregations.pyx#L1559.

    N = len(a)
    if N == 0:
        return

    old_wt_factor = 1.0 - alpha
    new_wt = 1.0
    ignore_na = False  # could add as option in the future

    weighted_avg = np.nan
    n_obs = 0
    old_wt = 1.0

    for i in range(N):
        cur = a[i]
        is_observation = not np.isnan(cur)
        n_obs += int(is_observation)
        if not np.isnan(weighted_avg):
            if is_observation or (not ignore_na):
                old_wt *= old_wt_factor

                if is_observation:
                    # avoid numerical errors on constant series
                    if weighted_avg != cur:
                        weighted_avg = (
                            (old_wt * weighted_avg) + (new_wt * cur)
                        ) / (old_wt + new_wt)
                    old_wt += new_wt
        elif is_observation:
            # The first non-nan value.
            weighted_avg = cur

        out[i] = weighted_avg


@ndmovingexp(
    [(float32[:], float32, float32[:]), (float64[:], float64, float64[:])]
)
def move_exp_nansum(a, alpha, out):
    """
    Calculates the exponentially decayed sum.
    Very similar to move_exp_nanmean, but calculates a decayed sum rather than the mean.
    """

    # As per https://github.com/numbagg/numbagg/issues/26#issuecomment-830437132, we
    # could try implementing this with a bool flag on the same function as
    # `move_exp_nanmean` and hope that numba optimizes it away. The code here is
    # basically a subset of that function.

    N = len(a)
    if N == 0:
        return

    weight = 1.0 - alpha
    ignore_na = False  # could add as option in the future
    weighted_sum = 0

    for i in range(N):
        cur = a[i]
        is_observation = not np.isnan(cur)
        if not np.isnan(weighted_sum):
            if is_observation or (not ignore_na):
                weighted_sum = weight * weighted_sum
                if is_observation:
                    weighted_sum += cur
        elif is_observation:
            # The first non-nan value.
            weighted_sum = cur

        out[i] = weighted_sum
