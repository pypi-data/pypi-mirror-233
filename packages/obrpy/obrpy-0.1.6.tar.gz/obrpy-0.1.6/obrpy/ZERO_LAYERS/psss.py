import numpy as np
import pandas as pd

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from SIGNAL.cross_spectrum import PSSS
from SIGNAL.spectral_shift import spectral_shift

def psss(ID, slice0, slice1):
    
    # Unpack info
    P0 = slice0.loc["P"]
    P1 = slice1.loc["P"]
    S0 = slice0.loc["S"]
    S1 = slice1.loc["S"]
    
    z  = slice0.loc["z"]
    f  = slice0.loc["f"]

    T0 = slice0.loc["T"]
    T1 = slice1.loc["T"]
    E0 = slice0.loc["E"]
    E1 = slice1.loc["E"]

    y0 = np.array([P0,S0])
    y1 = np.array([P1,S1])

 
    X = [spectral_shift(y0, y1, z, f), PSSS(y0, y1, z, f)]
    Y = [T0-T1, E0-E1]

    Xcolumns = [3+i for i in range(0,len(X))]
    Ycolumns = [3+len(X)+i for i in range(0,len(Y))]

    new_row = [ID] + [slice0.loc["ID"]] + [slice1.loc["ID"]] + X + Y

    return Xcolumns, Ycolumns, new_row