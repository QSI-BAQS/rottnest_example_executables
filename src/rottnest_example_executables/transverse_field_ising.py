'''
    Transverse Field Ising Model
'''
from rottnest.executables.t_rz_executable import T_RZ_RottnestExecutable
from pyLIQTR.ProblemInstances.getInstance import getInstance
from pyLIQTR.BlockEncodings.getEncoding import getEncoding, VALID_ENCODINGS


from pyLIQTR.clam.lattice_definitions import SquareLattice


from . import Heisenberg

class TransverseFieldIsing(Heisenberg):
    '''
        Transverse Field Ising Model
    '''

    instance_name = "TransverseFieldIsing"

    DEFAULT_p_algo = 0.99998
    DEFAULT_times = 0.1 

    DEFAULT_J = 1.0
    DEFAULT_H = 0.0 
    DEFAULT_G = -1.0


    @staticmethod
    def get_name():
        return 'TransverseFieldIsing'

    @staticmethod
    def get_parameters():
        '''
            Returns the parameters of the executable 
            This can then be passed to the front-end
        '''
        return T_RZ_RottnestExecutable.base_params | {
            'height':(int, Heisenberg.DEFAULT_HEIGHT),
            'width':(int, Heisenberg.DEFAULT_WIDTH),
            'p_algo':(float, Heisenberg.DEFAULT_p_algo),
            'times':(float, Heisenberg.DEFAULT_times),
            'J':(float, TransverseFieldIsing.DEFAULT_J),
            'h':(float, TransverseFieldIsing.DEFAULT_H),
            'g':(float, TransverseFieldIsing.DEFAULT_G)
        }

    def _generate_circuit(self):
        '''
            Dispatch via interface
        '''
        return self._make_transverse_field_ising_circuit()

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
    
    def _make_transverse_field_ising_circuit(self):
        """
            Helper function to build the Ising circuit.
        """

        # Create Transverse Field Ising model instance
        model = getInstance(self.instance_name,
            shape=(self.height, self.width),
            J=self.J,
            h=self.h,
            g=self.g,
            cell=SquareLattice
        )
        return self._make_qsvt_circuit(
            model,
            encoding=getEncoding(VALID_ENCODINGS.PauliLCU)
        )
