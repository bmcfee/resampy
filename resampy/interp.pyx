# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
'''Cython implementation of resampler'''

import cython
import numpy as np
cimport numpy as cnp

from cython import floating
from cython cimport floating


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef void resample_f(floating[:, :] x, floating[:, :] y, 
                      double sample_ratio,
                      double[:] interp_win, double[:] interp_delta, int num_table) nogil:
    
    cdef:
        double scale = min(1.0, sample_ratio)
        double time_increment = 1./sample_ratio
        int index_step = int(scale * num_table)
        double time_register = 0.0
    
        int n = 0
        double frac = 0.0
        double index_frac = 0.0
        int offset = 0
        double eta = 0.0
        double weight = 0.0
    
        int nwin = interp_win.shape[0]
        int n_orig = x.shape[0]
        int n_out = y.shape[0]
        int n_channels = y.shape[1]

        int t, i, j

    for t in range(n_out):
        # Grab the top bits as an index to the input buffer
        n = int(time_register)
        
        # Grab the fractional component of the time index
        frac = scale * (time_register - n)
        
        # Offset into the filter
        index_frac = frac * num_table
        offset = int(index_frac)
        
        # Interpolation factor
        eta = index_frac - offset
        
        # Compute the left wing of the filter response
        for i in range(min(n + 1, (nwin - offset) // index_step)):

            weight = (interp_win[offset + i * index_step] + eta * interp_delta[offset + i * index_step])
            for j in range(n_channels):
                y[t, j] += weight * x[n - i, j]
        
        # Invert P
        frac = scale - frac

        # Offset into the filter
        index_frac = frac * num_table
        offset = int(index_frac)
        
        # Interpolation factor
        eta = index_frac - offset
        
        # Compute the right wing of the filter response
        for i in range(min(n_orig - i - n + 1, (nwin - offset)//index_step)):
            weight = (interp_win[offset + i * index_step] + eta * interp_delta[offset + i * index_step])
            for j in range(n_channels):
                y[t, j] += weight * x[n + i + 1, j]

        # Increment the time register
        time_register += time_increment
    pass

