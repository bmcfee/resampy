#!/usr/bin/env python

import numpy as np

import resampy


def make_tone(freq, sr, duration):
    return np.sin(2 * np.pi * freq / sr * np.arange(sr * duration))



def test_quality_sine():

    def __test(sr_orig, sr_new, fil, rms, x, y):

        y_pred = resampy.resample(x, sr_orig, sr_new, filter=fil)

        idx = slice(sr_new // 2, - sr_new//2)

        err = np.mean(np.abs(y[idx] - y_pred[idx]))
        assert err <= rms, '{:g} > {:g}'.format(err, rms)

    FREQ = 880.0
    DURATION = 2.0

    for (sr_orig, sr_new) in [ (44100, 22050), (22050, 44100) ]:
        x = make_tone(FREQ, sr_orig, DURATION)
        y = make_tone(FREQ, sr_new, DURATION)

        for (fil, rms) in [('sinc_window', 1e-6),
                           ('kaiser_fast', 1e-4),
                           ('kaiser_best', 1e-7)]:
            yield __test, sr_orig, sr_new, fil, rms, x, y
