'''Cython implementation of resampler'''

import cython
import numpy as np
cimport numpy as cnp


@cython.boundscheck(False)
@cython.wraparound(False)
def resample_f(float[:] x, float[:] y, double sample_ratio,
               float[:] interp_win, float[:] interp_delta, int num_table):
    
    cdef double SCALE = min(1.0, sample_ratio)
    cdef double TIME_INC = 1./sample_ratio
    
    cdef int STEP = int(SCALE * num_table)
    
    cdef double time_register = 0.0
    
    cdef int n_orig = len(x)
    cdef int n = 0
    cdef double P = 0.0
    cdef double PL = 0.0
    cdef int offset = 0
    cdef double eta = 0.0
    cdef int t, i
    
    cdef int nwin = len(interp_win)
    
    for t in range(len(y)):
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
            y[t] += x[n - i] * (interp_win[offset + i * STEP] + 
                                eta * interp_delta[offset + i * STEP])
        
        # Invert P
        P = SCALE - P

        # Offset into the filter
        PL = P * num_table
        offset = int(PL)
        
        # Interpolation factor
        eta = PL - offset
        
        # Compute the right wing of the filter response
        for i in range(min(n_orig - i - n + 1, (nwin - offset)//STEP)):
            y[t] += x[n + i + 1] * (interp_win[offset + i * STEP] +
                                    eta * interp_delta[offset + i * STEP])

        # Increment the time register
        time_register += TIME_INC
    pass

