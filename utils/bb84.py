import numpy as np
# from qiskit import QuantumCircuit
from braket.circuits import Circuit, Observable
import os


def initialize_protocol(number_of_qubits):
    encoding_basis = np.random.randint(2, size=number_of_qubits)
    alice_states = np.random.randint(2, size=number_of_qubits)
    measurement_basis = np.random.randint(2, size=number_of_qubits)
    return encoding_basis, alice_states, measurement_basis


def encode_qubits(number_of_qubits, alice_states, encoding_basis):
    # To encode 0, no action is needed. To encode state 1 - an X gate (NOT) is applied to the qubit (circuit.x).
    # To encode in computational basis - no action needed. To encode in the Hadamard basis - apply Hadamard gate (circuit.h).

    circuit = Circuit()
    for idx in range(len(encoding_basis)):
        if alice_states[idx] == 1:
            circuit.x(idx)
        else:
            circuit.i(idx)
        if encoding_basis[idx] == 1:
            circuit.h(idx)

    return circuit


def measure_qubits(circuit, measurement_basis):
    # circuit - a QuantumCircuit() object
    # measurement_basis: array of 0s and 1s denoting the basis to be used for measurement
    #                   0 - Rectilinear (Computational) Basis
    #                   1 - Diagonal (Hadamard) Basis

    for i in range(len(measurement_basis)):
        if measurement_basis[i] == 1:
                circuit.h(i)  
    #circuit.measure_all()
    return circuit


def filter_qubits(measured_bits, alice_basis, bob_basis):
    # alice_basis, bob_basis - have to be parsed as strings
    max_range = min(len(bob_basis), len(alice_basis))
    to_keep = np.array([int(measured_bits[i]) for i in range(max_range) if bob_basis[i]==alice_basis[i]])
    return to_keep


def array_to_string(array):
    result = np.array2string(
        array, 
        separator="", 
        max_line_width=(len(array)+3))
    return result.strip('[').strip(']')


def get_circuit_size(filename, safety_buffer=16):
    # Determine size of quantum circuit in bytes (can encode numbers up to 8 digits)
    # A circuit with 10_000 qubits takes 508890 bytes so 8 digits should be enough for our purpose.
    circuit_size = os.path.getsize(filename) + safety_buffer
    circuit_size_string = str(circuit_size).zfill(8)
    return circuit_size_string