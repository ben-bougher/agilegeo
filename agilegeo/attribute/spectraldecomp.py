from numpy import zeros
import numpy as np
from agilegeo.attribute import spectra


def spectraldecomp( data, f=(.1,.25,.4),
                    window_length=32, dt=1,
                    window_type='hann' ):
    """
    Uses the STFT to decompose traces into normalized spectra. Only
    frequencies defined by the user will be output. Using 3
    frequencies will work for RGB color plots.

    :param data: A 1/2D array (samples, traces) of data that will
                 be decomposed.
    :keyword f: A list of frequencies to select from the spectra.
    :keyword window_length: The length of fft window to use for
                            the STFTs. Defaults to 32. Can be
                            provided in seconds if dt is specified.
    :keyword dt: The time sample interval of the traces.
    :keyword window_type: The type of window to use for the STFT. The
                          same input as scipy.signal.get_window.

    :returns: an array of shape (samples, traces, f)
    """

    overlap = 0.5

    
    # Do the 1D case
    if len( data.shape ) == 1:
        ntraces = 1
    else:
        ntraces = data.shape[-1]

    
        
    for i in range( ntraces ):

        if( ntraces == 1 ):
            spect = spectra( data, window_length, dt=dt,
                             window_type=window_type, overlap=overlap,
                             normalize = True )
            if( i == 0 ): output = np.zeros( (spect.shape[0], len(f)))
            
        else:
            spect = spectra( data[:,i], window_length, dt=dt,
                             window_type=window_type, overlap=overlap,
                             normalize = True )
            if( i == 0 ):
                output = np.zeros( (spect.shape[0],ntraces,
                                   len(f) ))

        res = ( (1. / dt) / 2.0 ) / spect.shape[-1]

        for j in range( len( f ) ):

            index = np.floor( f[j] / res )

            if( ntraces == 1 ): output[:,j] = spect[:,index] 
            else: output[:,i, j] = spect[:,index]


        
    return( output )
