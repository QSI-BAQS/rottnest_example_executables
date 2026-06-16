# Collect all executables from this module

from .fermi_hubbard import FermiHubbard
from .fermi_hubbard_nnn import FermiHubbardNNN
from .heisenberg import Heisenberg 
from .transverse_field_ising import TransverseFieldIsing


rottnest_executables = [
    FermiHubbard,
    Heisenberg,
    FermiHubbardNNN,
    TransverseFieldIsing
]

try:
    # Requires QMPA library
    from .adder import StridedCuccaroAdder
    rottnest_executables.append(StridedCuccaroAdder)
except:
    pass

