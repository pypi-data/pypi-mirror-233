import sys
import os
from .utils import find_index

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import matplotlib.pyplot as plt

def read_OBR(file:str) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
        Function to read binaries (OBR)

        param
            file    (str): path al fichero a leer

        returns
            f       (np.array)  : Spectral distribution [GHz] (from SF to SF+FI*2*n with FI incrments)
            z       (np.array)  : Spacial distribution  [m]
            Pc      (complex 1xn np.array)  : p-polarization readout (spatial-domain)
            Sc      (complex 1xn np.array)  : s-polarization readout (spatial-domain)

        * Along this file some information has been commented out for a faster reading
          please feel free of uncoment whenever you may need

    """

    # Lectura de datos

    #FileForVer=np.fromfile(file, count=1, dtype= np.dtype('<f'))[0]                 # File format version (3.4)
    offset = np.dtype('<f').itemsize

    #ObrOfdr=np.fromfile(file, count=8,dtype= '|S1', offset = offset).astype('|U8')  # Type of file. Nosense string
    offset += np.dtype('|U8').itemsize
    offset = 12 # No idea why but it works

    StartFreq=np.fromfile(file, count=1,dtype= np.dtype('<d'), offset = offset)[0]  # [GHz] Scan start frequency, the higher in the whole scaned spectrum
    offset += np.dtype('<d').itemsize

    SF=StartFreq

    FreqIncr=np.fromfile(file, count=1,dtype= np.dtype('<d'), offset = offset)[0]   # [GHz] Frecuency increments for frequency readouts
    offset += np.dtype('<d').itemsize

    FI=FreqIncr

    StartTime=np.fromfile(file, count=1,dtype= np.dtype('<d'),offset = offset)[0]   # [ns] Measure initial time. Represents when the outter (outter to OBR) optical fiber begins
    offset += np.dtype('<d').itemsize

    TimeIncr=np.fromfile(file, count=1,dtype= np.dtype('<d'),offset = offset)[0]    # [ns] Time increment
    offset += np.dtype('<d').itemsize

    dt=TimeIncr

    #MeasurementType=np.fromfile(file, count=1,dtype= 'uint16',offset = offset)[0]   # Zero for reflection (backscattering) because OBR also works in transmission (I suppose)
    offset += np.dtype('uint16').itemsize

    GroupIndex=np.fromfile(file, count=1,dtype= np.dtype('<d'),offset = offset)[0]   # Index of refraction, arround 1.5 for silica
    offset += np.dtype('<d').itemsize

    #GainValue=np.fromfile(file, count=1,dtype= 'int32',offset = offset)[0]          # [dB] Gain 
    offset += np.dtype('int32').itemsize

    #ZeroLengthIndex=np.fromfile(file, count=1,dtype= 'int32',offset = offset)[0]    # (StartTime)/(Time_increment) Columna que le corresponde al inicio de medida de la fibra exterior al OBR
    offset += np.dtype('int32').itemsize

    #DataTypeSize=np.fromfile(file, count=1,dtype= 'uint32',offset = offset)[0]      # Number of bytes for each point (8)
    offset += np.dtype('uint32').itemsize

    nPoints=np.fromfile(file, count=1,dtype= 'uint32',offset = offset)[0]            # Number of points of readouts arrays: readout = |real part|imaginary part|
    offset += np.dtype('uint32').itemsize

    n=int(nPoints/2)                                                                 # Readout corresponding points

    DateTime=np.fromfile(file, count=8,dtype= 'uint16',offset = offset)              # Acquisition date
    offset += np.dtype('uint16').itemsize * 8

    CalibrationDate=np.fromfile(file, count=8,dtype= 'uint16',offset = offset)       # Calibration date
    offset += np.dtype('uint16').itemsize * 8

    #TempCoeffs=np.fromfile(file, count=5,dtype= np.dtype('<d'),offset = offset)     # Temperature coeficients (for measures based on spectral shift)
    offset += np.dtype('<d').itemsize * 5

    #StrainCoeffs=np.fromfile(file, count=5,dtype= np.dtype('<d'),offset = offset)   # Deformation coeficients (for measures based on spectral shift)
    offset += np.dtype('<d').itemsize * 5

    #FreqWinFlg=np.fromfile(file, count=1,dtype= 'uint8',offset = offset)[0]         # 1 if a frecuency filter has been applied else 0
    offset += np.dtype('uint8').itemsize

    #Unused=np.fromfile(file, count=1865,dtype= 'uint8',offset = offset)             # Without use (unknown)
    offset += np.dtype('uint8').itemsize * 1865

    Preal=np.fromfile(file, count=n,dtype= np.dtype('<d'),offset = offset)     # Real part of p-polarization readout (already in time domain)
    offset += np.dtype('<d').itemsize * n
    Pimag=np.fromfile(file, count=n,dtype= np.dtype('<d'),offset = offset)     # Imag part of p-polarization readout (already in time domain) 
    offset += np.dtype('<d').itemsize * n
    Sreal=np.fromfile(file, count=n,dtype= np.dtype('<d'),offset = offset)     # Real part of s-polarization readout (already in time domain) 
    offset += np.dtype('<d').itemsize * n
    Simag=np.fromfile(file, count=n,dtype= np.dtype('<d'),offset = offset)     # Imag part of s-polarization readout (already in time domain) 
    offset += np.dtype('<d').itemsize * n

    # Device=np.fromfile(file, count=1, dtype= '|S1', offset = offset)[0].astype('|U8')  # Depends on filename


    """ Posterior calculations """

    GroupIndex = 1.4682                    # Modified for: Corning SMF-28e+ Optical Fiber

    ### Time and frequency space

    tf = (n-1)*dt                       # [ns] Final readout time, computed from total readout number of values (n)
    t  = np.arange(0,tf+dt,dt)          # [ns] Time array with a lineal time increment until final readout time 
    t  = t+StartTime                    # Because the equipment (OBR-4600) reads also its inner part 
    c  = 299792458                      # [m/s] speed of light                          
    z  = t*1e-9*((c)/(GroupIndex*2))    # [m] time in [ns] 299792458 es la velocidad de la luz en el vacio y en indice de grupo es el indice de refracción medio de la fibra

    df    = FI                      # [GHz] Frequency increment
    dw    = df*2*np.pi              # [G·rad/s] Frequency increment in radians per second
    fl    = SF-FI*2*n               # [GHz] Lower frequency
    fh    = SF+FI                   # [GHz] Higher frequency
    f     = np.arange(fl,fh,df)     # [GHz] Frequency axis array

    ### Measurements

    Pt = Preal+Pimag*1j # p-polarization measurement in time domain
    St = Sreal+Simag*1j # s-polarization measurement in time domain

    #r = (np.abs(P)**2 + np.abs(S)**2)**0.5                                         # reflection
    #tg = np.angle(Sw[0:-1]*np.conjugate(Sw[1:])+Pw[0:-1]*np.conjugate(Pw[1:]))/df  # group delay

    return f,z,Pt,St

def multi_read_OBR(files,path_to_data='.',limit1 = None,limit2 = None,display=False,n_plots_max=3) -> tuple[np.ndarray,np.ndarray,dict]:

    """ Function to read multiple OBR files and crop it
    after displaying all signals in the same plot (if display == True)

    :param files        (list)      : List of files to be read (without .orb extension)
    :param path_to_data (string)    : Path to directory which contains all OBR files
    :param limit1       (float)     : First length to conserve in data arrays
    :param limit2       (float)     : Last length to conserve in data arrays
    :param display      (boolean)   : Boolean to display read data (True) or not (False)

    :return f,z,Data          : Read "read_OBR" above
                                        Data['filename'] = [P,S]
                                        f and z are from the last lecture (asuming they are the same for all lectures)
    """

    Data = dict()
    pending_files = list()
    print('*Start reading')

    if display == True:
        
        " Let's make a plot with several lines but not too much"

        max_plots = min(n_plots_max,len(files)-1)
        plt.figure()
        for idx,file in enumerate(files):
            print('Reading',file)
            
            
            if idx < max_plots:
                # Include plot
                f,z,Pt,St =read_OBR(f'{path_to_data}/{file}.obr')
                plt.plot(z,np.log10(np.absolute(Pt+St)))
                Data[file] = [Pt,St]
                pending_files.append(file)
            
            elif idx == max_plots:
                # Last plot, display
                f,z,Pt,St =read_OBR(f'{path_to_data}/{file}.obr')
                plt.plot(z,np.log10(np.absolute(Pt+St)))
                Data[file] = [Pt,St]
                pending_files.append(file)
                plt.xlabel('z [m]')
                plt.ylabel(r'$Log_{10}(H(t))$')
                plt.grid()
                plt.show()

                # Ask for limits
                l1, l2 = ask_for_limits(limit1, limit2, z)

                # Crop previous data
                for file in pending_files:
                    f,z,Data = crop_data(f,z,Data,file,l1,l2)

            elif idx > max_plots:
                # Will not appear
                f,z,Pt,St =read_OBR(f'{path_to_data}/{file}.obr')
                Data[file] = [Pt,St]
                f,z,Data = crop_data(f,z,Data,file,l1,l2)
            
            else:
                print('Error')

        print('*End reading')

    else:
        for idx,file in enumerate(files):
            print('Reading',file)
            f,z,Pt,St = read_OBR(f'{path_to_data}/{file}.obr')
            Data[file] = [Pt,St]
            if idx == 0:
                l1,l2 = ask_for_limits(limit1, limit2, z)
            f,z,Data = crop_data(f,z,Data,file,l1,l2)

        print('*End reading\n')


    return f,z,Data

def ask_for_limits(limit1:float, limit2:float, z:list) -> tuple:
    """ Function to get the closest indexes to the start and end points specified, over an array of values

    :param limit1       (float/bool)        : Start point, if 'False' or 'None' 0  will be returned
    :param limit2       (float/bool)        : End point,   if 'False' or 'None' -1 will be returned
    :param z            (list/np.array)     : array of values 

    :return l1,l2          : Start and end (respectively) indexes of the array which matches the values specified

    """

    if limit1 == 'manual':
        try:
            l1 = float(input('First limit:'))
        except:
            l1 = False
    if limit2 == 'manual':
        try:
            l2 = float(input('Second limit:'))
        except:
            l2 = False
    

    l1 = find_index(z,limit1) if limit1 is not False and limit1 is not None else 0
    l2 = find_index(z,limit2) if limit2 is not False and limit2 is not None else -1

    return l1,l2

def crop_data(f:np.ndarray,z:np.ndarray,Data:list,file:str,l1:int,l2:int) -> tuple[np.ndarray, np.ndarray, list[np.ndarray]]:
    """ Function designed to crop properly all data extracted from .obr file 

    :param f,z,Data     (np.array,np.array,list of np.array)        : OBR information
    :param file         (str)                                       : End point,   if 'False' or 'None' -1 will be returned
    :return l1,l2       (int)                                       : Start and end (respectively) indexes of the array which matches the values specified


    :return f,z,Data     (np.array,np.array,list of np.array)       : OBR information crop

    """

    for measure in range(len(Data[file])):
        if not isinstance(Data[file][measure],list):
            if len(Data[file][measure].shape) == 1:
                Data[file][measure] = Data[file][measure][int(l1):int(l2)]
            elif len(Data[file][measure].shape) == 2:
                Data[file][measure] = Data[file][measure][:,int(l1):int(l2)]
        else:
            pass

    f = f
    z = z[int(l1):int(l2)]

    return f,z,Data
