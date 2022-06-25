#!/usr/bin/env python
'''Numba implementation of resampler'''

import numba


def _resample_f(x, y, t_out, interp_win, interp_delta, num_table, scale=1.0):

    index_step = int(scale * num_table)
    time_register = 0.0

    n = 0
    frac = 0.0
    index_frac = 0.0
    offset = 0
    eta = 0.0
    weight = 0.0

    nwin = interp_win.shape[0]
    n_orig = x.shape[0]
    n_out = t_out.shape[0]

    for t in numba.prange(n_out):
        time_register = t_out[t]

        # Grab the top bits as an index to the input buffer
        n = int(time_register)

        # Grab the fractional component of the time index
        frac = scale * (time_register - n)

        # Offset into the filter
        index_frac = frac * num_table
        offset = int(index_frac)

        # Interpolation factor
        eta = index_frac - offset

        # Compute the left wing of the filter response
        i_max = min(n + 1, (nwin - offset) // index_step)
        for i in range(i_max):

            weight = (interp_win[offset + i * index_step] + eta * interp_delta[offset + i * index_step])
            y[t] += weight * x[n-i]

        # Invert P
        frac = scale - frac

        # Offset into the filter
        index_frac = frac * num_table
        offset = int(index_frac)

        # Interpolation factor
        eta = index_frac - offset

        # Compute the right wing of the filter response
        k_max = min(n_orig - n - 1, (nwin - offset) // index_step)
        for k in range(k_max):
            weight = (interp_win[offset + k * index_step] + eta * interp_delta[offset + k * index_step])
            y[t] += weight * x[n + k + 1]

resample_f_p = numba.jit(nopython=True, nogil=True, parallel=True)(_resample_f)
resample_f_s = numba.jit(nopython=True, nogil=True, parallel=False)(_resample_f)
