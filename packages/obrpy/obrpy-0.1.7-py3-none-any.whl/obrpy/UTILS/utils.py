def printProgressBar(iteration, total,prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    if float(percent) < 100:
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        return False
    elif float(percent) >= 100:
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\n')
        return True
    else:
        print(percent)
        

def find_index(array,value):

    """ Function to determine the closest index to some value within an array
        
        :param array (list) :   list to be evaluated
        :param value (float/array):   value (or values) to reach

        :return idx  (int/list)  :   index (or indexes if value is array)
    """

    import numpy as np

    array = np.asarray(array)

    if isinstance(value, int) or isinstance(value, float):
        idx = (np.abs(array - value)).argmin()
        return idx

    elif isinstance(value, list) or type(value).__module__ == np.__name__:
        idx = list()
        for val in value:
            idx.append((np.abs(array - val)).argmin())
        return idx
    else:
        print(f'find_index() error [Type not suported: {type(value)}]')
        exit()

def get_all_files(path,verbosity = False,extension=False,file_extension='.obr'):
    """ Get all binaries filenames from a path 
        
        :param: path (str): path to directory where files will be found (also within its subdirectories)
        
        :optional: verbosity (bool) = False : False for no prints
        :optional: extension (bool) = False : False to not append extension in the return
        :optional: file_extension (str) = '.obr': Extension of the files to be found

        :return binaries (list): list with the path to each file (with or without extension)


    """

    import os

    binaries = []
    for root, dirs, files in os.walk(path):
        print((len(path) - 1) * '---', os.path.basename(root)) if verbosity == True else False
        for file in files:
            print(len(path) * '---', file) if verbosity == True else False
            if file.endswith(file_extension):
                if extension == False:
                    binaries.append(file.split('.')[0])
                elif extension == True:
                    binaries.append(file)

    try:
        # Split filenames and get the first number
        order = list()
        for file in binaries:
            try:
                num =  float(file.split('_')[0])
                order.append([num , file])
            except:
                try:
                    num =  float(file.split('.')[0])
                    order.append([num , file])
                except:
                    pass
        # Sort files using the num-> file correspondence  in "order"
        if order != []:
            binaries = [file for num,file in sorted(order, key = lambda x:x[0])]
    except:
        pass


    return binaries

def get_times(file):
    """ Function to get elapsed time in (HH:MM:SS) format second column of a csv
        where elapsed time is specified in seconds.

        : param file   (string): path to file

        : retrun times (np.array): array with elapsed times
    """

    import numpy as np
    import pandas as pd
    import time

    # Read file
    data = pd.read_csv(file, sep=',', header=None)

    # Convert to numpy array
    data = data.values

    # Get values
    elapsed_time = data[:, 1]
    # Change format
    times = np.array([time.strftime('%H:%M:%S', time.gmtime(t)) for t in elapsed_time])

    return times

def create_onedrive_directdownload(onedrive_link):
    """ Function to create a One Drive direct download link from the sharing link generated there

        :param: onedrive_link (str): One Drive sharing link generated in One Drive

        :return: resultUrl (str): Direct downloadeabled link
    """

    import base64
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

def find_OBR(path):
    """ Function to find all .obr files from a folder

        param: path (string): path to folder
        return: OBR_files (list of string): list of OBR filenames

    """
    import glob
    import os
    # Find all .obr files
    OBR_files = glob.glob(os.path.join(path,'0_OBR','*.obr'))
    # Keep just filename and extension
    OBR_files = [os.path.basename(f) for f in OBR_files]
    return OBR_files

def sort_OBR(OBR_files):
    """ Funtion to sort OBR by the first number (before '_' splitter)

        param: OBR_files (list of string) : list of OBR filenames
        return: OBR_files (list of string) : list of OBR filenames sorted

    """
    import re
    OBR_files.sort(key=lambda x: int(re.findall('\d+', x)[0]))
    return OBR_files

def remove_extension(OBR_files):

    """ Function to remove the extension '.obr' of a bunch of '.obr' files

        :param:  OBR_files (list): '.obr' files' filenames with extension
        :return: OBR_files (list): '.obr' files' filenames without extension
    
    """

    return [OBR_file.replace('.obr','') for OBR_file in OBR_files]

def find_all_OBR(path):

    """ Function to find, sort and remove extension of all '.obr' files contained in path
    
        :param:  path (string): path to folder
        :return: OBR_files (list): '.obr' files' filenames without extension"""

    OBR_files = find_OBR(path)
    OBR_files = sort_OBR(OBR_files)
    OBR_files = remove_extension(OBR_files)

    return OBR_files

def check_memory(percentage=90,timeout = 60):

    """ Function to check memory already available

        :optional percentage (float) = 90: non crossing percentage
        :optional timeout    (float) = 60: [s] elapsed time after closing program

    """

    import time
    import psutil

    zero_time = float(time.time())
    while psutil.virtual_memory()[2] > percentage:
        print('Waiting for memory')
        time.sleep(1)
        if float(time.time())-zero_time > timeout:
            exit()


def dict_from_multiplekeys(keys,base=None):

    """ Function to create two nested dictionaries with three levels of deepth.

            :param: keys (list):    List (three elements for the three levels) 
                                    of list keys which will be used as keys for dictionaries
            :optional: base = None:     Whatever to be included in each of the lowest
                                        level of the nested dictionaries

            :return multikeys (dict):   Nested dictionary which contains labels (str) used
                                        for the representation of the values storaged in the
                                        other dictionary
            :return multidict (dict):   Nested dictionary which contains 'base' in each place
                                       

        This function was created to perform signal analysis therefore the three 
        levels are: 

            magnitudes  (m)
            domains     (d)
            operations  (o)
    
        the nested dictionaries keys will be ordered as follows:

            multikeys[m][d][o]
            multidict[m][d][o]

        and multikeys values are formatted as:
            
            if o is None:
                multikeys[m][d][o] = m+'$($'+d+'$)$'
            else:
                multikeys[m][d][o] = m+'$($'+d+'$)$'+o+m+'$_0($'+d+'$)$'

    """

    from copy import deepcopy

    if isinstance(keys[0],list):
        magnitudes  = keys[0]
        domains     = keys[1]
        operations  = keys[2]

        multidict = dict.fromkeys(magnitudes)
        multikeys = dict.fromkeys(magnitudes)
        for m in magnitudes:
            multidict[m] = dict.fromkeys(domains)
            multikeys[m] = dict.fromkeys(domains)
            for d in domains:
                multidict[m][d] = dict.fromkeys(operations)
                multikeys[m][d] = dict.fromkeys(operations)
                for o in operations:
                    multidict[m][d][o] = deepcopy(base)
                    if o is None:
                        multikeys[m][d][o] = m+'$($'+d+'$)$'
                    else:
                        multikeys[m][d][o] = m+'$($'+d+'$)$'+o+m+'$_0($'+d+'$)$'

    return multikeys, multidict

def magnitude_interpolation(x,y=None,plot=False):
    """ Function to interpolate a magnitude
    
    :optional y = None

    if y is None
        :param: x (np.array): values to be interpolated (assuming equispaced)
        :return interp_y1 (np.array): values interpolated
    
    else
        :param: x (np.array): x-axis coordinates of the values
        :param: y (np.array): y-axis coordinates of the values
        :return interp_y1 (np.array): y-axis values interpolated (x-axis values are the same)

    :optional plot (bool) = False: Set True to visualize the interpolation stages

    

    """

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import CubicSpline

    if y == None:
        y = np.array(x)
        x = np.linspace(0,1,len(y))
    else:
        y = np.array(y)
        x = np.array(x)

    step_index = np.where(np.diff(y) != 0)[0]
    step_ini = np.append(0,step_index+1)           # Inicio del escalón
    step_fin = np.append(step_index,len(x)-1)      # Final del escalón

    step_width  = x[step_fin] - x[step_ini]        # Ancho de los escalones
    step_center = x[step_ini] + step_width/2       # Centro de los escalones

    # Linear interpolation

    new_y = np.interp(x,step_center,y[step_ini])

    # Cubic interpolation

    new_x = np.linspace(0,1,10*len(y))

    cs =  CubicSpline(x, new_y)
    interp_y1 = np.interp(x,new_x,cs(new_x))

    if plot:

        plt.figure()
        plt.plot(x,y,'-o',label='original')
        plt.plot(x[step_ini],y[step_ini],'>',label='step_ini')
        plt.plot(x[step_fin],y[step_fin],'<',label='step_fin')
        plt.plot(step_center,step_width,'^',label='step_width')
        plt.plot(step_center,y[step_ini],'-P',label='step_center')
        plt.plot(x,new_y,'-x',label='interp1')
        plt.plot(x,interp_y1,'-v',label='interp2')
        plt.grid()
        plt.legend()
        plt.show()


    return interp_y1
