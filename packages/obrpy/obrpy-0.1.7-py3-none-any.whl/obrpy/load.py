import os
import pickle
import shutil

def load(self,path=None) -> None:
    """ Load the object existing in the root of the folder """

    if not path:
        path = os.path.join(self.path,self.name)

    new_path = self.path
    new_name = self.name

    with open(path, 'rb') as inp:
        self.__dict__ = pickle.load(inp)

    self.path = new_path
    self.name = new_name

    print(f'<--- {self.name} loaded!')

    return self

def new(self) -> None:

    """ Creates a new obrpy folder structure and initializes atributes and objects """

    # Folder structure
    self.folders = {'OBR' : './0_OBR'}

    # Creates folder structure if not exists
    for key,val in self.folders.items():
        if not os.path.exists(os.path.join(self.path,val)):
            os.makedirs(os.path.join(self.path,val))

    # Move all .obr files to its folder, if they exists
    for file in os.listdir(self.path):
        if file.endswith('.obr'):
            print('Moving',file,'to',self.folders['OBR'])
            shutil.move(os.path.join(self.path,file), os.path.join(self.path,self.folders['OBR'],file))


    ######### Other atributes inicialization  #########

    # OBRfiles
    self.obrfiles = self.OBRfiles()

    # Settings
    self.settings = self.Settings(None)

    # Slices
    self.slices = self.Slices()

    # Dataset 
    self.dataset = self.Dataset()

    # Signal
    self.signal = self.Signal()

    # Zero layers
    self.zeroLayers = self.ZeroLayers()