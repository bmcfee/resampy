'''resampy install script'''
import imp
import sys

from setuptools import setup, Extension
import numpy as np


USE_CYTHON = False
EXT = '.c'

if 'build_ext' in sys.argv:
    from Cython.Build import cythonize
    USE_CYTHON = True
    EXT = '.pyx'


VERSION = imp.load_source('resampy.version', 'resampy/version.py')

sourcefiles = ['resampy/interp' + EXT]
extensions = [Extension('resampy.interp',
                        ['resampy/interp' + EXT],
                        include_dirs=[np.get_include()])]

if USE_CYTHON:
    extensions = cythonize(extensions)


setup(
    author="Brian McFee",
    author_email="brian.mcfee@nyu.edu",
    name='resampy',
    version=VERSION.version,
    url='https://github.com/bmcfee/resampy',
    download_url='https://github.com/bmcfee/resampy/releases',
    description='Efficient signal resampling',
    license='ISC',
    ext_modules=extensions,
    packages=['resampy'],
    package_data={'resampy': ['data/*']},
    install_requires=[
        'numpy>=1.10',
        'scipy>=0.13',
        'six>=1.3',
        'Cython>=0.23'],
    extras_require={
        'docs': [
            'sphinx!=1.3.1',  # autodoc was broken in 1.3.1
            'numpydoc',
        ],
        'tests': [
            'pytest',
            'pytest-cov',
        ],
    },
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
