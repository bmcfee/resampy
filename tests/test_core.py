#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import resampy

from nose.tools import eq_, raises


def test_shape():

    def __test(axis, sr_orig, sr_new, X):

        Y = resampy.resample(X, sr_orig, sr_new, axis=axis)

        target_shape = list(X.shape)
        target_shape[axis] = target_shape[axis] * sr_new // sr_orig

        eq_(target_shape, list(Y.shape))

    sr_orig = 100
    X = np.random.randn(sr_orig, sr_orig, sr_orig)

    for axis in [0, 1, 2]:
        yield __test, axis, sr_orig, sr_orig // 2, X
