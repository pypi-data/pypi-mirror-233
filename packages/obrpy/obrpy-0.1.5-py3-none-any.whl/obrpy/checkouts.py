import os

def OBR_checkout(self, verbose=True):

    """ OBR checkout """

    # Check if OBRfiles are already computed
    if len(self.obrfiles.files) == 0:
        print('No obrfiles created, creating and computing ...') if verbose else None
        self.mainOBR()

    if not any([hasattr(obrfile, 'Data') for key, obrfile in self.obrfiles.files.items()]):
        print('No data in obrfiles, computing...') if verbose else None
        self.computeOBR()
    else:
        print('OBR data already computed') if verbose else None
        pass

def slices_checkout(self):

    # Check if slices were previously created
    if not isinstance(self.slices,bool) and len(self.slices.slices) != 0 : 
        ans = input('\nSLICES already computed (append/overwrite/quit):')
        if 'a' in ans:
            return True
        if 'o' in ans:
            self.clear_slices()
            return True
        if 'q' in ans:
            return False
    else:
        return True

def dataset_checkout(self):
    
    # Check if dataset already exists
    if not isinstance(self.dataset,bool) and not self.dataset.data.empty: 
        ans = input('\nDATASET already computed (append/overwrite/quit):')
        if 'a' in ans:
            return True
        if 'o' in ans:
            self.clear_dataset()
            return True
        if 'q' in ans:
            return False
    else:
        return True