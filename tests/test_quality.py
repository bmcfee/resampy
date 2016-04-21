#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import pytest

import resampy


def make_tone(freq, sr, duration):
    return np.sin(2 * np.pi * freq / sr * np.arange(sr * duration))


def make_sweep(freq, sr, duration):
    return np.sin(np.cumsum(2 * np.pi * np.logspace(np.log2(2.0 / sr),
                                                    np.log2(float(freq) / sr),
                                                    num=duration*sr, base=2.0)))


@pytest.mark.parametrize('sr_orig,sr_new', [(44100, 22050), (22050, 44100)])
@pytest.mark.parametrize(
    'fil,rms',
    [('sinc_window', 1e-6), ('kaiser_fast', 1e-4), ('kaiser_best', 1e-7)]
)
def test_quality_sine(sr_orig, sr_new, fil, rms):
    FREQ = 512.0
    DURATION = 2.0

    x = make_tone(FREQ, sr_orig, DURATION)
    y = make_tone(FREQ, sr_new, DURATION)
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
    x = make_sweep(FREQ, sr_orig, DURATION)
    y = make_sweep(FREQ, sr_new, DURATION)

    y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

    idx = slice(sr_new // 2, - sr_new//2)

    err = np.mean(np.abs(y[idx] - y_pred[idx]))
    assert err <= rms, '{:g} > {:g}'.format(err, rms)
