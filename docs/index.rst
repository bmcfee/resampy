.. resampy documentation master file, created by
   sphinx-quickstart on Sat Apr  9 10:53:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
------------
`resampy` is a python module for efficient time-series resampling.  It is based on the
band-limited sinc interpolation method for sampling rate conversion as described by
[1]_.

.. [1] Smith, Julius O. Digital Audio Resampling Home Page
    Center for Computer Research in Music and Acoustics (CCRMA), 
    Stanford University, 2015-02-23.
    Web published at `<http://ccrma.stanford.edu/~jos/resample/>`_.

`resampy` supports multi-dimensional resampling on numpy arrays, and is well-suited to
audio applications.  For long-duration signals --- e.g., minutes at a high-quality
sampling rate --- `resampy` will be considerably faster
than `scipy.signal.resample` and have little perceivable difference in audio quality.

Its dependencies are `numpy <http://www.numpy.org/>`_, `scipy
<http://www.scipy.org>`_, and `numba <http://numba.pydata.org/>`_.


For a quick introduction to using `resampy`, please refer to the `Examples`_ section.

Installation
------------
`resampy` can be installed from source through `pip`:

.. code-block:: bash

    pip install resampy


Conda users can install pre-compiled packages:

.. code-block:: bash

    conda install -c conda-forge resampy


Advanced users and developers may wish to install from source by cloning the source repository:

.. code-block:: bash

    git clone https://github.com/bmcfee/resampy.git
    cd resampy
    python setup.py build_ext -i
    pip install -e .


Running tests
=============

Developers that wish to run the included unit test suite can do so by installing from source, and then
executing the following commands from the source directory:

.. code-block:: bash

    pip install -e .[tests]
    pip install pytest pytest-cov pytest-faulthandler
    py.test --cov-report term-missing --cov resampy


Examples
--------
.. toctree::
    :maxdepth: 3

    example

API Reference
=============
.. toctree::
   :maxdepth: 2

   api

Changes
=======
.. toctree::
   :maxdepth: 2

   changes

Contribute
==========
- `Issue Tracker <http://github.com/bmcfee/resampy/issues>`_
- `Source Code <http://github.com/bmcfee/resampy>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

