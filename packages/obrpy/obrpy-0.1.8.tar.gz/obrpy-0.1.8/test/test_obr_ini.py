import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

###

import pandas as pd
from obrpy import obrpy
import matplotlib.pyplot as plt

test1 = False
test2 = True
test3 = False
test4 = False

if test1:

    """ TEST 1: New creation """

    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')
    obrpy_obj.mainOBR()
    obrpy_obj.save()

    # Delete pkl
    obrpy_obj.fuego_purificador()

if test2:

    """ TEST 2: Settings to set limits """

    # Create object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create OBRbook
    obrpy_obj.initOBR()

    # Create settings
    obrpy_obj.genSettings()
    obrpy_obj.settings.z_ini = 0.1
    obrpy_obj.settings.z_fin = 0.5

    # Compute OBRfiles (with limits from settings)
    obrpy_obj.computeOBR()
    obrpy_obj.save()

    # Delete pkl
    obrpy_obj.fuego_purificador()

if test3:

    """ TEST 3: Limits specified in the input """

    # Create object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create OBRbook
    obrpy_obj.mainOBR(limit1=0.1,limit2=None)
    obrpy_obj.save()

    # Delete pkl
    obrpy_obj.fuego_purificador()

if test4:

    """ TEST 4: Reopen a pkl (comment above one of them)"""
    
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    print(obrpy_obj.obrfiles.book)

    plt.figure()
    for key, val in obrpy_obj.obrfiles.files.items():
        plt.plot(val.z,val.Data[0],label=val.name)

    plt.legend()
    plt.grid()
    plt.show()

    obrpy_obj.fuego_purificador()