# resampy
[![PyPI](https://img.shields.io/pypi/v/resampy.svg)](https://pypi.python.org/pypi/resampy)
[![License](https://img.shields.io/pypi/l/resampy.svg)](https://github.com/bmcfee/resampy/blob/master/LICENSE.md)
[![Build Status](https://travis-ci.org/bmcfee/resampy.png?branch=master)](http://travis-ci.org/bmcfee/resampy?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/bmcfee/resampy/badge.svg?branch=master)](https://coveralls.io/github/bmcfee/resampy?branch=master)
[![Documentation Status](https://readthedocs.org/projects/resampy/badge/?version=latest)](http://resampy.readthedocs.org/en/latest/?badge=latest)

Efficient audio resampling in Python / Cython.

This package implements the band-limited sinc interpolation method for sampling rate conversion as described by
[Julius O. Smith III](https://ccrma.stanford.edu/~jos/resample/resample.html).
