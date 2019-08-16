Changes
-------

v0.2.2
~~~~~~
- `#68 <https://github.com/bmcfee/resampy/issues/68>`_ Preserve array ordering (C- or F-contiguity) from input to output.

v0.2.1
~~~~~~
- `#63 <https://github.com/bmcfee/resampy/issues/63>`_ Fixed an error in filter response boundary calculations.

v0.2.0
~~~~~~
- `#57 <https://github.com/bmcfee/resampy/issues/57>`_ Rewrote the core resampler using Numba. This should alleviate Cython-based installation issues going forward.
- `#14 <https://github.com/bmcfee/resampy/issues/14>`_ Added support for resampling complex-valued signals.
- `#17 <https://github.com/bmcfee/resampy/issues/17>`_ Added a safety check for resampling short signals.

v0.1.5
~~~~~~
- `#44 <https://github.com/bmcfee/resampy/issues/44>`_ Added type-checking to ensure floating-point inputs

v0.1.4
~~~~~~

- `#27 <https://github.com/bmcfee/resampy/pull/27>`_ Fixed cython packaging

v0.1.3
~~~~~~

- `#23 <https://github.com/bmcfee/resampy/pull/23>`_ updated the Cython version requirement.

v0.1.2
~~~~~~

- `#20 <https://github.com/bmcfee/resampy/pull/20>`_ Expose the ``rolloff`` parameter of (pre-computed) filters

v0.1.1
~~~~~~

- Fixed a cython installation and distribution issue

v0.1.0
~~~~~~

- Initial release.
