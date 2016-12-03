# resampy
[![GitHub license](https://img.shields.io/badge/license-ISC-blue.svg)](https://raw.githubusercontent.com/bmcfee/resampy/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/resampy.svg)](https://pypi.python.org/pypi/resampy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/resampy/badges/version.svg)](https://anaconda.org/conda-forge/resampy)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/resampy/badges/downloads.svg)](https://anaconda.org/conda-forge/resampy)
[![Build Status](https://travis-ci.org/bmcfee/resampy.png?branch=master)](http://travis-ci.org/bmcfee/resampy?branch=master)
[![Circle CI](https://circleci.com/gh/conda-forge/resampy-feedstock.svg?style=svg)](https://circleci.com/gh/conda-forge/resampy-feedstock)
[![TravisCI](https://travis-ci.org/conda-forge/resampy-feedstock.svg?branch=master)](https://travis-ci.org/conda-forge/resampy-feedstock)
[![AppVeyor](https://ci.appveyor.com/api/projects/status/github/conda-forge/resampy-feedstock?svg=True)](https://ci.appveyor.com/project/conda-forge/resampy-feedstock/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/bmcfee/resampy/badge.svg?branch=master)](https://coveralls.io/github/bmcfee/resampy?branch=master)
[![Dependency Status](https://dependencyci.com/github/bmcfee/resampy/badge)](https://dependencyci.com/github/bmcfee/resampy)
[![Documentation Status](https://readthedocs.org/projects/resampy/badge/?version=latest)](http://resampy.readthedocs.org/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.163184.svg)](https://doi.org/10.5281/zenodo.163184)


Efficient sample rate conversion in Python.

This package implements the band-limited sinc interpolation method for sampling rate conversion as described by:
> Smith, Julius O. Digital Audio Resampling Home Page
> Center for Computer Research in Music and Acoustics (CCRMA), 
> Stanford University, 2015-02-23.
> Web published at [http://www-ccrma.stanford.edu/~jos/resample/](http://www-ccrma.stanford.edu/~jos/resample/).


# Installation

`resampy` can be compiled from source via `pip` by saying:
```
pip install resampy
```

Pre-built packages can be installed with `conda` by saying:
```
conda install -c conda-forge resampy
```
