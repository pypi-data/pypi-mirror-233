class Signal(object):

    """ Class to contain all singal analysis functions available """

    def __init__(self) -> None:
        pass

    from .cross_spectrum import PSSS
    from .spectral_shift import spectral_shift, spectral_shift_GPU