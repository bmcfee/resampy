'''Cython implementation of resampler'''

import cython
import numpy as np
cimport numpy as cnp


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef void resample_f(float[:, :] x, float[:, :] y, 
                      double sample_ratio,
                      float[:] interp_win, float[:] interp_delta, int num_table) nogil:
    
    cdef:
        double SCALE = min(1.0, sample_ratio)
        double TIME_INC = 1./sample_ratio
    
        int STEP = int(SCALE * num_table)
    
        double time_register = 0.0
    
        int n = 0
        double P = 0.0
        double PL = 0.0
        int offset = 0
        double eta = 0.0
        int t, i
    
        int nwin = interp_win.shape[0]
        int n_orig = x.shape[0]
        int n_out = y.shape[0]
        int n_channels = y.shape[1]
        
        double weight = 0.0

    for t in range(n_out):
        # Grab the top bits as an index to the input buffer
        n = int(time_register)
        
        # Grab the fractional component of the time index
        P = SCALE * (time_register - n)
        
        # Offset into the filter
        PL = P * num_table
        offset = int(PL)
        
        # Interpolation factor
        eta = PL - offset
        
        # Compute the left wing of the filter response
        for i in range(min(n + 1, (nwin - offset) // STEP)):

            weight = (interp_win[offset + i * STEP] + eta * interp_delta[offset + i * STEP])
            for j in range(n_channels):
                y[t, j] += weight * x[n - i, j]
        
        # Invert P
        P = SCALE - P

        # Offset into the filter
        PL = P * num_table
        offset = int(PL)
        
        # Interpolation factor
        eta = PL - offset
        
        # Compute the right wing of the filter response
        for i in range(min(n_orig - i - n + 1, (nwin - offset)//STEP)):
            weight = (interp_win[offset + i * STEP] + eta * interp_delta[offset + i * STEP])
            for j in range(n_channels):
                y[t, j] += x[n + i + 1, j]

        # Increment the time register
        time_register += TIME_INC
    pass

