import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from obrpy import obrpy
import pandas as pd
import numpy as np

obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

ds = obrpy_obj.genDataset(obrpy_obj.ZeroLayers.psss, percentage=5)

obrpy_obj.dataset.export_obj('./ds.pkl')
obrpy_obj.dataset.export_book('./ds.csv')
obrpy_obj.save()
