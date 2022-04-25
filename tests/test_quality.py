#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import pytest

import resampy


def make_tone(freq, sr, duration):
    t = np.arange(int(sr * duration)) / sr
    return np.sin(2 * np.pi * freq * t), t


def make_sweep(freq, sr, duration):
    t = np.linspace(1, np.log2(float(freq)), num=int(duration*sr), endpoint=True)
    return np.sin(np.cumsum(2 * np.pi * 2**(t - np.log2(sr)))), t


@pytest.mark.parametrize('sr_orig,sr_new', [(44100, 22050), (22050, 44100)])
@pytest.mark.parametrize(
    'fil,rms',
    [('sinc_window', 1e-6), ('kaiser_fast', 1e-4), ('kaiser_best', 1e-7)]
)
def test_quality_sine(sr_orig, sr_new, fil, rms):
    FREQ = 512.0
    DURATION = 2.0

    x, _ = make_tone(FREQ, sr_orig, DURATION)
    y, _ = make_tone(FREQ, sr_new, DURATION)
    y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

    idx = slice(sr_new // 2, - sr_new//2)

    err = np.mean(np.abs(y[idx] - y_pred[idx]))
    assert err <= rms, '{:g} > {:g}'.format(err, rms)


@pytest.mark.parametrize('sr_orig,sr_new', [(44100, 22050), (22050, 44100)])
@pytest.mark.parametrize(
    'fil,rms',
    [('sinc_window', 1e-1), ('kaiser_fast', 1e-1), ('kaiser_best', 1e-1)]
)
def test_quality_sweep(sr_orig, sr_new, fil, rms):
    FREQ = 8192
    DURATION = 5.0
    x, _ = make_sweep(FREQ, sr_orig, DURATION)
    y, _ = make_sweep(FREQ, sr_new, DURATION)

    y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

    idx = slice(sr_new // 2, - sr_new//2)

    err = np.mean(np.abs(y[idx] - y_pred[idx]))
    assert err <= rms, '{:g} > {:g}'.format(err, rms)


@pytest.mark.parametrize('sr_orig,sr_new', [(44100, 22050), (22050, 44100)])
@pytest.mark.parametrize(
    'fil,rms',
    [('sinc_window', 1e-6), ('kaiser_fast', 1e-4), ('kaiser_best', 1e-7)]
)
def test_resample_nu_quality_sine(sr_orig, sr_new, fil, rms):
    FREQ = 512.0
    DURATION = 2.0

    x, t_in = make_tone(FREQ, sr_orig, DURATION)
    y, t_out = make_tone(FREQ, sr_new, DURATION)

    dt = t_in[1] - t_in[0]
    t = (t_out - t_in[0]) / dt

    y_pred = resampy.resample_nu(x, t[:-1], filter=fil)

    idx = slice(sr_new // 2, - sr_new//2)

    err = np.mean(np.abs(y[:-1][idx] - y_pred[idx]))
    assert err <= rms, '{:g} > {:g}'.format(err, rms)


@pytest.mark.parametrize('sr_orig,sr_new', [(44100, 22050), (22050, 44100)])
@pytest.mark.parametrize(
    'fil,rms',
    [('sinc_window', 1e-1), ('kaiser_fast', 1e-1), ('kaiser_best', 1e-1)]
)
def test_resample_nu_quality_sweep(sr_orig, sr_new, fil, rms):
    FREQ = 8192
    DURATION = 5.0
    x, t_in = make_sweep(FREQ, sr_orig, DURATION)
    y, t_out = make_sweep(FREQ, sr_new, DURATION)

    dt = t_in[1] - t_in[0]
    t = (t_out - t_in[0]) / dt

    y_pred = resampy.resample_nu(x, t[:-1], filter=fil)

    idx = slice(sr_new // 2, - sr_new//2)

    err = np.mean(np.abs(y[:-1][idx] - y_pred[idx]))
    assert err <= rms, '{:g} > {:g}'.format(err, rms)
