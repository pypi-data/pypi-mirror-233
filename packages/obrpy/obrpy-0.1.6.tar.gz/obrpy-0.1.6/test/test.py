import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from obrpy import obrpy

obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

obrpy_obj.mainOBR()
obrpy_obj.genSettings("Calibration")

input('Open OBRbook, add T0, T1, E0 and E1 columns. Open seetings, write the name of the columns in settings. Once finished press any key to continue')

obrpy_obj.update_OBRbook()
obrpy_obj.update_OBRfiles()
obrpy_obj.update_settings()

obrpy_obj.genSlices()

exit()

Y0 = obrpy_obj.OBRfiles['2'].Data
Y1 = obrpy_obj.OBRfiles['B11'].Data
F =  obrpy_obj.OBRfiles['2'].f
Z =  obrpy_obj.OBRfiles['2'].z

import numpy as np
Y0 = np.array(Y0)
Y0 = Y0[:,0:5000]

Y1 = np.array(Y1)
Y1 = Y1[:,0:5000]

Z = np.array(Z)
Z = Z[0:5000]



out = obrpy_obj.global_analysis_GPU(Y0, Y1, Z, F, local_function=obrpy_obj.Signal.spectral_shift_GPU, point=1)


import matplotlib.pyplot as plt

plt.figure()
plt.plot(Z,out)
plt.grid()
plt.show()
