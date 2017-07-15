'''resampy install script'''
import imp

from distutils.version import LooseVersion

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.sdist import sdist as _sdist


VERSION = imp.load_source('resampy.version', 'resampy/version.py')

extensions = [Extension('resampy.interp', ['resampy/interp.pyx'])]


class build_ext(_build_ext):
    # build extensions borrowed from yt: 
    # https://github.com/yt-project/yt/blob/master/setup.py#L291
    # subclass setuptools extension builder to avoid importing cython and numpy
    # at top level in setup.py. See http://stackoverflow.com/a/21621689/1382869
    def finalize_options(self):
        try:
            import cython
            import numpy
        except ImportError:
            raise ImportError(
"""Could not import cython or numpy. Building resampy from source requires
cython and numpy to be installed. Please install these packages using
the appropriate package manager for your python environment.""")
        if LooseVersion(cython.__version__) < LooseVersion('0.23'):
            raise RuntimeError(
"""Building resampy from source requires Cython 0.23 or newer but
Cython %s is installed. Please update Cython using the appropriate
package manager for your python environment.""" %
                cython.__version__)
        if LooseVersion(numpy.__version__) < LooseVersion('1.10'):
            raise RuntimeError(
"""Building resampy from source requires NumPy 1.10 or newer but
NumPy %s is installed. Please update NumPy using the appropriate
package manager for your python environment.""" %
                numpy.__version__)
        from Cython.Build import cythonize
        self.distribution.ext_modules[:] = cythonize(
                self.distribution.ext_modules)
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process
        # see http://stackoverflow.com/a/21621493/1382869
        if isinstance(__builtins__, dict):
            # sometimes this is a dict so we need to check for that
            # https://docs.python.org/3/library/builtins.html
            __builtins__["__NUMPY_SETUP__"] = False
        else:
            __builtins__.__NUMPY_SETUP__ = False
        self.include_dirs.append(numpy.get_include())


class sdist(_sdist):
    # subclass setuptools source distribution builder to ensure cython
    # generated C files are included in source distribution.
    # See http://stackoverflow.com/a/18418524/1382869
    # subclass setuptools source distribution builder to ensure cython
    # generated C files are included in source distribution and readme
    # is converted from markdown to restructured text.  See
    # http://stackoverflow.com/a/18418524/1382869
    def run(self):
        # Make sure the compiled Cython files in the distribution are
        # up-to-date
        from Cython.Build import cythonize
        cythonize(extensions)
        _sdist.run(self)


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
    cmdclass={'sdist': sdist, 'build_ext': build_ext},
    install_requires=[
        'numpy>=1.10',
        'scipy>=0.13',
        'six>=1.3'],
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
