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


@pytest.mark.parametrize('axis', [0, 1, 2])
def test_resample_nu_shape(axis):
    sr_orig = 100
    sr_new = sr_orig // 2
    X = np.random.randn(sr_orig, sr_orig, sr_orig)
    t = np.arange(X.shape[axis] // 2) / sr_new
    Y = resampy.resample_nu(X, sr_orig, t, axis=axis)

    target_shape = list(X.shape)
    target_shape[axis] = len(t)

    assert target_shape == list(Y.shape)


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('sr_orig, sr_new', [(100, 0), (100, -1), (0, 100), (-1, 100)])
def test_bad_sr(sr_orig, sr_new):
    x = np.zeros(100)
    resampy.resample(x, sr_orig, sr_new)


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('sr', [0, -1])
def test_bad_sr_nu(sr):
    x = np.zeros(100)
    t = np.arange(3)
    resampy.resample_nu(x, sr, t)


@pytest.mark.xfail(raises=ValueError, strict=True)
@pytest.mark.parametrize('t', [np.empty(0), np.eye(3)])
def test_bad_time_nu(t):
    x = np.zeros(100)
    resampy.resample_nu(x, 1, t)


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
                                   np.complex64, np.complex128])
def test_dtype(dtype):
    x = np.random.randn(100).astype(dtype)

    y = resampy.resample(x, 100, 200)

    assert x.dtype == y.dtype


@pytest.mark.parametrize('dtype', [np.int16, np.int32, np.int64])
def test_dtype_int(dtype):
    x = (32767 * np.random.randn(100)).astype(dtype)

    y = resampy.resample(x, 100, 200)

    assert y.dtype == np.float32


@pytest.mark.parametrize('dtype', [np.int16, np.int32, np.int64])
def test_dtype_int_nu(dtype):
    x = (32767 * np.random.randn(100)).astype(dtype)
    t = np.arange(2 * len(x) - 1) / 2

    y = resampy.resample_nu(x, 1., t)
    assert y.dtype == np.float32


@pytest.mark.parametrize('dtype', [np.float32, np.float64,
                                   np.complex64, np.complex128])
def test_resample_nu_dtype(dtype):
    x = np.random.randn(100).astype(dtype)
    t = np.arange(2 * len(x) - 1) / 2

    y = resampy.resample_nu(x, 1., t)

    assert x.dtype == y.dtype


@pytest.mark.xfail(raises=TypeError)
def test_bad_window():
    x = np.zeros(100)

    resampy.resample(x, 100, 200, filter='sinc_window', window=np.ones(50))


@pytest.mark.xfail(raises=ValueError)
def test_short_signal():

    x = np.zeros(2)
    resampy.resample(x, 4, 1)


@pytest.mark.xfail(raises=ValueError)
def test_resample_nu_short_signal():

    x = np.zeros(2)
    t = np.asarray([])
    resampy.resample_nu(x, 1., t)


def test_good_window():
    sr_orig = 100
    sr_new = 200
    x = np.random.randn(500)
    y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window', window=scipy.signal.windows.blackman)

    assert len(y) == 2 * len(x)


@pytest.mark.parametrize('order', ['C', 'F'])
@pytest.mark.parametrize('shape', [(50,), (10, 50), (10, 25, 50)])
@pytest.mark.parametrize('axis', [0, -1])
def test_contiguity(order, shape, axis):

    x = np.zeros(shape, dtype=np.float64, order=order)
    sr_orig = 1
    sr_new = 2
    y = resampy.resample(x, sr_orig, sr_new, axis=axis)

    assert x.flags['C_CONTIGUOUS'] == y.flags['C_CONTIGUOUS']
    assert x.flags['F_CONTIGUOUS'] == y.flags['F_CONTIGUOUS']


@pytest.mark.parametrize('order', ['C', 'F'])
@pytest.mark.parametrize('shape', [(50,), (10, 50), (10, 25, 50)])
@pytest.mark.parametrize('axis', [0, -1])
def test_resample_nu_contiguity(order, shape, axis):

    x = np.zeros(shape, dtype=np.float64, order=order)
    t = np.arange(x.shape[axis] * 2 - 1) / 2
    y = resampy.resample_nu(x, 1., t, axis=axis)

    assert x.flags['C_CONTIGUOUS'] == y.flags['C_CONTIGUOUS']
    assert x.flags['F_CONTIGUOUS'] == y.flags['F_CONTIGUOUS']


@pytest.mark.xfail(raises=ValueError)
@pytest.mark.parametrize('shape', [(50,), (10, 50), (10, 25, 50)])
@pytest.mark.parametrize('axis', [0, -1])
@pytest.mark.parametrize('domain', [(0, 100), (-1, 5)])
def test_resample_nu_domain(shape, axis, domain):

    x = np.zeros(shape, dtype=np.float64)
    t = np.linspace(*domain, num=10, endpoint=True)
    resampy.resample_nu(x, 1., t, axis=axis)


def test_resample_matched():
    x = np.random.randn(100)
    y = resampy.resample(x, 1, 1)

    # All values should match
    assert np.allclose(x, y)
    # y should own the data
    assert y.flags['OWNDATA']
    # x and y are distinct objects
    assert y is not x


def test_resample_axis():
    # derived from https://github.com/bmcfee/resampy/issues/73

    rand_arr = np.abs(np.random.rand(3, 4, 5, 100))

    resampled_arr = resampy.resample(rand_arr, 100, 24, axis=3)

    resampled_t_arr = resampy.resample(np.transpose(rand_arr), 100, 24, axis=0)

    assert np.allclose(resampled_arr, np.transpose(resampled_t_arr))
    assert (resampled_arr**2).sum() > 0


def test_resample_length_rounding():
    # Test for length calculation edge case https://github.com/bmcfee/resampy/issues/111
    x = np.zeros(12499)
    y = resampy.resample(x, 12499, 15001)
    assert len(y) == 15001


def test_resample_rates_fixedprecision():
    # Test for avoiding ill effects of fixed-precision math
    # This should fix a bug in librosa https://github.com/librosa/librosa/issues/1569

    x = np.zeros(720200)
    sr_out = np.int32(4000)
    sr_in = 22050
    resampy.resample(x, sr_in, sr_out)
