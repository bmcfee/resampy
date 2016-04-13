#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Filter construction and loading'''

import scipy.signal
import numpy as np
import six
import sys

FILTER_FUNCTIONS = ['sinc_window']


def sinc_window(num_zeros=69, precision=9, window=None, rolloff=0.95):
    '''Construct a windowed sinc interpolation filter

    Parameters
    ----------
    num_zeros : int > 0
        The number of zero-crossings to retain in the sinc filter

    precision : int > 0
        The number of filter coefficients to retain for each zero-crossing

    window : callable
        The window function

    rolloff : float > 0
        The roll-off frequency (as a fraction of nyquist)

    Returns
    -------
    interp_window: np.ndarray [shape=(num_zeros * num_table + 1)]
        The interpolation window (right-hand side)

    num_bits: int
        The number of bits of precision to use in the filter table

    Raises
    ------
    TypeError
        if `window` is not callable or `None`
    ValueError
        if `num_zeros < 1`, `precision < 1`,
        or `rolloff` is outside the range `(0, 1]`.

    '''

    if window is None:
        window = scipy.signal.hann
    elif not six.callable(window):
        raise TypeError('window must be callable, not type(window)={}'.format(type(window)))

    if not 0 < rolloff <= 1:
        raise ValueError('Invalid roll-off: rolloff={}'.format(rolloff))

    if num_zeros < 1:
        raise ValueError('Invalid num_zeros: num_zeros={}'.format(num_zeros))

    if precision < 1:
        raise ValueError('Invalid precision: precision={}'.format(precision))

    # Generate the right-wing of the sinc
    num_bits = 2**precision
    n = num_bits * num_zeros
    sinc_win = rolloff * np.sinc(rolloff * np.linspace(0, num_zeros, num=n + 1,
                                                       endpoint=True))

    # Build the window function and cut off the left half
    taper = window(2 * n + 1)[n:]

    interp_win = (taper * sinc_win)

    return interp_win, num_bits


def get_filter(name_or_function, **kwargs):
    '''Retrieve a window given its name or function handle.

    Parameters
    ----------
    name_or_function : str or callable
        If a string
    '''
    if name_or_function in FILTER_FUNCTIONS:
        return getattr(sys.modules[__name__], name_or_function)(**kwargs)
    elif six.callable(name_or_function):
        return name_or_function(**kwargs)
    else:
        # TODO: load pre-computed filter from disk
        raise NotImplementedError(name_or_function)
