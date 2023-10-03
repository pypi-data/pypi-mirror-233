import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from obrpy import obrpy
obrobj = obrpy('./test/folder_test')
obrobj.OBRSDKscan('p')