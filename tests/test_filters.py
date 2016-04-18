#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import scipy
import resampy

from nose.tools import eq_, raises

def test_filter_sinc():

    def __test(filt, window, num_zeros, precision, rolloff):

        kwargs = dict()
        if window is not None:
            kwargs['window'] = window

        if num_zeros is not None:
            kwargs['num_zeros'] = num_zeros

        if precision is not None:
            kwargs['precision'] = precision

        if rolloff is not None:
            kwargs['rolloff'] = rolloff

        interp, prec = resampy.filters.get_filter(filt, **kwargs)

        if precision in kwargs:
            eq_(2**precision, prec)

    for filt in ['sinc_window', resampy.filters.sinc_window]:
        for window in [None, scipy.signal.hann]:
            for num_zeros in [None, 13]:
                for precision in [None, 9]:
                    for rolloff in [None, 0.925]:
                        yield __test, filt, window, num_zeros, precision, rolloff


def test_filter_load():
    half_win, precision = resampy.filters.get_filter('kaiser_best')

@raises(IOError)
def test_filter_missing():
    resampy.filters.get_filter('bad name')
