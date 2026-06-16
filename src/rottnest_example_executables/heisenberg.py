from rottnest.executables.t_rz_executable import T_RZ_RottnestExecutable

from . import fermi_hubbard_rigetti 

from pyLIQTR.ProblemInstances.getInstance import getInstance
from pyLIQTR.clam.lattice_definitions import SquareLattice
from pyLIQTR.BlockEncodings.getEncoding import getEncoding, VALID_ENCODINGS
from pyLIQTR.qubitization.qsvt_dynamics import qsvt_dynamics, simulation_phases

from . import fermi_hubbard_rigetti 
#from . import fermi_hubbard_hashes

class Heisenberg(T_RZ_RottnestExecutable):
    '''
        Heisenberg Model
    '''

    instance_name = "Heisenberg"

    DEFAULT_p_algo = 0.99998
    DEFAULT_times = 0.1 

    DEFAULT_HEIGHT = 4
    DEFAULT_WIDTH = 4
    
    DEFAULT_J = (1.0, 1.0, 1.0)
    DEFAULT_h = (0.5, 0.0, 0.5) 

    @staticmethod
    def get_name():
        return 'Heisenberg'

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
 'J_x':(float, Heisenberg.DEFAULT_J[0]),
 'J_y':(float, Heisenberg.DEFAULT_J[1]),
 'J_z':(float, Heisenberg.DEFAULT_J[2]),
 'h_x':(float, Heisenberg.DEFAULT_h[0]),
 'h_y':(float, Heisenberg.DEFAULT_h[1]),
 'h_z':(float, Heisenberg.DEFAULT_h[2]),
    }

    def _generate_circuit(self):
        '''
            Dispatch via interface
        '''
        return self._make_heisenberg_circuit()

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
    
    def _make_heisenberg_circuit(self):
        """
            Helper function to build Fermi-Hubbard circuit.
        """

        # Create Heisenberg model instance
        model = getInstance(self.instance_name,
            shape=(self.height, self.width),
            J=(self.J_x, self.J_y, self.J_z),
            h=(self.h_x, self.h_y, self.h_z),
            cell=SquareLattice
        )
        return self._make_qsvt_circuit(
            model,
            encoding=getEncoding(VALID_ENCODINGS.PauliLCU)
        )

    def _make_qsvt_circuit(
            self,
            model,
            encoding,
            ):
        """
            Make a QSVT based circuit from pyLIQTR
        """
        eps = (1 - self.p_algo) / 2
        scaled_times = self.times * model.alpha
        phases = simulation_phases(
            times=scaled_times,
            eps=eps,
            precompute=False,
            phase_algorithm="random")
        gate_qsvt = qsvt_dynamics(encoding=encoding, instance=model, phase_sets=phases)

        return gate_qsvt.circuit
