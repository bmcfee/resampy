# resampy
[![PyPI](https://img.shields.io/pypi/v/resampy.svg)](https://pypi.python.org/pypi/resampy)
[![GitHub license](https://img.shields.io/badge/license-ISC-blue.svg)](https://raw.githubusercontent.com/bmcfee/resampy/master/LICENSE)
[![Build Status](https://travis-ci.org/bmcfee/resampy.png?branch=master)](http://travis-ci.org/bmcfee/resampy?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/bmcfee/resampy/badge.svg?branch=master)](https://coveralls.io/github/bmcfee/resampy?branch=master)
[![Documentation Status](https://readthedocs.org/projects/resampy/badge/?version=latest)](http://resampy.readthedocs.org/en/latest/?badge=latest)

Efficient audio resampling in Python / Cython.

This package implements the band-limited sinc interpolation method for sampling rate conversion as described by:
> Smith, Julius O. Digital Audio Resampling Home Page
> Center for Computer Research in Music and Acoustics (CCRMA), 
> Stanford University, 2015-02-23.
> Web published at [http://www-ccrma.stanford.edu/~jos/resample/](http://www-ccrma.stanford.edu/~jos/resample/).
