import os
import pandas as pd
import pickle

def import_book(self,path=None):
    
    """ Overwrite the book with an external one """
    
    # Set default if None
    if not path:  
        path = self.book_path

    # Check if the book exists
    if not os.path.exists(path):
        raise('ERROR: No book (.csv) found with path ' + path)
    
    # Update book
    self.book = pd.read_csv(path)

    # Update book_path
    self.book_path = path 

    print(f'<--- Book loaded from: '+ self.book_path)

    return self.book

def import_obj(self,path=None):
    
    """ Overwrite the object """

    # Set default if None
    if not path:
        path = self.obj_path 

    # Check if the book exists
    if not os.path.exists(self.book_path):
        raise('ERROR: No object (.pkl) found with path: ' + path)

    # Update object
    with open(path, 'rb') as inp:
        self.__dict__ = pickle.load(inp)

    # Update path
    self.obj_path = path

    print(f'<--- Object loaded from: '+ self.obj_path)

    return self