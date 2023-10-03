import os
import pandas as pd

class obrpy(object):
    """
        Main class for correct management of .obr files

            Initialization:
            
                An object of class obrpy can be initialized either by specifying the path or leaving it unspecified, 
                in this case, a wizard will be displayed to select the folder where the .obr and other files will 
                be saved.

            Atributes:

                path (str)                       : absolute path to the root folder
                name (str)                       : name of the root folder (used as the name of the object) 
                folders (dict)                   : dictionary with the name of the folders where different files are storaged
                INFO (dict)                      : dictionary which contains the name of each external file created by this clase
                OBRfiles (dict)                  : dictionary which contains all OBRfile objects labeled with its filename
                settings (obj of class Settings) : object which contains all settings information

            Methods:

                - obr -
                mainOBR()               
                initOBR()        
                computeOBR()        
                update_OBRfiles()  

                - obrsdk -
                OBRSDKcalibration() 
                OBRSDKalignment()
                OBRSDKscan()
                OBRSDKextendedScan()

                - settings -
                genSettingsTemplate()
                genSettings()

                - load -
                load()              
                
                - save -
                save()              
                save_OBRfiles()     
                save_something()
                save_settings()   

                - update -
                update_OBRfiles() 
                update_OBRbook()
                update_settings()

            Classes:

                OBRfile()
                Settings()
    """

    def __init__(self,path=None,showpath=False) -> None:


        ######### Folder definition #########

        # Launch GUI if no path is provided
        if not path:
            from .gui import PathSelector
            import tkinter as tk
            # Initialize gui
            root = tk.Tk()
            root.geometry("400x100")
            root.title("Path Selector")

            # Create gui
            app = PathSelector(master=root)
            app.pack_propagate(0)
            app.mainloop()

            # Get path
            path = app.path

        # In construction generates absolute path and name based on the folder name
        self.path = os.path.abspath(path)
        self.name = f'{os.path.basename(os.path.normpath(path))}.pkl'

        # Just to check it
        if showpath:
             print(os.listdir(self.path))

        ######### Load or creation #########

        # Tries to load dataset object, else, if not found, creates one
        try:      
            self.load()

        except Exception as e:
            if 'No such file or directory' in str(e):
                print('No obrpy object (.pkl) found in path, creating new one')
                self.new()
            else:
                print(e)
                exit()

            

    ######### Classes definitions #########

    class OBRfile(object):
        
        """ Container class for '.obr' file information """

        def __init__(self,ID,filename,date):

            self.ID             = ID             # see ID_generator() for information
            self.filename       = filename
            self.name           = filename.replace('.obr','')
            self.date           = date           # %Y,%M,%D,%h:%m:%s
            self.f              = None           # [GHz]
            self.z              = None           # [m]
            self.Data           = None           # P, S

    class OBRfiles(object):

        def __init__(self,obj_path=None, book_path=None):
            
            self.files = dict()

            # Import/Export stuff 
            self.obj_path  = obj_path   # Where to save the object
            self.book      = None       # Object as pd.DataFrame
            self.book_path = book_path  # Where to save the book
            self.exclude_columns = ['f', 'z', 'Data']   # List of columns to exclude in book
            self._export_book_message = 'Select a path to export obrfiles book (.csv)'      
            self._export_obj_message  = 'Select a path to export obrfiles obj (.pkl)'

        def create_book(self) -> pd.DataFrame:

            self.book = pd.DataFrame.from_records([{k: v for k, v in value.__dict__.items()} for value in self.files.values()])
            
            return self.book

        from .to_export import export_book, export_obj

        from .to_import import import_book, import_obj


    
    class Settings(object):
        
        """ Class to manage settings information """

        ### Some stuff to link attributes ###

        _T0 = 'T0'    # [ºC]
        _T1 = 'T1'    # [ºC/m]      T(x) = T0 + T1 * x  -> Name of temperature coeficients in OBRbook 
        _E0 = 'E0'    # []          E(x) = E0 + E1 * x  -> Name of strain coeficients in OBRbook
        _E1 = 'E1'    # [1/m]
        _z_ini = 0    # Initial point of the segment of interest x=0
        _z_fin = 0    # Final point of the segment of interest x=0

        # T0
        @property
        def T0(self):
            return str(self.book['Calibration'].loc[0, 1]) if self.book['Calibration'].loc[0, 1] is not None else ''
        
        @T0.setter
        def T0(self,new_value):
            self._T0 = new_value
            self.book['Calibration'].loc[0, 1] = new_value

        # T1
        @property
        def T1(self):
            return str(self.book['Calibration'].loc[0, 3]) if self.book['Calibration'].loc[0, 3] is not None else ''
        
        @T1.setter
        def T1(self,new_value):
            self._T1 = new_value
            self.book['Calibration'].loc[0, 3] = new_value    

        # E0
        @property
        def E0(self):
            return str(self.book['Calibration'].loc[1, 1]) if self.book['Calibration'].loc[1, 1] is not None else ''
        
        @E0.setter
        def E0(self,new_value):
            self._E0 = new_value
            self.book['Calibration'].loc[1, 1] = new_value  

        # E1
        @property
        def E1(self):
            return str(self.book['Calibration'].loc[1, 3]) if self.book['Calibration'].loc[1, 3] is not None else ''
        
        @E1.setter
        def E1(self,new_value):
            self._E1 = new_value
            self.book['Calibration'].loc[1, 3] = new_value      

        # z_ini
        @property
        def z_ini(self):
            return float(self.book['Calibration'].loc[2, 1]) if self.book['Calibration'].loc[2, 1] is not None else 0
        
        @z_ini.setter
        def z_ini(self,new_value):
            self._z_ini = new_value
            self.book['Calibration'].loc[2, 1] = new_value

        # z_fin
        @property
        def z_fin(self):
            return float(self.book['Calibration'].loc[3, 1]) if self.book['Calibration'].loc[3, 1] is not None else 0
        
        @z_fin.setter
        def z_fin(self,new_value):
            self._z_fin = new_value
            self.book['Calibration'].loc[3, 1] = new_value      
   

        def __init__(self,situation=None,obj_path=None,book_path=None):

            self.book = {'Calibration': None, 'Test': None}
            self.book['Calibration'] = pd.DataFrame([[None] * 4] * 4, columns=[0, 1, 2, 3])   

            self.T0 = 'T0'    # [ºC]
            self.T1 = 'T1'    # [ºC/m]      T(x) = T0 + T1 * x  -> Name of temperature coeficients in OBRbook 
            self.E0 = 'E0'    # []          E(x) = E0 + E1 * x  -> Name of strain coeficients in OBRbook
            self.E1 = 'E1'    # [1/m]
            self.z_ini = None    # Initial point of the segment of interest x=0
            self.z_fin = None    # Final point of the segment of interest x=0

            # Import/Expor stuff
            self.obj_path  = obj_path   # Where to save the object    
            self.book_path = book_path  # Where to save the book  
            self._export_book_message = 'Select a path to export seetings book (.xlsx)'      
            self._export_obj_message  = 'Select a path to export seetings obj (.pkl)'
             

        def export_book(self,path=None):

            # Update dataframe
            #self.update_book() # Actually this is unnecessary currently because attributes are linked but...

            # Launch GUI if no path is provided
            if not path:
                from tkinter import filedialog
                path = filedialog.asksaveasfilename(defaultextension='.xlsx',title=self._export_book_message)

            # Check extension
            if not path.endswith(".xlsx"):
                path = os.path.splitext(path)[0] + ".xlsx"

            # Update book path
            self.book_path = path

            # Initialize excel writer
            writer = pd.ExcelWriter( self.book_path, engine='xlsxwriter')
            
            # Create the "Calibration" sheet
            calibration_data = self.book['Calibration']
            calibration_data.to_excel(writer, sheet_name='Calibration', index=False)
            # Create the "Test" sheet
            test_data = self.book['Test'] if self.book['Test'] is not None else pd.DataFrame()
            test_data.to_excel(writer, sheet_name='Test', index=False)
            
            # save the Excel file
            writer.save()
            print('--> settings file saved in', self.book_path)

        from .to_export import export_obj

        def import_book(self, path=None):
            """ Overwrite the book with an external one """
    
            # Set default if None
            if not path:  
                path = self.book_path

            # Check if the book exists
            if not os.path.exists(path):
                raise('ERROR: No book (.xlsx) found with path ' + path)
            
            # Read the Excel file
            book_data = pd.read_excel(path, sheet_name=['Calibration', 'Test'])

            # Access the 'Calibration' sheet data
            self.book['Calibration'] = book_data['Calibration']
            # Access the 'Test' sheet data
            self.book['Test'] = book_data['Test']

            # Update book_path
            self.book_path = path 

            print(f'---> Book loaded from: '+ self.book_path)
            
            # self.update_attributes()

            return self.book

        from .to_import import import_obj

    class Slice(object):
        """
        Container class for one slice
        """

        def __init__(self):
            self.ID           = 0       # ID of the slice, within the slices objet
            self.T            = 0       # Temperature of the slice
            self.E            = 0       # Strain of the slice
            self.z            = list()  # [m]   Spatial axis
            self.x            = 0       # [mm]  Relative position of this slide into the segment of interest (to compute T and E as uniform variables)
            self.f            = list()  # [GHz] Frequency axis
            self.delta        = 0       # [Number of points] Sensor spacing 
            self.window       = 0       # [Number of points] Sensor length
            self.date         = ''      # Date of the measurement formatted as %Y,%M,%D,%h:%m:%s
            self.parent_file  = ''      # File where the data has been extracted
            self.P            = list()  # p-polarization signal, later it will be a complex numpy array
            self.S            = list()  # s-polarization signal, later it will be a complex numpy array

    class Slices(object):

        """
        Class to contain a dataset of slices
        """

        def __init__(self, obj_path=None, book_path=None):

            self.last_ID = -1
            self.slices  = dict()
        
            # Import/Export stuff 
            self.obj_path  = obj_path                       # Where to save the object
            self.book      = None                           # Object as pd.DataFrame
            self.book_path = book_path                      # Where to save the book
            self.exclude_columns = ['z', 'f', 'P', 'S']     # List of columns to exclude in book
            self._export_book_message = 'Select a path to export slices book (.csv)'      
            self._export_obj_message  = 'Select a path to export slices obj (.pkl)'

        def create_book(self) -> pd.DataFrame:

            self.book = pd.DataFrame.from_records([{k: v for k, v in value.__dict__.items()} for value in self.slices.values()])
            
            return self.book

        from .to_export import export_book, export_obj

        from .to_import import import_book, import_obj

    class Dataset(object):

        def __init__(self,obj_path=None, book_path=None):
            
            self.data = pd.DataFrame()
            
            # The dataset is composed as follows:
            #
            #        0       1        2         ... Xcolumns ... Ycolumns 
            #       ID  parent1_ID parent2_ID   ...    X     ...    Y 
            #     
  
            self.Xcolumns    = list()
            self.Ycolumns    = list()
            self.last_ID     = -1

            # Import/Export stuff 
            self.obj_path  = obj_path   # Where to save the object
            self.book      = None       # Object as pd.DataFrame
            self.book_path = book_path  # Where to save the book
            self.exclude_columns = []   # List of columns to exclude in book
            self._export_book_message = 'Select a path to export dataset book (.csv)'      
            self._export_obj_message  = 'Select a path to export dataset obj (.pkl)'

        def create_book(self) -> pd.DataFrame:

            self.book = self.data
            
            return self.book

        from .to_export import export_book, export_obj

        from .to_import import import_book, import_obj

    class Signal(object):

        """ Class to contain all singal analysis functions available """

        def __init__(self) -> None:
            pass

        from .SIGNAL.cross_spectrum import PSSS
        from .SIGNAL.spectral_shift import spectral_shift, spectral_shift_GPU

    class ZeroLayers(object):

        def __init__(self) -> None:
            pass

        from .ZERO_LAYERS.psss import psss


    ######### Methods definitions #########

    # General purpose methods

    from .load import load, new

    from .save import save

    from .clear import clear_slices, clear_dataset

    from .fuego import fuego_purificador

    from .checkouts import OBR_checkout, slices_checkout, dataset_checkout

    ### Data reading methods
    
    from .obr import mainOBR, initOBR, computeOBR

    from .obrsdk import OBRSDKcalibration, OBRSDKalignment, OBRSDKscan, OBRSDKextendedScan

    from .settings import getSettingsTemplates, genSettings, _getNewValuesFromOBRfiles

    ### Data usage methods

    # from .take_a_look import take_a_look # TO BE DONE

    from .ANALYSIS.global_analysis import global_analysis, global_analysis_GPU

    from .ANALYSIS.local_analysis import genSlices, _obr2slices, genDataset


def path_selector():

    from .gui import PathSelector
    import tkinter as tk
    # Initialize gui
    root = tk.Tk()
    root.geometry("400x100")
    root.title("Path Selector")

    # Create gui
    app = gui(master=root)
    app.pack_propagate(0)
    app.mainloop()

    # Return path
    return app.path