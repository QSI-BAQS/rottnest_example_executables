from functools import reduce

# These hashes are already technically in the default set
# But this tests the loading logic
from rottnest.monkey_patchers.default_hashes.pyliqtr_hashes import pauli_lcu, qsp, qsvt, qubitized_operations

from rottnest.monkey_patchers.default_hashes.qualtran_hashes import lcu, mct 

cirq_hashes = {}

qualtran_hashes = reduce(
    lambda x, y:  x | y.TARGETS,
    (lcu, mct,),
    {}
)

pyliqtr_hashes = reduce(
    lambda x, y:  x | y.TARGETS,
    (pauli_lcu, qsp, qsvt, qubitized_operations,),
    {}
)
