import os

def fuego_purificador(self):
    """ Function which deletes every file created by the object (even the object.pkl copy)"""

    files_to_burn = [
        os.path.join(self.path,self.name),
        self.obrfiles.book_path,
        self.obrfiles.obj_path,
        self.settings.book_path,
        self.settings.obj_path,
        self.slices.book_path,
        self.slices.obj_path
    ]

    for file_path in files_to_burn:
        if file_path:
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file: {file_path}\n{str(e)}")