#!/usr/bin/env python

import numpy as np

import resampy

from nose.tools import raises

def make_tone(freq, sr, duration):
    return np.sin(2 * np.pi * freq / sr * np.arange(sr * duration))


def make_sweep(freq, sr, duration):
    
    return np.sin(np.cumsum(2 * np.pi * np.logspace(np.log2(2.0 / sr),
                                                    np.log2(freq / sr),
                                                    num=duration*sr, base=2.0)))

def test_quality_sine():

    def __test(sr_orig, sr_new, fil, rms, x, y):

        y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

        idx = slice(sr_new // 2, - sr_new//2)

        err = np.mean(np.abs(y[idx] - y_pred[idx]))
        assert err <= rms, '{:g} > {:g}'.format(err, rms)

    FREQ = 512.0
    DURATION = 2.0

    for (sr_orig, sr_new) in [ (44100, 22050), (22050, 44100) ]:
        x = make_tone(FREQ, sr_orig, DURATION)
        y = make_tone(FREQ, sr_new, DURATION)

        for (fil, rms) in [('sinc_window', 1e-6),
                           ('kaiser_fast', 1e-4),
                           ('kaiser_best', 1e-7)]:
            yield __test, sr_orig, sr_new, fil, rms, x, y

def test_quality_sweep():

    def __test(sr_orig, sr_new, fil, rms, x, y):

        y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

        idx = slice(sr_new // 2, - sr_new//2)

        err = np.mean(np.abs(y[idx] - y_pred[idx]))
        assert err <= rms, '{:g} > {:g}'.format(err, rms)

    FREQ = 8192
    DURATION = 5.0

    for (sr_orig, sr_new) in [ (44100, 22050), (22050, 44100) ]:
        x = make_sweep(FREQ, sr_orig, DURATION)
        y = make_sweep(FREQ, sr_new, DURATION)

        for (fil, rms) in [('sinc_window', 1e-1),
                           ('kaiser_fast', 1e-1),
                           ('kaiser_best', 1e-1)]:
            yield __test, sr_orig, sr_new, fil, rms, x, y

