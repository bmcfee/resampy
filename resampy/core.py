#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Core resampling interface'''

import numpy as np

from .filters import get_filter
from .resample import resample_f

__all__ = ['resample']


def resample(x, sr_orig, sr_new, axis=-1, filter='sinc_window', **kwargs):
    '''Resample a signal x from sr_orig to sr_new along a given axis.

    Parameters
    ----------
    x : np.ndarray
        The input signal(s) to resample

    sr_orig : int > 0
        The sampling rate of x

    sr_new : int > 0
        The target sampling rate of the output signal(s)

    axis : int
        The target axis along which to resample `x`

    filter : optional, str or callable
        The resampling filter to use.

    kwargs
        additional keyword arguments provided to the specified filter

    Returns
    -------
    y : np.ndarray
        `x` resampled to `sr_new`

    Raises
    ------
    ValueError
        if `sr_orig` or `sr_new` is not positive
    '''

    if sr_orig <= 0:
        raise ValueError('Invalid sample rate: sr_orig={}'.format(sr_orig))

    if sr_new <= 0:
        raise ValueError('Invalid sample rate: sr_new={}'.format(sr_new))

    sample_ratio = float(sr_new) / sr_orig

    # Set up the output shape
    shape = list(x.shape)
    shape[axis] = int(shape[axis] * sample_ratio)

    y = np.zeros(shape, dtype=x.dtype)

    interp_win, precision = get_filter(filter, **kwargs)

    if sample_ratio < 1:
        interp_win *= sample_ratio

    interp_delta = np.zeros_like(interp_win)
    interp_delta[:-1] = np.diff(interp_win)

    # Construct 2d views of the data with the resampling axis on the first dimension
    x_2d = x.swapaxes(0, axis).reshape((x.shape[axis], -1))
    y_2d = y.swapaxes(0, axis).reshape((y.shape[axis], -1))
    resample_f(x_2d, y_2d, sample_ratio, interp_win, interp_delta, precision)

    return y
