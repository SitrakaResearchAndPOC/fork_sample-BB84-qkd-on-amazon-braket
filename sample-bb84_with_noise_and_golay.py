import base64
import numpy as np

from braket.circuits import noises
from braket.devices import LocalSimulator

from utils.bb84 import initialize_protocol, encode_qubits, measure_qubits, filter_qubits, array_to_string
from utils.golay_code import GolayCode
from utils.secret_utils import convert_to_octets

# ---

BIT_FLIP_PROBABILITY = 0.1          # probability of bit flip - should work fine up to probability of about 0.25
NUMBER_OF_QUBITS = 12               # only change this line if you are sure you know what you're doing :)
ERROR_CORRECTION_CHUNK_SIZE = 12    # do not change this line in this notebook

alice_raw_key = np.array([])
bob_raw_key = np.array([])

# ---

# Generate key material until there are 12 bits of raw key

while len(alice_raw_key) < ERROR_CORRECTION_CHUNK_SIZE:

    # For Alice, the important basis is encoding basis.
    encoding_basis_A, states_A, _ = initialize_protocol(NUMBER_OF_QUBITS)
    
    # Print the initial state of Alice
    sent_bits = array_to_string(states_A)

    # For Bob, the relevant basis is measurement basis.
    _, _, measurement_basis_B = initialize_protocol(NUMBER_OF_QUBITS)

    # Alice encodes the values of her qubits using according bases from `encoding_bases_A`.  
    # This is stored as a Qiskit quantum circuit.  
    encoded_qubits_A = encode_qubits(NUMBER_OF_QUBITS, states_A, encoding_basis_A)

    # Transmission of encoded qubits to Bob - might add noise!
    noise = noises.BitFlip(probability=BIT_FLIP_PROBABILITY)
    encoded_qubits_A.apply_gate_noise(noise)

    # Bob performs measurement on the received qubits
    measured_circuit = measure_qubits(encoded_qubits_A, measurement_basis_B)
    device = LocalSimulator("braket_dm")
    result = device.run(measured_circuit, shots=1).result()
    measured_bits = list(result.measurements[0])

    # After Bob has measured the qubits, he sends his measurement bases to Alice. 
    # She responds to Bob by sending him her encoding bases. Now both parties know both the encoding basis and measurement basis for each qubit.   
    # In the key sifting phase, both sides keep only the qubits for which encoding basis and measurement basis were the same.      
    alice_raw_key = np.concatenate( (alice_raw_key, filter_qubits(sent_bits, encoding_basis_A, measurement_basis_B)) ) 
    bob_raw_key = np.concatenate( (bob_raw_key, filter_qubits(measured_bits, encoding_basis_A, measurement_basis_B)) )


# ---

alice_raw_key = alice_raw_key[:12]
alice_raw_key

# ---

bob_raw_key = bob_raw_key[:12]
bob_raw_key

# ---

error_correcting_code = GolayCode()

generator_matrix = error_correcting_code.get_generator_matrix()
parity_check = error_correcting_code.get_parity_check_matrix()
b_matrix = error_correcting_code.get_b_matrix()

# ---

encoded_key_A = np.matmul(generator_matrix, alice_raw_key) % 2
print(f'Key of Alice after encoding is: {encoded_key_A}')
syndrome_A = np.matmul(encoded_key_A, parity_check) % 2
print(f'Syndrom of Alice (should be all zero): {syndrome_A}')
parity_bits = encoded_key_A[12:]
print(f'Information sent to Bob: {parity_bits}')

# ---

encoded_key_B = np.concatenate((bob_raw_key, parity_bits))
print(encoded_key_B)
syndrome_B = np.matmul(encoded_key_B, parity_check) % 2
print(syndrome_B)
syndrome_BB = np.matmul(syndrome_B, b_matrix) % 2
syndrome_BB

# ---

if syndrome_BB.sum() < 4:
    correction_mask = np.concatenate((syndrome_BB, np.zeros(12,)))
    print(correction_mask)
else:
    print("Decoding failed - more than 3 errors")

# ---

corrected_key = np.mod(bob_raw_key + correction_mask[:12], 2).astype(int)
corrected_key

# ---

corrected_key == alice_raw_key

# ---

ASCII_key = base64.b64encode(convert_to_octets(array_to_string(corrected_key))).decode('ascii')
print(ASCII_key)