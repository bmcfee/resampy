---
title: 'resampy: efficient sample rate conversion in Python'
tags:
  - digital signal processing
  - sample rate conversion
authors:
 - name: Brian McFee
   orcid: 0000-0001-6261-9747
   affiliation: 1
affiliations:
 - name: New York University
   index: 1
date: 13 July 2016
bibliography: paper.bib
---

# Summary

This package implements efficient, high-quality sample rate conversion using the
band-limited sinc interpolation method [@RESAMPLE].
This method supports fast sample rate conversion for long and multi-channel signals.
Its functionality and features are similar to `libsamplerate` [@libsamplerate], but it differs by having a permissive (BSD-style) license, and it is written in Cython so that it is easier to
install and use within larger Python projects.

# References
