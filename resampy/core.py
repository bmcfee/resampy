#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Core resampling interface'''

import scipy.signal
import numpy as np
import six

from .resample import resample_f

__all__ = ['resample']


def make_window(num_zeros, num_table, window, rolloff):
    '''Construct the interpolation window
    
    Parameters
    ----------
    num_zeros : int > 0
        The number of zero-crossings to retain in the sinc filter

    num_table : int > 0
        The number of filter coefficients to retain for each zero-crossing

    window : callable
        The window function

    rolloff : float > 0
        The roll-off frequency (as a fraction of nyquist)

    Returns
    -------
    interp_window: np.ndarray [shape=(num_zeros * num_table + 1)]
        The interpolation window (right-hand side)
    '''

    # Generate the right-wing of the sinc
    n = num_table * num_zeros
    sinc_win = rolloff * np.sinc(rolloff * np.linspace(0, num_zeros, num=n + 1,
                                                       endpoint=True))

    # Build the window function and cut off the left half
    taper = window(2 * n + 1)[n:]

    interp_win = (taper * sinc_win)

    return interp_win


def resample(x, sr_orig, sr_new, num_zeros=69, precision=9, window=None, rolloff=0.95, axis=-1):
    '''Resample a signal x

    Parameters
    ----------
    x : np.ndarray
        The input signal(s) to resample

    sr_orig : int > 0
        The sampling rate of x

    sr_new : int > 0
        The target sampling rate of the output signal(s)

    num_zeros : int > 0
        Number of zero-crossings to use in the low-pass filter.
        Larger values give higher accuracy, but increase running time.

    precision : int > 0
        Number of bits to use for the filter table index.

    window : callable or None
        A window function to taper the low-pass filter.
        By default, uses `scipy.signal.hann`.

        .. seealso:: scipy.signal

    rolloff : float in (0, 1]
        The roll-off frequency as a fraction of nyquist

    axis : int
        The target axis along which to resample `x`

    Returns
    -------
    y : np.ndarray
        `x` resampled to `sr_new`

    Raises
    ------
    TypeError
        if `window` is not callable or `None`

    ValueError
        if `sr_orig` or `sr_new` is not positive
    '''
    if window is None:
        window = scipy.signal.hann

    elif not six.callable(window):
        raise TypeError('window must be callable, not type(window)={}'.format(type(window)))

    if sr_orig <= 0:
        raise ValueError('Invalid sample rate: sr_orig={}'.format(sr_orig))

    if sr_new <= 0:
        raise ValueError('Invalid sample rate: sr_new={}'.format(sr_new))

    if not 0 < rolloff <= 1:
        raise ValueError('Invalid roll-off: rolloff={}'.format(rolloff))

    if num_zeros < 1:
        raise ValueError('Invalid num_zeros: num_zeros={}'.format(num_zeros))

    if precision < 1:
        raise ValueError('Invalid precision: precision={}'.format(precision))

    sample_ratio = float(sr_new) / sr_orig

    # Set up the output shape
    shape = list(x.shape)
    shape[axis] = int(shape[axis] * sample_ratio)

    y = np.zeros(shape, dtype=x.dtype)

    num_table = 2**precision
    interp_win = min(sample_ratio, 1.0) * make_window(num_zeros, num_table, window, rolloff)

    interp_delta = np.zeros_like(interp_win)
    interp_delta[:-1] = np.diff(interp_win)

    # Construct 2d views of the data with the resampling axis on the first dimension
    x_2d = x.swapaxes(0, axis).reshape((x.shape[axis], -1))
    y_2d = y.swapaxes(0, axis).reshape((y.shape[axis], -1))
    resample_f(x_2d, y_2d, sample_ratio, interp_win, interp_delta, num_table)

    return y
