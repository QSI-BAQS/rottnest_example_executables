from functools import partial

from rottnest.executables.t_rz_executable import T_RZ_RottnestExecutable

from . import fermi_hubbard_rigetti 

from pyLIQTR.ProblemInstances.getInstance import getInstance
from pyLIQTR.clam.lattice_definitions import SquareLattice
from pyLIQTR.BlockEncodings.getEncoding import getEncoding, VALID_ENCODINGS
from pyLIQTR.qubitization.qsvt_dynamics import qsvt_dynamics, simulation_phases

from . import fermi_hubbard_rigetti 

class FermiHubbardNNN(T_RZ_RottnestExecutable):
    '''
        Fermi Hubbard Model
    '''

    instance_name = "FermiHubbardNNN"
    DEFAULT_N = 4
    DEFAULT_p_algo = 0.99998
    DEFAULT_times = 0.1 
    
    DEFAULT_J1 = -1.0 
    DEFAULT_J2 = -1.0 
    DEFAULT_U = 4.0 

    @staticmethod
    def get_name():
        return 'Fermi-Hubbard Next-Nearest-Neighbour'

    @staticmethod
    def get_parameters():
        '''
            Returns the parameters of the executable 
            This can then be passed to the front-end
        '''
        return T_RZ_RottnestExecutable.base_params | {
'N':(int, FermiHubbardNNN.DEFAULT_N),
'p_algo':(float, FermiHubbardNNN.DEFAULT_p_algo),
'times':(float, FermiHubbardNNN.DEFAULT_times),
'J1':(float, FermiHubbardNNN.DEFAULT_J1),
'J2':(float, FermiHubbardNNN.DEFAULT_J2),
'U':(float, FermiHubbardNNN.DEFAULT_U)
    }

    def _generate_circuit(self):
        '''
            Dispatch via interface
        '''
        return self._make_fh_circuit()

    @classmethod
    def pyliqtr_patchers(cls) -> dict:
        '''
            Hash functions for pyliqtr objects
        '''
        return {}
        #return fermi_hubbard_hashes.pyliqtr_hashes

    @classmethod
    def qualtran_patchers(cls) -> dict: 
        '''
            Hash functions for quatlran objects
        '''
        return {}
        #return fermi_hubbard_hashes.qualtran_hashes

    @classmethod
    def cirq_patchers(cls) -> dict:
        '''
            Hash functions for cirq objects
        '''
        return {}
        #return fermi_hubbard_hashes.cirq_hashes



    def precompute(self):
        '''
            Pre-decompose reflections
            Adjoint
            Prepare Pauli LCU
            Select Pauli LCU 
        '''

    def _make_fh_circuit(self):
        """
            Helper function to build Fermi-Hubbard circuit.
        """

        # Create Fermi-Hubbard Instance
        model = getInstance(
            self.instance_name,
            shape=(self.N, self.N),
            J1=self.J1,
            J2=self.J2,
            U=self.U,
            cell=SquareLattice
        )
        return self._make_qsvt_circuit(
            model,
            encoding=getEncoding(VALID_ENCODINGS.PauliLCU)
        )



# License separation 
FermiHubbardNNN._make_qsvt_circuit = fermi_hubbard_rigetti.make_qsvt_circuit
