from rottnest.executables.t_rz_executable import T_RZ_RottnestExecutable

from . import fermi_hubbard_rigetti 

from pyLIQTR.ProblemInstances.getInstance import getInstance
from pyLIQTR.clam.lattice_definitions import SquareLattice
from pyLIQTR.BlockEncodings.getEncoding import getEncoding, VALID_ENCODINGS
from pyLIQTR.qubitization.qsvt_dynamics import qsvt_dynamics, simulation_phases

from . import fermi_hubbard_rigetti 

class FermiHubbard(T_RZ_RottnestExecutable):
    '''
        Fermi Hubbard Model
    '''

    DEFAULT_N = 5
    DEFAULT_p_algo = 0.95
    DEFAULT_times = 1.0

    @staticmethod
    def get_name():
        return 'Fermi-Hubbard'

    @staticmethod
    def get_parameters():
        '''
            Returns the parameters of the executable 
            This can then be passed to the front-end
        '''
        return T_RZ_RottnestExecutable.base_params | {'N':(int, FermiHubbard.DEFAULT_N), 'p_algo':(float, FermiHubbard.DEFAULT_p_algo), 'times':(float, FermiHubbard.DEFAULT_times)}

    def _generate_circuit(self):
        '''
            Dispatch via interface
        '''
        return self._make_fh_circuit()

    def precompute(self):
        '''
            Pre-decompose reflections
            Adjoint
            Prepare Pauli LCU
            Select Pauli LCU 
        '''

# License separation 
FermiHubbard._make_fh_circuit = fermi_hubbard_rigetti.make_fh_circuit
FermiHubbard._make_qsvt_circuit = fermi_hubbard_rigetti.make_qsvt_circuit
