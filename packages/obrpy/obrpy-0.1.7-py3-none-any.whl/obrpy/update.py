import os
import pandas as pd
from copy import deepcopy

def update_OBRfiles(self):
    """ Adds, to each OBRfile object in OBRfiles dict, all new atributes created in the OBRbook and updates OBRbook df from main class """

    # Check if OBRbook exists
    if not isinstance(self.OBRbook, pd.DataFrame):
        print('ERROR: No OBRbook found')
        print(' Please, run genOBRbook() first')
        return

    # Open file
    book = deepcopy(self.OBRbook)

    # Get list of all columns
    columns = list(book.columns)
    new_columns = deepcopy(columns)

    # Read new attribues from OBRbook
    new_columns.remove('ID')
    new_columns.remove('filename')
    new_columns.remove('date')

    # Create atributes in OBRfile objects
    for o in self.OBRfiles.values():
        for atr in new_columns:
            new_value = book.loc[book['ID'] == int(o.ID), atr].values[0]
            setattr(o, atr, new_value)
    

def update_OBRbook(self):
    """ Adds, to each OBRfile object in OBRfiles dict, all new atributes created in the OBRbook and updates OBRbook df from main class """

    # Check if OBRbook.csv exists
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['OBR book filename'])
    if not os.path.exists(book_path):
        print('ERROR: No OBRbook saved as .csv')
        print(' Please, run genOBRbook() first')
        return
    
    # Update OBRbook
    self.OBRbook = pd.read_csv(book_path)

def update_settings(self):
    """ Update settings from settings file new information """

    # Check if settings.xlsx exists
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['settings filename'])
    if not os.path.exists(book_path):
        print(f'ERROR: No seetings file found in {book_path}')
        print(' Please, run genSettingsTemplate() then edit it')
        return
    
    # Update settings
    excel_file = pd.read_excel(book_path, sheet_name=None)
    self.settings.info['Calibration']   = excel_file['Calibration']
    self.settings.info['Test']          = excel_file['Test']
    self.settings.update()

def update_slicesbook(self):
    """ Updates slicesbook """

    # Check if slicesbook.csv exists
    book_path = os.path.join(self.path,self.folders['INFORMATION'],self.INFO['slices book filename'])
    if not os.path.exists(book_path):
        print('ERROR: No slicesbook already saved as .csv')
        print(' Please, run genSlices() first')
        return
    
    # Update OBRbook
    self.slicesbook = pd.read_csv(book_path)

def update_slicesbook_from_slices(self):

    # Extract the attribute names from the first object in the list
    attrs = [a for a in dir(self.slices[0]) if not a.startswith('__') and not a.startswith('P') and not a.startswith('S')]
    
    # Convert the list of objects into a list of dictionaries
    data = [{attr: getattr(slice, attr) for attr in attrs} for slice in self.slices.slices]

    # Convert the list of dictionaries into a Pandas DataFrame
    self.slicesbook = pd.DataFrame(data)

def update_slices(self):

    """ Updates slices form slicesbook """

    ### TO BE DONE ###

    pass

def update_slices_from_slicesbook(self):
    
    """ Updates slices form slicesbook """

    ### TO BE DONE ###

    pass