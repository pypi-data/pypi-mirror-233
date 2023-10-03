import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from obrpy import obrpy
import pandas as pd
import numpy as np

obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')


def layer0(ID, slice0, slice1):
    
    P0 = slice0.loc["P"]
    P1 = slice1.loc["P"]

    T0 = slice0.loc["T"]
    T1 = slice1.loc["T"]
    E0 = slice0.loc["E"]
    E1 = slice1.loc["E"]

    p0 = np.absolute(np.fft.fft(P0))
    p1 = np.absolute(np.fft.fft(P1))

    #corr = np.correlate(p0, p1, mode='same')
    
    X = [0,2,3,4]
    Y = [T0-T1, E0-E1]

    #new_row = [ID] + [slice0.loc["ID"]] + [slice1.loc["ID"]] + corr.tolist() + y
    new_row = [ID] + [slice0.loc["ID"]] + [slice1.loc["ID"]] + X + Y

    Xcolumns = [3+i for i in range(0,len(X))]
    Ycolumns = [3+len(X)+i for i in range(0,len(Y))]
    
    return Xcolumns, Ycolumns, new_row

ds = obrpy_obj.genDataset(layer0)

print(ds)