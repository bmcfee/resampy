'''resampy install script'''
import imp

from setuptools import setup


VERSION = imp.load_source('resampy.version', 'resampy/version.py')


setup(
    author="Brian McFee",
    author_email="brian.mcfee@nyu.edu",
    name='resampy',
    version=VERSION.version,
    url='https://github.com/bmcfee/resampy',
    download_url='https://github.com/bmcfee/resampy/releases',
    description='Efficient signal resampling',
    license='ISC',
    packages=['resampy'],
    package_data={'resampy': ['data/*']},
    install_requires=[
        'numpy>=1.10',
        'scipy>=0.13',
        'numba>=0.32',
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
