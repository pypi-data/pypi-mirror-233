import numpy as np

try:
     import cupy as cp
     cupy_available = True
except Exception as e:
     print('Warning: Please install cupy in order to use GPU acceleration')
     cupy_available = False

import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from UTILS.utils import printProgressBar, find_index


def global_analysis(self, y0:np.ndarray[np.ndarray,np.ndarray], y1:np.ndarray[np.ndarray,np.ndarray],
                        z:np.ndarray, f:np.ndarray,
                        local_function,
                        delta=200, window=2000,
                        point=None, progressbar=False):
    
    """ Computes some analysis between two signals in a given window over a length
        
        :param y0           (np.array)      : first signal  [P,S] (used as reference)
        :param y1           (np.array)      : second signal [P,S]
        :param z            (np.ndarray)    : length array    [m]
        :param f            (np.array)      : frequency array [GHz]

        :param local_function (function): function which will compute some operation for each window

                    Available functions are
                            
                            - spectral_shift()   : relative spectral shift
                            - PSSS()             : phase-spectrum relative spectral shift

                            * All of them are contained in the class Singal of obrpy -> obrpy.Signal.spectral_shift
                    
                    Any custom function provided, which have the following inputs will be work

                            - y0 : local reference signal [P,S]
                            - y1 : local signal [P,S]
                            - z  : spatial array
                            - f  : frequency array
                            - display: will be set as True when the point of global analysis matches the parameter "point"

        
        :optional delta     (int)       : number of points of each step 
        :optional window    (int)       : number of points on window 

        :optional progressbar (bool)    : default is False. If True, a progressbar is displayed while processing the signal
        :optional point       (float)   : default is False. If it is not False, some graphs will be created at this point

        :returns output (np.array)      : array with computed signal at each window in a sequence
    """

    # Re define the window variable (is easier for the rest of the code)
    window = round(window/2)

    # Check type of signal
    if not isinstance(y0, np.ndarray):
         y0 = np.array(y0)
    if not isinstance(y1,np.ndarray):
         y1 = np.array(y1)

    # Check if both y0 and y1 have the same dimension
    if len(y0.shape) != len(y1.shape):
        raise Exception("Signal dimension mismatch")

    # Get the total number of points
    n_points = y0.shape[1]

    # Split the whole points into steps
    steps = range(window,n_points-window+1,delta)

    # Display the signals at this point
    if point is not None:

        point = find_index(z, point)

        plt.figure()
        plt.plot(y0[0],label='y0(P)')
        plt.plot(y1[0],label='y1(P)')
        plt.plot(y0[1],label='y0(S)')
        plt.plot(y1[1],label='y1(S)')
        plt.axvline(x=point)
        plt.grid()
        plt.show()

    # Compute analysis 
    output = []
    for i in steps:

            yy0 = np.array([y0[0,i-window:i+window], y0[1,i-window:i+window]])
            yy1 = np.array([y1[0,i-window:i+window], y1[1,i-window:i+window]])
            zz  = np.array(z[i-window:i+window])

            output.append(float(local_function(yy0,yy1,zz,f,display=True if point is not None and i==point else False)))

            printProgressBar(i + 1, n_points-window-delta-1, prefix = 'Computing spectral shift:', suffix = 'Complete', length = 50) if progressbar else None

    return np.array(output)


if cupy_available:

     def global_analysis_GPU(self, y0:np.ndarray[np.ndarray,np.ndarray], y1:np.ndarray[np.ndarray,np.ndarray],
                         z:np.ndarray, f:np.ndarray,
                         local_function,
                         delta=200, window=2000,
                         point=None, progressbar=False):
     
          """ Computes some analysis between two signals in a given window over a length
               
               :param y0           (np.array)      : first signal  [P,S] (used as reference)
               :param y1           (np.array)      : second signal [P,S]
               :param z            (np.ndarray)    : length array    [m]
               :param f            (np.array)      : frequency array [GHz]

               :param local_function (function): function which will compute some operation for each window

                              Available functions are
                                   
                                   - spectral_shift()   : relative spectral shift
                                   - PSSS()             : phase-spectrum relative spectral shift

                                   * All of them are contained in the class Singal of obrpy -> obrpy.Signal.spectral_shift
                              
                              Any custom function provided, which have the following inputs will be work

                                   - p0 : local reference signal P
                                   - s0 : local reference signal S
                                   - p1 : local signal P
                                   - s1 : local signal S
                                   - z  : spatial array
                                   - f  : frequency array
                                   - display: will be set as True when the point of global analysis matches the parameter "point"

               
               :optional delta     (int)       : number of points of each step 
               :optional window    (int)       : number of points on window 

               :optional progressbar (bool)    : default is False. If True, a progressbar is displayed while processing the signal
               :optional point       (float)   : default is False. If it is not False, some graphs will be created at this point

               :returns output (np.array)      : array with computed signal at each window in a sequence
          """

          # Check type of signal
          if not isinstance(y0, np.ndarray):
               y0 = np.array(y0)
          if not isinstance(y1,np.ndarray):
               y1 = np.array(y1)
          if not isinstance(y0, np.ndarray):
               f = np.array(f)
          if not isinstance(y1,np.ndarray):
               z = np.array(z)

          # Check if both y0 and y1 have the same dimension
          if len(y0.shape) != len(y1.shape):
               raise Exception("Signal dimension mismatch")

          # Get the total number of points
          n_points = y0.shape[1]

          # Split the whole points into steps
          steps = range(window,n_points-window+1,delta)

          ##### GPU acceleration algorithm #####

          # Unpack the signals 
          p0 = y0[0,:]
          p1 = y1[0,:]
          s0 = y0[1,:]
          s1 = y1[1,:]

          # Convert input arrays to CuPy arrays
          p0 = cp.asarray(p0)
          p1 = cp.asarray(p1)
          s0 = cp.asarray(s0)
          s1 = cp.asarray(s1)
          z = cp.asarray(z)
          f = cp.asarray(f)

          # Define the window size and stride
          window_size = window
          stride = delta

          # Generate a list of window indices
          start_indices = cp.arange(0, n_points - window_size + 1, stride)

          # Extract the windows from the data
          p0W = cp.array([p0[i:i+window_size] for i in start_indices])
          p1W = cp.array([p1[i:i+window_size] for i in start_indices])
          s0W = cp.array([s0[i:i+window_size] for i in start_indices])
          s1W = cp.array([s1[i:i+window_size] for i in start_indices])
          zW  = cp.array([z[i:i+window_size] for i in start_indices])

          # Process signal windowed
          output = local_function(p0W,s0W,p1W,s1W,zW,f)

          # Convert output array to NumPy array
          return output.get()

elif not cupy_available:

     def global_analysis_GPU(self, y0:np.ndarray[np.ndarray,np.ndarray], y1:np.ndarray[np.ndarray,np.ndarray],
                    z:np.ndarray, f:np.ndarray,
                    local_function,
                    delta=200, window=2000,
                    point=None, progressbar=False):
          
          if local_function.__name__.endswith('_GPU'):
               func_name = local_function.__name__[:-4] # remove the _GPU suffix
               local_function = getattr(self.Signal, func_name)

          return self.global_analysis(y0=y0, y1=y1, z=z, f=f, local_function = local_function, delta=delta, window=window, point=point, progressbar=progressbar)