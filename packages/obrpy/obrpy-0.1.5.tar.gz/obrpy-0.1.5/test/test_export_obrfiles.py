import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

###

import pandas as pd
from obrpy import obrpy
import matplotlib.pyplot as plt

test1 = False
test2 = False
test3 = True
test4 = False

if test1:

    """ TEST 1: OBRfiles book with GUI """

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

    # Export obrfiles to .csv using GUI
    obrpy_obj.obrfiles.export_book()

    # Delete pkl
    obrpy_obj.fuego_purificador()

if test2:

    """ TEST 2: OBRfiles book without GUI """

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

    # Export obrfiles to .csv
    obrpy_obj.obrfiles.export_book('./here.csv')

    # Delete pkl
    obrpy_obj.fuego_purificador()


if test3:

    """ TEST 3: OBRfiles as object with GUI """

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

    # Export obrfiles to .csv using GUI
    obrpy_obj.obrfiles.export_obj()

    # Delete pkl
    obrpy_obj.fuego_purificador()

if test4:

    """ TEST 4: OBRfiles as object without GUI """

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

    # Export obrfiles to .pkl
    obrpy_obj.obrfiles.export_obj('./here.pkl')

    # Delete pkl
    obrpy_obj.fuego_purificador()


