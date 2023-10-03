import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from UTILS.utils import printProgressBar, find_index

def genSlices(self,delta=200,window=2000,export=False):

    """
    Creates a slices object full of slices by slicing .obr data contained in self.OBRfiles

            optional: delta  (int)  = 200      : step
            optional: window (int)  = 2000     : window
            optional: export (bool) = False    : export slices to .csv and .book

    """

    """ Checkouts """
    # OBRfiles checkout
    self.OBR_checkout()

    # Slices checkout (if already exists)
    if self.slices_checkout():
        pass
    else:
        return
    
    """ Slices generation """

    # Open slices object
    slices_obj = self.slices

    # Generate slices
    LEN = len(self.obrfiles.files);i=0
    printProgressBar(0, LEN, prefix = 'Progress:', suffix = 'Complete', length = 50); i += 1

    for key, OBRfile in self.obrfiles.files.items():
        slices_obj = self._obr2slices(OBRfile,slices_obj,delta=delta,window=window)
        printProgressBar(i, LEN, prefix = 'Progress:', suffix = 'Complete', length = 50); i += 1

    # Update
    self.slices = slices_obj

    # Export
    if export:
        self.slices.export_book()
        self.slices.export_obj()

def _obr2slices(self,OBRfile,slices_obj,delta=200,window=2000):
    """
    Generates slices from a single OBRfile and labels the slices in slices book.

    The slices are created by taking the entire signal and then
    traversing it in jumps of points of size "step" and considering
    the points to be in a bubble of diameter "window".

            param: OBRfile    (OBRfile object)    : an object which contains all the information required
            param: slices_obj (Slices object)     : the slices object which will contain the slices and that will be saved

            optional: delta  = 200     : step
            optional: window = 2000    : window size

            returns: slices_obj (slices object): an object which contains all the slices
    """

    """ Variables checkout """

    # Check if delta is an integer
    if not isinstance(delta,int):
         delta = round(delta)

    # Reduce window to the half F¡for easier programation below
    window = int(window/2)

    """ Get information about state of the fiber from settings """

    # Get environment variables
    T0 = getattr(OBRfile,self.settings.T0)
    T1 = getattr(OBRfile,self.settings.T1)
    E0 = getattr(OBRfile,self.settings.E0)
    E1 = getattr(OBRfile,self.settings.E1)

    z_ini = self.settings.z_ini
    z_fin = self.settings.z_fin

    """ Take data from the segment """

    if OBRfile.z[0] != z_ini or OBRfile.z[-1] != z_fin:
        l = find_index(OBRfile.z,[z_ini,z_fin])
        P = OBRfile.Data[0][l[0]:l[1]]
        S = OBRfile.Data[1][l[0]:l[1]]
        z = OBRfile.z[l[0]:l[1]]
    elif OBRfile.z[0] == z_ini and OBRfile.z[-1] == z_fin:
        P = OBRfile.Data[0]
        S = OBRfile.Data[1]
        z = OBRfile.z
    else:
        raise Exception('Something went wrong with the function obr2slices:( ')
    
    
    """ Make the distributions of the strain and temperature"""

    # Full data length (takes one state of polarization)
    n = len(P)

    # Corresponding steps
    steps = range(window,n-window+1,delta)
    
    x = np.linspace(0,abs(z_fin-z_ini),len(steps))
    T = T0 + T1 * x
    E = E0 + E1 * x

    """ Slices generation """

    # Column names and slice initialization
    slice_obj = self.Slice()
    column_names = [key for key in slice_obj.__dict__.keys()]

    # Create a dataframe to storage new information
    new_information = pd.DataFrame(columns = column_names, dtype=object)

    # ID initialization
    ID = slices_obj.last_ID

    # Generate slices
    for idx,i in enumerate(steps):

            # Current ID
            ID += 1
 
            # Update new information
            new_row = {
            'ID'                : ID,
            'T'                 : T[idx],               # [ºC]
            'E'                 : E[idx],               # 
            'z'                 : z[i-window:i+window], # [m]                    
            'x'                 : x[idx]*1e3,           # [mm]
            'f'                 : OBRfile.f,            # [GHz]
            'delta'             : delta,
            'window'            : window,
            'date'              : time.strftime("%Y,%m,%d,%H:%M:%S"),
            'parent_file'       : OBRfile.ID,
            'P'                 : P[i-window:i+window],
            'S'                 : S[i-window:i+window]}

            # Append new row
            new_information = pd.concat([new_information, pd.DataFrame([new_row])], ignore_index=True)

            # Append new element
            slice_obj = self.Slice()
            for val in column_names:
                setattr(slice_obj, val, new_row[val])
            slices_obj.slices[ID] = slice_obj

    # Update last ID
    slices_obj.last_ID = ID

    return slices_obj


def genDataset(self, layer0, matches = 100, percentage = 100):
    
    """ Function to load all slices (previously generated), compute them in pairs with a function, and
    genenerate new values for a dataset usable for AI 

        : param: layer0 (fun) : function to compute slices by pairs, it must take two rows of slices.book
                                and return Xcolumns, Ycolumns and the new_row (list) of dataframe whose first columns must be 
                                the ID of the row, the ID of the first parent and the ID of the second one (in that order)

        : optional: matches (float)                   : percentage of reference segments to consider from total
        : optional: percentage (float) :              : percentage of dataset to consider

    """

    """ Checkout """

    if not isinstance(self.slices,bool) and len(self.slices.slices) != 0 :
        pass
    else:
        print("No slices found: Please run genSlices() and then genDataset()")
        return

    if self.dataset_checkout():
        pass
    else:
        return

    """ Dataset generation """
    dataset = self.dataset

    # Create slices book
    slices_book = self.slices.create_book()
    slices_book = slices_book.sample(frac=percentage/100)

    # Generate dataset
    LEN = int(len(slices_book.index)); i=0; elements=0
    printProgressBar(0, LEN, prefix = 'Progress:', suffix = 'Complete', length = 50); i += 1

    for index, row in slices_book.iterrows():

        # Search in dataframe for other rows to consider as reference
        try:
            ref_rows = slices_book[(round(slices_book['x'], 8) == round(row['x'],8))]
        except:
            print('NO REF FOUND for:',row['ID'])
            z_matches = slices_book[slices_book['x'] == row['x']]
            print('z_matches: ',len(z_matches))
            continue

        # Reduce number of references
        ref_rows = ref_rows.sample(frac=matches/100)

        # For each slice in the same position compute difference
        for jndex, ref_row in ref_rows.iterrows():

            # Update ID
            dataset.last_ID += 1

            # Compute the pair of slices
            dataset.Xcolumns, dataset.Ycolumns, new_row = layer0(dataset.last_ID, row, ref_row)
            dataset.data = pd.concat([dataset.data, pd.DataFrame([new_row])], ignore_index=True)

            # Just to know later
            elements += 1

        printProgressBar(i, LEN, prefix = 'Progress:', suffix = 'Complete', length = 50); i += 1


    print(f'Dataset with {elements} elements created!')

    # Update book with new information
    self.dataset = dataset
    print(dataset.data)

    return dataset.data