.. _examples:

Monophonic resampling
=====================

The following code block demonstrates how to resample an audio signal.

We use `librosa <https://bmcfee.github.io/librosa/>`_ for loading the audio,
but this is purely for ease of demonstration.  `resampy` does not depend on `librosa`.

.. code-block:: python
    :linenos:

    import librosa
    import resampy

    # Load in librosa's example audio file at its native sampling rate
    x, sr_orig = librosa.load(librosa.util.example_audio_file(), sr=None)

    # x is now a 1-d numpy array, with `sr_orig` audio samples per second

    # We can resample this to any sampling rate we like, say 16000 Hz
    y_low = resampy.resample(x, sr_orig, 16000)

    # That's it!


Stereo and multi-dimensional data
=================================

The previous example operates on monophonic signals, but resampy also supports stereo
resampling, as demonstrated below.

.. code-block:: python
    :linenos:

    import librosa
    import resampy

    # Load in librosa's example audio file at its native sampling rate.
    # This time, also disable the stereo->mono downmixing
    x, sr_orig = librosa.load(librosa.util.example_audio_file(), sr=None, mono=False)

    # x is now a 2-d numpy array, with `sr_orig` audio samples per second
    # The first dimension of x indexes the channels, the second dimension indexes
    # samples.
    # x[0] is the left channel, x[1] is the right channel.

    # We can again resample.  By default, resample assumes the last index is time.
    y_low = resampy.resample(x, sr_orig, 16000)

    # To be more explicit, provide a target axis
    y_low = resampy.resample(x, sr_orig, 16000, axis=1)


The next block illustrates resampling along an arbitrary dimension.

.. code-block:: python
    :linenos:

    import numpy as np
    import resampy

    # Generate 4-dimensional white noise.  The third axis (axis=2) will index time.
    sr_orig = 22050
    x = np.random.randn(10, 3, sr_orig * 5, 2)

    # x is now a 10-by-3-by-(5*22050)-by-2 tensor of data.

    # We can resample along the time axis as follows
    y_low = resampy.resample(x, sr_orig, 11025, axis=2)

    # y_low is now a 10-by-3-(5*11025)-by-2 tensor of data

Advanced filtering
==================
resampy allows you to control the design of the filters used in resampling operations.

.. code-block:: python
    :linenos:

    import numpy as np
    import scipy.signal
    import librosa
    import resampy

    # Load in some audio
    x, sr_orig = librosa.load(librosa.util.example_audio_file(), sr=None, mono=False)

    # Resample to 22050Hz using a Hann-windowed sinc-filter
    y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window', window=scipy.signal.hann)

    # Or a shorter sinc-filter than the default (num_zeros=64)
    y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window', num_zeros=32)

    # Or use the pre-built high-quality filter
    y = resampy.resample(x, sr_orig, sr_new, filter='kaiser_best')

    # Or use the pre-built fast filter
    y = resampy.resample(x, sr_orig, sr_new, filter='kaiser_fast')


Benchmarking
============
Benchmarking `resampy` is relatively simple, using `ipython`'s ``%timeit`` magic.
The following example demonstrates resampling a monophonic signal of 400000 samples from
22.05 KHz to 16 KHz using both `resampy` and `scipy.signal.resample`.

.. code-block:: python

    In [1]: import numpy as np

    In [2]: import scipy
    
    In [3]: import resampy
    
    In [4]: x = np.random.randn(400000)
    
    In [5]: sr_in, sr_out = 22050, 16000
    
    In [6]: %timeit resampy.resample(x, sr_in, sr_out, axis=-1)
    1 loop, best of 3: 199 ms per loop
    
    In [7]: %timeit scipy.signal.resample(x,
       ...:                               int(x.shape[-1] * sr_out / float(sr_in)),
       ...:                               axis=-1)
    1 loop, best of 3: 6min 5s per loop
