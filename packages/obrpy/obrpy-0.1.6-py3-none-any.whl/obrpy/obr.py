import os
import pandas as pd
import numpy as np
import glob

from .UTILS.read_OBR import multi_read_OBR

def mainOBR(self,limit1=None,limit2=None) -> None:
    """ Computes the following sequence:
            
        * First generates OBR book from OBR filenames and the date recorded in each .obr
                
            self.initOBR()

        * Then open each one and reads relevant information in the specified segment
                
            self.computeOBR(limit1,limit2)

        
        :optional limit1 (float/bool)=None: Initial point of the region of interest 
        :optional limit2 (float/bool)=None: Final   point of the region of interest 
    
    """

    self.initOBR()
    self.computeOBR(limit1,limit2)

def initOBR(self,auto_overwrite=False, auto_quit = False) -> None:
    """
    Function to generate OBR book from OBR filenames and the date recorded in each .obr

        :optional: auto_overwrite (bool) = False: if True the OBRbook will be auto-overwritten
        :returns: df (pd.Dataframe): dataframe from OBR book file

    """

    # Check current information

    if len(self.obrfiles.files) != 0:
        print('OBR files already registered')
        if auto_quit:
            print('Auto-quit enabled, returning')
            return
        else:
            if auto_overwrite==True:
                print(' Auto-overwrite enabled, obrfiles will be overwitten')
                pass
            else:
                ans = input('OBR files already initialized (overwrite/quit):')
                if 'o' in ans:
                    pass
                if 'q' in ans:
                    return


    # Get all OBR files
    OBR_filenames = find_OBR(os.path.join(self.path,self.folders['OBR']))
    
    # Initialize dataframe
    df = pd.DataFrame()

    # Loop through OBR files saving them into obrfiles.files dict
    for filename in OBR_filenames:
        # Get date
        date = get_date(os.path.join(self.path,self.folders['OBR'],filename))
        # Get ID from date
        ID = ID_generator(date)
        # Append to object OBRfile
        self.obrfiles.files[filename.replace('.obr','')] = self.OBRfile(ID,filename,date)
        
    print('Done!')


def computeOBR(self,limit1=None,limit2=None) -> None:
    """
    Reads all .obr files and registers information: f,z and Data = [Pc,Sc,Hc]
    among currently existing (filename, name, flecha, temperature and date)

    * If RAM is not able to allocate enough memory the object will be saved and
    by running this function a couple of times all the information will be
    sotoraged correctly

    :optional: limit1 (bool) = None
    :optional: limit2 (bool) = None

        * If both limits (limit1 and limit2) are None, a prompt will be displayed asking for them
        * If some limit  (limit1 or  limit2) is False, no prompt will be displayed asking for them and will be assumed that the users wants to keep the whole OBR readouts 

    """

    # Check for region of interest
    if limit1==None and limit2==None:

        if self.settings.z_ini is None and self.settings.z_fin is None:
            # If there is not settings file, display warning
            print('WARNING: No settings found')
            print('Please if you want to configure the DOFS settings run:')
            print('>>     your_obrpy_object.genSettings(Calibration_df, Test_df)')
            print('or')
            print('>>     your_obrpy_object.genSettingsTemplate()')
            print('edit it and then import the values with:')
            print('>>     your_obrpy_object.import_settings("your/path/to/your/file.xslx")')
            print('WARNING: No limits were specified')
            print(' if you want to compute the full lenght of sensors leave empty the next prompts')

            limit1 = input(' Region of interest start point [m]: ')
            limit2 = input(' Region of interest end point [m]: ')

            limit1 = False if limit1 == "" else float(limit1)
            limit2 = False if limit2 == "" else float(limit2)

        else:
            print('No limits were specified, taking ones from seetings')
            # Gets limits from settings
            limit1 = self.settings.z_ini
            limit2 = self.settings.z_fin

    # Generate datasets from selected data
    for key, OBRfile in self.obrfiles.files.items():

        import psutil
        if psutil.virtual_memory()[2] < 90:

            if not hasattr(OBRfile, 'Data') or OBRfile.Data is None:
                # Read .obr file
                f,z,Data = multi_read_OBR([OBRfile.name],os.path.join(self.path,self.folders['OBR']),limit1=limit1,limit2=limit2)
                # Update OBR file register
                OBRfile.f           = f
                OBRfile.z           = z
                OBRfile.Data        = Data[OBRfile.name]
            else:
                pass

        else:
            # Esta parte hay que mejorarla para la 2.0
            print('\nUnable to allocate more information')
            print("DON'T PANIC the information will be saved")
            print('just run again computeOBR() until no more .obr files are read')
            self.save()
            return False

    print('Done!')
    return True

def find_OBR(path:str, verbose=False) -> list:
    """ Function to find all .obr files from a folder

        param:  path      (str)          : path to folder
        return: OBR_files (list of str)  : list of OBR filenames

    """
    # Find all .obr files
    OBR_files = glob.glob(os.path.join(path,'*.obr'))
    print(OBR_files) if verbose else None
    # Keep just filename and extension (basename)
    OBR_files = [os.path.basename(f) for f in OBR_files]
    print(OBR_files) if verbose else None
    return OBR_files

def get_date(file:str) -> str:
    """
    Open an .obr file to get date of the measure

        param: file (str): file to be read
        return: DateTime (str): date formated as %Y,%M,%D,%h:%m:%s

    """

    # Data lecture (all this offsets are heritage from read_OBR())
    offset = np.dtype('<f').itemsize
    offset += np.dtype('|U8').itemsize
    offset = 12 # Ni idea de por qué este offset pero funciona
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('uint16').itemsize
    offset += np.dtype('<d').itemsize
    offset += np.dtype('int32').itemsize
    offset += np.dtype('int32').itemsize
    offset += np.dtype('uint32').itemsize
    offset += np.dtype('uint32').itemsize

    DateTime=np.fromfile(file, count=8,dtype= 'uint16',offset = offset)                              # Measurement date

    DateTime=f'{DateTime[0]},{DateTime[1]},{DateTime[3]},{DateTime[4]}:{DateTime[5]}:{DateTime[6]}'  # "2022,03,03,13:41:27"

    return DateTime

def ID_generator(date:str) -> str:
    
    """Function to create OBRfile ID. Modifies the input date string by removing commas and colons and adds a hyphen between the day and hour.
    
    :param date: Date where the measure was taken, formatted as %Y,%m,%d,%H:%M:%S
    :returns: Date formatted as %Y%m%d-%H%M%S
    
    """
    
    # Replace commas and colons with empty strings
    formatted_date = date.replace(',', '').replace(':', '')
    
    # Insert a hyphen between the day and hour
    formatted_date = formatted_date[:8] + '-' + formatted_date[8:]
    
    return formatted_date
