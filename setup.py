#!/usr/bin/env python
'''resampy setup script'''

from __future__ import print_function
import imp
import sys
import os
import subprocess

from setuptools import setup
from setuptools.extension import Extension

import numpy as np

PACKAGE_NAME = 'resampy'

VERSION = imp.load_source('resampy.version', 'resampy/version.py')

def generate_cython(package):
    """Cythonize all sources in the package"""
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                         os.path.join(cwd, 'tools', 'cythonize.py'),
                         package],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


EXTENSIONS = [Extension("resampy.interp", ["resampy/interp.c"],
                        include_dirs=[np.get_include()])]

generate_cython(PACKAGE_NAME)

setup(
    author="Brian McFee",
    author_email="brian.mcfee@nyu.edu",
    name=PACKAGE_NAME,
    version=VERSION.version,
    url='https://github.com/bmcfee/resampy',
    download_url='https://github.com/bmcfee/resampy/releases',
    description='Efficient signal resampling',
    license='ISC',
    ext_modules=EXTENSIONS,
    packages=[PACKAGE_NAME],
    package_data={'resampy': ['data/*']},
    install_requires=[
        'numpy>=1.10',
        'scipy>=0.13',
        'six>=1.3',
        'Cython>=0.21'],
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
    ],
)
