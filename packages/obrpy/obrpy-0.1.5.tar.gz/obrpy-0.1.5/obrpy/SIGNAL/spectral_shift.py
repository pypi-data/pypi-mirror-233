import numpy as np

try:
    import cupy as cp
    cupy_available = True
except Exception as e:
    print('Warning: Please install cupy in order to use GPU acceleration')
    cupy_available = False

import matplotlib.pyplot as plt
from scipy import signal
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from UTILS.utils import printProgressBar


""" 
Spectral shift

    This module contains functions used to compuhow te the relaive spectral shift
    (which actually is spectralshift/central_frecuency) along an optic fiber longitude

"""

def spectral_shift(y0:np.ndarray,y1:np.ndarray,z:np.ndarray,f:np.ndarray,display=False,fft=True) -> float:
    """ Function to compute the relative spectral shift in a region.

        Scipy's signal.correlate is used to determine the cross correlation, then the
        maximum position is located and related with the spectral shift trought the scan ratio

        :param  y0 (np.array)   : First signal to compare, used as reference [P,S]
        :param  y1 (np.array)   : Second signal to compare [P,S]
        :param  z  (np.array)   : Spatial domain x axis [m] (not used)
        :param  f  (np.array)   : Frequency domain x axis [GHz]

        :optional display=False (bool) : If True, a plot with the cross correlation will be displayed 
                                        (add  "plt.show()" or "plt.savefig()" after this funtion)
        :optional fft=True (bool)      : If True a FFT will be performed after computing the cross correlation

        :retruns spectralshift/mean_f (float)   : relative spectralshift
    """

    # Unpacking the signal
    p0 = y0[0,:]
    p1 = y1[0,:]

    # Length of the signal
    n_points = len(p0) 

    # Frequency sampling
    DF = f[-1]-f[0]     # Frequency increment
    n  = n_points        # Sample lenght
    sr = 1/(DF/n)       # Scan ratio

    # FFT
    p0 = np.absolute(np.fft.fft(p0)) if fft else np.absolute(p0)
    p1 = np.absolute(np.fft.fft(p1)) if fft else np.absolute(p1)

    # Normalization
    p0 = (p0 - np.mean(p0)) / (np.std(p0) * len(p0))
    p1 = (p1 - np.mean(p1)) / (np.std(p1))

    # Cross correlation
    corr = np.correlate(p0, p1, mode='same') if type == '1D' else signal.correlate(p0, p1, mode='same')

    # Spectral shift
    spectralshift_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n+1)
    spectralshift = spectralshift_arr[np.argmax(corr)]


    if display:

        plt.figure()
        plt.title('Cross correlation')
        plt.plot(spectralshift_arr,np.interp(spectralshift_arr,np.linspace(-len(corr)/2,len(corr)/2,len(corr)),corr))
        plt.xlabel(r'$\Delta\nu$ [GHz]')
        plt.grid()

    return -1*spectralshift/np.mean(f)

if cupy_available:
    
    @cp.fuse(kernel_name='spectralshift')
    def spectral_shift_GPU(p0:cp.ndarray,s0:cp.ndarray,p1:cp.ndarray,s1:cp.ndarray,z:cp.ndarray,f:cp.ndarray):

        """ Function to compute the relative spectral shift in a region.

            Scipy's signal.correlate is used to determine the cross correlation, then the
            maximum position is located and related with the spectral shift trought the scan ratio

            :param  p0 (cp.array)   : First signal to compare, used as reference P
            :param  s0 (cp.array)   : First signal to compare, used as reference S
            :param  p1 (cp.array)   : Second signal to compare P
            :param  s1 (cp.array)   : Second signal to compare S
            :param  z  (cp.array)   : Spatial domain x axis [m] (not used)
            :param  f  (cp.array)   : Frequency domain x axis [GHz]

            :retruns spectralshift/mean_f (float)   : relative spectralshift
        """

        # Length of the signal
        n_points = cp.ndarray(p0).shape

        print(z[0])

        # Frequency sampling
        DF = f[-1]-f[0]     # Frequency increment
        n  = n_points        # Sample lenght
        sr = 1/(DF/n)       # Scan ratio

        # FFT
        p0 = cp.absolute(cp.fft.fft(p0)) 
        p1 = cp.absolute(cp.fft.fft(p1)) 

        # Normalization
        p0 = (p0 - cp.mean(p0)) / (cp.std(p0) * len(p0))
        p1 = (p1 - cp.mean(p1)) / (cp.std(p1))

        # Cross corelation
        corr = cp.correlate(p0, p1, mode='same')

        # Spectral shift
        spectralshift_arr = cp.linspace(-0.5*n/sr, 0.5*n/sr, n+1)
        spectralshift = spectralshift_arr[cp.argmax(corr)]

        # Mean f
        f_bar = np.mean(f.get())

        return -1*spectralshift/f_bar

elif not cupy_available:

    def spectral_shift_GPU(p0,s0,p1,s1,z,f):

        y0 = [p0,s0]
        y1 = [p1,s1]

        return spectral_shift(y0,y1,z,f,display=False,fft=True)
