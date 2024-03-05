Changes
-------

v0.4.3
~~~~~~
2024-03-05

- `#117 <https://github.com/bmcree/resampy/pull/117>`_ Update to remove deprecated usage of pkg_resources.

v0.4.2
~~~~~~
2022-09-13

- `#115 <https://github.com/bmcfee/resampy/pull/115>`_ Fixed buffer length calculation to avoid
  numerical overflow issues on some platforms.

v0.4.1
~~~~~~
2022-09-09

- `#113 <https://github.com/bmcfee/resampy/pull/113>`_ Fixed a rounding error in output buffer length calculations.
- `#110 <https://github.com/bmcfee/resampy/pull/110>`_ Added a special case to disable unsupported parallel mode on 32bit architectures.

v0.4.0
~~~~~~
2022-08-05

- `#109 <https://github.com/bmcfee/resampy/pull/109>`_ Reduced import time and switched to parallel=False by default.
- `#109 <https://github.com/bmcfee/resampy/pull/109>`_ Integer-valued inputs now produce floating point outputs.

v0.3.1
~~~~~~
2022-07-07

- `#104 <https://github.com/bmcfee/resampy/issues/104>`_ Fixed an efficiency regression introduced in the 0.3.0 release.

v0.3.0
~~~~~~
2022-06-29

- `#99 <https://github.com/bmcfee/resampy/issues/99>`_ Enable caching of pre-computed filters to improve runtime efficiency.
- `#98 <https://github.com/bmcfee/resampy/issues/98>`_ Automate pre-computed filter generation.  Regenerated and improved `kaiser_fast` and `kaiser_best` filters.
- `#95 <https://github.com/bmcfee/resampy/issues/95>`_ Improved documentation
- `#93 <https://github.com/bmcfee/resampy/issues/93>`_ Enable parallel processing for sample rate conversion. *Antonio Valentino*
- `#91 <https://github.com/bmcfee/resampy/issues/91>`_ Improved python packaging workflow.
- `#90 <https://github.com/bmcfee/resampy/issues/90>`_ Fixed a bug in resampling high-dimensional data.
- `#89 <https://github.com/bmcfee/resampy/issues/89>`_ Removed support for python 2.7.
- `#88 <https://github.com/bmcfee/resampy/issues/88>`_ Bypass sample rate conversion if input and output rates are identical.
- `#87 <https://github.com/bmcfee/resampy/issues/87>`_ Added continuous integration tests for linting.
- `#82 <https://github.com/bmcfee/resampy/issues/82>`_ Non-uniform output sample positions. *Antonio Valentio*

v0.2.2
~~~~~~
2019-08-15

- `#68 <https://github.com/bmcfee/resampy/issues/68>`_ Preserve array ordering (C- or F-contiguity) from input to output.

v0.2.1
~~~~~~
2018-06-04

- `#63 <https://github.com/bmcfee/resampy/issues/63>`_ Fixed an error in filter response boundary calculations.

v0.2.0
~~~~~~
2017-09-16

- `#57 <https://github.com/bmcfee/resampy/issues/57>`_ Rewrote the core resampler using Numba. This should alleviate Cython-based installation issues going forward.
- `#14 <https://github.com/bmcfee/resampy/issues/14>`_ Added support for resampling complex-valued signals.
- `#17 <https://github.com/bmcfee/resampy/issues/17>`_ Added a safety check for resampling short signals.

v0.1.5
~~~~~~
2017-02-16

- `#44 <https://github.com/bmcfee/resampy/issues/44>`_ Added type-checking to ensure floating-point inputs

v0.1.4
~~~~~~
2016-07-13

- `#27 <https://github.com/bmcfee/resampy/pull/27>`_ Fixed cython packaging

v0.1.3
~~~~~~
2016-06-21

- `#23 <https://github.com/bmcfee/resampy/pull/23>`_ updated the Cython version requirement.

v0.1.2
~~~~~~
2016-05-26

- `#20 <https://github.com/bmcfee/resampy/pull/20>`_ Expose the ``rolloff`` parameter of (pre-computed) filters

v0.1.1
~~~~~~
2016-05-23

- Fixed a cython installation and distribution issue

v0.1.0
~~~~~~
2016-04-21

- Initial release.
