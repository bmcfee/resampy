#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import scipy.signal
import pytest

import resampy


@pytest.mark.parametrize('axis', [0, 1, 2])
def test_shape(axis):
    sr_orig = 100
    sr_new = sr_orig // 2
    X = np.random.randn(sr_orig, sr_orig, sr_orig)
    Y = resampy.resample(X, sr_orig, sr_new, axis=axis)

    target_shape = list(X.shape)
    target_shape[axis] = target_shape[axis] * sr_new // sr_orig

    assert target_shape == list(Y.shape)


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('sr_orig, sr_new', [(100, 0), (100, -1), (0, 100), (-1, 100)])
def test_bad_sr(sr_orig, sr_new):
    x = np.zeros(100)
    resampy.resample(x, sr_orig, sr_new)


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('rolloff', [-1, 1.5])
def test_bad_rolloff(rolloff):
    x = np.zeros(100)
    resampy.resample(x, 100, 50, filter='sinc_window', rolloff=rolloff)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_bad_precision():
    x = np.zeros(100)
    resampy.resample(x, 100, 50, filter='sinc_window', precision=-1)


@pytest.mark.xfail(raises=ValueError, strict=True)
def test_bad_num_zeros():
    x = np.zeros(100)
    resampy.resample(x, 100, 50, filter='sinc_window', num_zeros=0)


@pytest.mark.parametrize('dtype', [np.float32, np.float64,
                                   np.int16, np.int32, np.int64])
def test_dtype(dtype):
    x = np.random.randn(100).astype(dtype)

    if np.issubdtype(dtype, np.float):
        y = resampy.resample(x, 100, 200)

        assert x.dtype == y.dtype
    else:
        with pytest.raises(TypeError):
            y = resampy.resample(x, 100, 200)


@pytest.mark.xfail(raises=TypeError)
def test_bad_window():
    x = np.zeros(100)

    resampy.resample(x, 100, 200, filter='sinc_window', window=np.ones(50))


@pytest.mark.xfail(raises=ValueError)
def test_short_signal():

    x = np.zeros(2)
    resampy.resample(x, 4, 1)


def test_good_window():
    sr_orig = 100
    sr_new = 200
    x = np.random.randn(500)
    y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window', window=scipy.signal.blackman)

    assert len(y) == 2 * len(x)
