# resampy
[![GitHub license](https://img.shields.io/badge/license-ISC-blue.svg)](https://raw.githubusercontent.com/bmcfee/resampy/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/resampy.svg)](https://pypi.python.org/pypi/resampy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/resampy/badges/version.svg)](https://anaconda.org/conda-forge/resampy)
[![CI](https://github.com/bmcfee/resampy/actions/workflows/ci.yml/badge.svg)](https://github.com/bmcfee/resampy/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/bmcfee/resampy/branch/main/graph/badge.svg?token=o6a0xO89rz)](https://codecov.io/gh/bmcfee/resampy)
[![Documentation Status](https://readthedocs.org/projects/resampy/badge/?version=stable)](https://resampy.readthedocs.io/en/stable/?badge=stable)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.596633.svg)](https://doi.org/10.5281/zenodo.596633)

Efficient sample rate conversion in Python.

This package implements the band-limited sinc interpolation method for sampling rate conversion as described by:
> Smith, Julius O. Digital Audio Resampling Home Page
> Center for Computer Research in Music and Acoustics (CCRMA), 
> Stanford University, 2015-02-23.
> Web published at [http://ccrma.stanford.edu/~jos/resample/](http://ccrma.stanford.edu/~jos/resample/).


# Installation

`resampy` can be installed `pip` by the following command:
```
python -m pip install resampy
```

It can also be installed by `conda` as follows:
```
conda install -c conda-forge resampy
```
