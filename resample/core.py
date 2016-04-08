#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Core resampling interface'''

import scipy
import numpy as np
import six

from .resample import resample_f

def make_window(num_zeros, num_table, window, sr_orig, sr_new, rolloff=0.95):
    '''Construct the interpolation window'''

    # Generate the right-wing of the sinc
    scale = min(sr_orig, sr_new) / float(sr_orig)

    n = num_table * num_zeros
    sinc_win = rolloff * np.sinc(rolloff * np.linspace(0, num_zeros, num=n + 1,
                                                       endpoint=True))

    # Build the window function and cut off the left half
    taper = scale * window(2 * n + 1)[n:]

    interp_win = (taper * sinc_win).astype(np.float32)

    return interp_win


def resample(x, sr_orig, sr_new, num_zeros=13, precision=9, window=None, axis=-1):
    '''Resample a signal x
    '''
    if window is None:
        window = scipy.signal.blackmanharris
    elif not six.callable(window):
        raise TypeError('window must be callable, not type(window)={}'.format(type(window)))

    sample_ratio = float(sr_new) / sr_orig

    # Set up the output shape
    shape = list(x.shape)
    shape[axis] = int(shape[axis] * sample_ratio)

    y = np.zeros(shape, dtype=x.dtype)

    num_table = 2**precision
    interp_win = make_window(num_zeros, num_table, window, sr_orig, sr_new)

    interp_delta = np.zeros_like(interp_win)
    interp_delta[:-1] = np.diff(interp_win)

    # Construct 2d views of the data with the resampling axis on the first dimension
    x_2d = x.swapaxes(0, axis).reshape((x.shape[axis], -1))
    y_2d = y.swapaxes(0, axis).reshape((y.shape[axis], -1))
    resample_f(x_2d, y_2d, sample_ratio, interp_win, interp_delta, num_table)

    return y
