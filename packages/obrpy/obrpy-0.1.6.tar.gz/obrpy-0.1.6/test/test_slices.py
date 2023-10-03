import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from obrpy import obrpy

obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

# Create OBRbook 
obrpy_obj.initOBR()

# Create settings
obrpy_obj.genSettings()

# Compute OBRfiles (with limits from settings)
obrpy_obj.settings.z_ini = 0.1
obrpy_obj.settings.z_fin = 0.5
obrpy_obj.computeOBR()

# Add values to OBRfiles 
i = 0
for key, val in obrpy_obj.obrfiles.files.items():
    i += 1
    val.T0 = 1 + i
    val.T1 = 2 + 2*i
    val.E0 = 3 + 3*i
    val.E1 = 4 + 4*i


# Gen slices out of OBRfiles
obrpy_obj.genSlices()
obrpy_obj.save()