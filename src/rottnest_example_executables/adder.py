import cirq

import qmpa

import numpy as np

from qmpa.circuit import Circuit
from qmpa import adapters_cirq 

from rottnest.executables.t_rz_executable import T_RZ_RottnestExecutable  

# Attempt to load pandora_cache
try:
    from rottnest.pandora.pandora_cache import pandora_cache, PandoraCacheOp  
except:
    raise Exception("Pandora Database Not Running")

class StridedCuccaroAdder(T_RZ_RottnestExecutable):
    '''
        Rottnest Adder Shim
    '''

    _circ = None

    @staticmethod
    def get_name():
        return 'Strided Cuccaro Adder'

    @staticmethod
    def get_parameters():
        '''
            Returns the parameters of the executable 
            This can then be passed to the front-end
        '''
        return T_RZ_RottnestExecutable.base_params | {
            'n_qubits':(int, 20),
            'stride':(int, 30),
        }

    def _generate_circuit(self):
        '''
            Dispatch via interface
        '''
        if self._circ is None:
            circ = self.adder(n_qubits=self.stride)
            n_reps = self.n_qubits // self.stride 
          
            self._circ = self.adder(n_qubits=self.stride) 
            for _ in range(n_reps):
                self._circ.append(circ) 
        return self._circ 

    def get_qubits(self):
        '''
            Using list of gates format
            Setting the appropriate qubit 
        '''
        return self._get_qubits_from_list_of_gates()

    def __str__(self):
        '''
        Overloading this field as an example hash
        '''
        return f"adder_{self.n_qubits}"

    def precompute(self, carry=False):
        '''
            Precomputation with or without pandora
        '''
        if self.pandora:
            print("Precompute!: ", self.n_qubits)
            maj = self.maj_slide(n_qubits=self.stride)

            maj_hsh = f'maj_{self.n_qubits}' 
            maj_op = PandoraCacheOp(maj_hsh)

            uma = self.uma_slide(n_qubits=self.stride)
            uma_hsh = f'uma_{self.n_qubits}' 
            uma_op = PandoraCacheOp(uma_hsh)

            pandora_cache.bind_hash(maj, hsh=uma_hsh)
            pandora_cache.bind_hash(uma, hsh=maj_hsh)

            # Naive
            n_reps = self.n_qubits // self.stride + 1
            self._circ = [maj_op] * n_reps + [uma_op] * n_reps 
            #return
        #else:
        #    # Remove this after benchmarking
        #    adder = self.adder()
        #    add_hsh = f'add_{self.n_qubits}' 
        #    add_op = PandoraCacheOp(add_hsh)

        #    pandora_cache.bind_hash(adder, hsh=add_hsh)

        #self._circ = self._generate_circuit() 

    def decompose(self, *args, **kwargs):
        return [self.op] 

    def adder(self, n_qubits=None):
        '''
            Create the adder circuit
        '''
        if n_qubits is None:
            n_qubits = self.n_qubits
        c = Circuit()
        r_a = c.register(n_qubits, 'A')
        r_b = c.register(n_qubits + 1, 'B')
        c.add(r_a, r_b)

        cirq_circuit = adapters_cirq.to_cirq(c)
        return cirq.decompose(cirq_circuit)


    def maj_slide(self, n_qubits=None):

        if n_qubits is None:
            n_qubits = self.n_qubits
        c = Circuit()
        reg_a = c.register(n_qubits, 'A')
        reg_b = c.register(n_qubits + 1, 'B')

        # Conditional alloc on reg_carry
        reg_carry = c.anc_register(1)
        
        # MAJ with carry
        c.MAJ(reg_a[0], reg_b[0], reg_carry[0])
        
        # MAJ sequence
        for i in range(1, n_qubits):
            c.MAJ(reg_a[i], reg_b[i], reg_a[i - 1])

        cirq_circuit = adapters_cirq.to_cirq(c)
        return cirq.decompose(cirq_circuit)

    def uma_slide(self, n_qubits=None):

        if n_qubits is None:
            n_qubits = self.n_qubits
        c = Circuit()
        reg_a = c.register(n_qubits, 'A')
        reg_b = c.register(n_qubits + 1, 'B')

        # Conditional alloc on reg_carry
        reg_carry = c.anc_register(1)
        
        # UMA Sequence
        for i in range(n_qubits - 1, 0, -1):
            c.UMA(reg_a[i], reg_b[i], reg_a[i - 1])
        
        # UMA with carry
        c.UMA(reg_a[0], reg_b[0], reg_carry[0])

        cirq_circuit = adapters_cirq.to_cirq(c)
        return cirq.decompose(cirq_circuit)

