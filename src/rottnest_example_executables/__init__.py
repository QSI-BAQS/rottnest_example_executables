from .fermi_hubbard import FermiHubbard

rottnest_executables = [
    FermiHubbard,
]

try:
    from .adder import StridedCuccaroAdder
    rottnest_executables.append(StridedCuccaroAdder)
except:
    pass

