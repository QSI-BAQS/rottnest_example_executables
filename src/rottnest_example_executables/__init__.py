# Collect all executables from this module

from .fermi_hubbard import FermiHubbard
from .fermi_hubbard_nnn import FermiHubbardNNN
from .heisenberg import Heisenberg 


rottnest_executables = [
    FermiHubbard,
    Heisenberg,
    FermiHubbardNNN
]

try:
    # Requires QMPA library
    from .adder import StridedCuccaroAdder
    rottnest_executables.append(StridedCuccaroAdder)
except:
    pass

