import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

###

import pandas as pd
from obrpy import obrpy
import matplotlib.pyplot as plt

test1 = True

if test1:

    # Create object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create OBRbook
    obrpy_obj.initOBR()

    # Create settings
    obrpy_obj.genSettings()
    obrpy_obj.settings.z_ini = 0.1
    obrpy_obj.settings.z_fin = 0.5

    # Export obrfiles to .csv using GUI
    obrpy_obj.settings.export_book()
    obrpy_obj.settings.export_obj()
