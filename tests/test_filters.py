#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import scipy
import pytest

import resampy


@pytest.mark.parametrize('filt', ['sinc_window', resampy.filters.sinc_window])
@pytest.mark.parametrize('window', [None, scipy.signal.windows.hann])
@pytest.mark.parametrize('num_zeros', [None, 13])
@pytest.mark.parametrize('precision', [None, 9])
@pytest.mark.parametrize('rolloff', [None, 0.925])
def test_filter_sinc(filt, window, num_zeros, precision, rolloff):
    kwargs = dict()
    if window is not None:
        kwargs['window'] = window

    if num_zeros is not None:
        kwargs['num_zeros'] = num_zeros

    if precision is not None:
        kwargs['precision'] = precision

    if rolloff is not None:
        kwargs['rolloff'] = rolloff

    interp, prec, _ = resampy.filters.get_filter(filt, **kwargs)

    if precision in kwargs:
        assert 2**precision == prec


def test_filter_load():
    half_win, precision, _ = resampy.filters.get_filter('kaiser_best')


@pytest.mark.xfail(raises=NotImplementedError, strict=True)
def test_filter_missing():
    resampy.filters.get_filter('bad name')


@pytest.mark.parametrize('sr1, sr2', [(1, 2), (2, 1)])
def test_filter_cache_reset(sr1, sr2):
    x = np.random.randn(100)
    y1 = resampy.resample(x, sr1, sr2, filter='kaiser_fast')

    assert len(resampy.filters.FILTER_CACHE) > 0

    resampy.filters.clear_cache()

    assert len(resampy.filters.FILTER_CACHE) == 0

    y2 = resampy.resample(x, sr1, sr2, filter='kaiser_fast')

    assert np.allclose(y1, y2)
