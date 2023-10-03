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
test4 = True

if test1:

    """ TEST 1: OBRfiles book and obj """

    # Create object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create OBRbook
    obrpy_obj.initOBR(auto_quit=True)

    # Create settings
    obrpy_obj.genSettings()
    obrpy_obj.settings.z_ini = 0.1
    obrpy_obj.settings.z_fin = 0.5

    # Compute OBRfiles (with limits from settings)
    obrpy_obj.computeOBR()

    # Export obrfiles to .csv using GUI
    obrpy_obj.obrfiles.export_book('./test/obrbooks.csv')
    obrpy_obj.obrfiles.export_obj('./test/obrfiles.pkl')

    # Create another object in another folder
    folder2 = 'C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test2'
    os.mkdir(folder2) if not os.path.exists(folder2) else False
    obrpy_obj2 = obrpy(folder2)

    obrpy_obj2.obrfiles.import_book(obrpy_obj.obrfiles.book_path)
    obrpy_obj2.obrfiles.import_obj(obrpy_obj.obrfiles.obj_path)

    print(obrpy_obj2.obrfiles.book)
    print(obrpy_obj2.obrfiles.__dict__)

if test2:

    """ TEST 2: settings book and obj """

    # Create object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create settings
    obrpy_obj.genSettings()

    obrpy_obj.settings.book['Calibration'].loc[0, 1] = 'TT0'
    obrpy_obj.settings.book['Calibration'].loc[0, 3] = 'TT1' 
    obrpy_obj.settings.book['Calibration'].loc[1, 1] = 'EE0'
    obrpy_obj.settings.book['Calibration'].loc[1, 3] = 'EE1'
    obrpy_obj.settings.z_ini = 0.1
    obrpy_obj.settings.z_fin = 0.5

    print('T0',obrpy_obj.settings.T0)  
    print('T1',obrpy_obj.settings.T1)  
    print('E0',obrpy_obj.settings.E0)  
    print('E1',obrpy_obj.settings.E1)  
    print('z_ini',obrpy_obj.settings.z_ini)  
    print('z_fin',obrpy_obj.settings.z_fin)  
    print(obrpy_obj.settings.book)

    # Export obrfiles to .csv using GUI
    obrpy_obj.settings.export_book('./test/settings.csv')
    obrpy_obj.settings.export_obj('./test/settings.pkl')

    # Create another object in another folder
    folder2 = 'C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test2'
    os.mkdir(folder2) if not os.path.exists(folder2) else False
    obrpy_obj2 = obrpy(folder2)

    # Import book
    obrpy_obj2.settings.import_book(obrpy_obj.settings.book_path)
    print('Import book')
    print(obrpy_obj2.settings.book)
    print('T0',obrpy_obj2.settings.T0)  
    print('T1',obrpy_obj2.settings.T1)  
    print('E0',obrpy_obj2.settings.E0)  
    print('E1',obrpy_obj2.settings.E1)  
    print('z_ini',obrpy_obj2.settings.z_ini)  
    print('z_fin',obrpy_obj2.settings.z_fin)  
    print('\n')
    
    # Import obj
    print('Import obj')
    obrpy_obj2.settings.import_obj(obrpy_obj.settings.obj_path)
    print(obrpy_obj2.settings.book)
    print('T0',obrpy_obj2.settings.T0)  
    print('T1',obrpy_obj2.settings.T1)  
    print('E0',obrpy_obj2.settings.E0)  
    print('E1',obrpy_obj2.settings.E1)  
    print('z_ini',obrpy_obj2.settings.z_ini)  
    print('z_fin',obrpy_obj2.settings.z_fin)  
    print('\n')

if test3:
    """ TEST 3: Slices book and obj"""

    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')
    #obrpy_obj = obrpy('/mnt/sda/0_Andres/1_Universidad/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create OBRbook 
    obrpy_obj.initOBR()

    # Create settings
    obrpy_obj.settings.T0 = 'T0'

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
    obrpy_obj.slices.export_obj('./test/slices.csv')
    obrpy_obj.slices.export_book('./test/slices.csv')


    # Create another object in another folder
    folder2 = 'C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test2'
    os.mkdir(folder2) if not os.path.exists(folder2) else False
    obrpy_obj2 = obrpy(folder2)

    # Import book
    obrpy_obj2.slices.import_book(obrpy_obj.slices.book_path)
    print(obrpy_obj2.slices.book)
    
    # Import obj
    obrpy_obj2.slices.import_obj(obrpy_obj.slices.obj_path)    
    print(obrpy_obj2.slices.__dict__)

if test4:

    """ TEST 4: Dataset book and obj"""

    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')
    #obrpy_obj = obrpy('/mnt/sda/0_Andres/1_Universidad/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Import slices from previous test (3)
    obrpy_obj.slices.import_book('./test/slices.csv')
    obrpy_obj.slices.import_obj('./test/slices.pkl')   

    # Generate and export Dataset
    obrpy_obj.genDataset(obrpy_obj.ZeroLayers.psss, percentage=5)

    obrpy_obj.dataset.export_obj('./ds.pkl')
    obrpy_obj.dataset.export_book('./ds.csv')

    # Create another object in another folder
    folder2 = '/mnt/sda/0_Andres/1_Universidad/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test2'
    os.mkdir(folder2) if not os.path.exists(folder2) else False
    obrpy_obj2 = obrpy(folder2)

    # Import book
    obrpy_obj2.dataset.import_book(obrpy_obj.dataset.book_path)
    print(obrpy_obj2.dataset.book)
    
    # Import obj
    obrpy_obj2.dataset.import_obj(obrpy_obj.dataset.obj_path)    
    print(obrpy_obj2.dataset.__dict__)