import os
import pickle as pickle
import pandas as pd

def export_book(self, path=None):

    """ 
    Saves the dict of objects as a .csv. The .csv will not contain "f", "z", and "Data" values but the DataFrame will do.
    """

    # Launch GUI if no path is provided
    if not path:
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension='.csv',title=self._export_book_message)

    # Check extension
    if not path.endswith(".csv"):
        path = os.path.splitext(path)[0] + ".csv"
    
    # Update path
    self.book_path = path

    # Create book
    self.create_book()

    # Drop the columns from the DataFrame
    modified_df = self.book.drop(columns=self.exclude_columns) if isinstance(self.exclude_columns, list) and len(self.exclude_columns) > 0 else self.book

    # Export the modified DataFrame to CSV
    modified_df.to_csv(self.book_path, index=False)

    print('--> book saved in', self.book_path)

    return self.book

def export_obj(self, path = None) -> None:
    
    """ Function to save an object with pickle
        :param: object_to_save (obj): object to be saved
        :param: path_to (str): path to the directory where the object will be saved
    """
    
    # Launch GUI if no path is provided
    if not path:
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(defaultextension='.pkl',title=self._export_obj_message)

    # Check extension
    if not path.endswith(".pkl"):
        path = os.path.splitext(path)[0] + ".pkl"

    # Update path
    self.obj_path = path

    # Export with pickle
    with open(self.obj_path, 'wb') as outp:
        pickle.dump(self.__dict__, outp, pickle.HIGHEST_PROTOCOL)
    
    print('--> object saved in',self.obj_path)

    return self