import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

###

test1 = False
test2 = False
test3 = False

testN = True

if test1:

    class MyClass:
        _class_attribute = None

        @property
        def class_attribute(self):
            return self._class_attribute

        @class_attribute.setter
        def class_attribute(self, new_value):
            self._class_attribute = new_value
            self.on_class_attribute_modified(new_value)

        @classmethod
        def on_class_attribute_modified(cls, new_value):
            # Function called when class_attribute is modified
            print(f"Class attribute modified: {new_value}")

    # Create an instance of MyClass
    my_instance = MyClass()

    # Set the value of class_attribute
    my_instance.class_attribute = "New value"


if testN:

    import pandas as pd
    from obrpy import obrpy
    import matplotlib.pyplot as plt

    # Create or open object
    obrpy_obj = obrpy('C:/Users/temis/0_CCMSS/CCMSS/1_Software/FOS/OBRpy/obrpy-base/test/folder_test')

    # Create settings
    obrpy_obj.genSettings()

    print('Default settings\n')
    print(obrpy_obj.settings.book['Calibration'])
    print(obrpy_obj.settings.__dict__)
    print('\n')


    print('Changes made by attribute\n')
    obrpy_obj.settings.T0 = 't0'
    obrpy_obj.settings.T1 = 't1'
    obrpy_obj.settings.E0 = 'Deformacion'
    obrpy_obj.settings.E1 = 'Deformacion_lineal'
    obrpy_obj.settings.z_ini = 0.1
    obrpy_obj.settings.z_fin = 0.5
    print(obrpy_obj.settings.book['Calibration'])
    print('\n')
    
    print('Changes made by dataframe\n')
    obrpy_obj.settings.book['Calibration'].loc[0, 1] = 'TT0'
    obrpy_obj.settings.book['Calibration'].loc[0, 3] = 'TT1' 
    obrpy_obj.settings.book['Calibration'].loc[1, 1] = 'EE0'
    obrpy_obj.settings.book['Calibration'].loc[1, 3] = 'EE1'
    obrpy_obj.settings.book['Calibration'].loc[2, 1] = 5.0 
    obrpy_obj.settings.book['Calibration'].loc[3, 1] = 10.0 
    print(obrpy_obj.settings.book['Calibration'])
    print('T0',obrpy_obj.settings.T0)  
    print('T1',obrpy_obj.settings.T1)  
    print('E0',obrpy_obj.settings.E0)  
    print('E1',obrpy_obj.settings.E1)  
    print('z_ini',obrpy_obj.settings.z_ini)  
    print('z_fin',obrpy_obj.settings.z_fin)  
    print('\n')


    print('Mixed \n')
    obrpy_obj.settings.book['Calibration'].loc[0, 1] = 'TT00'
    obrpy_obj.settings.book['Calibration'].loc[0, 3] = 'TT1' 
    print(obrpy_obj.settings.book['Calibration'])
    obrpy_obj.settings.E1 = 'Deformacion_lineal'
    obrpy_obj.settings.book['Calibration'].loc[2, 1] = 5.0 
    obrpy_obj.settings.z_fin = 0.5
    print(obrpy_obj.settings.book['Calibration'])
    print('T0',obrpy_obj.settings.T0)  
    print('T1',obrpy_obj.settings.T1)  
    print('E0',obrpy_obj.settings.E0)  
    print('E1',obrpy_obj.settings.E1)  
    print('z_ini',obrpy_obj.settings.z_ini)  
    print('z_fin',obrpy_obj.settings.z_fin)  
    print('\n')