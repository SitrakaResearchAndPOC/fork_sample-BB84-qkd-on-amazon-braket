# BB84 Quantum Key Distribution with Noise and Golay Error Correction

This project demonstrates a realistic implementation of the BB84 Quantum Key Distribution (QKD) protocol using Amazon Braket, incorporating quantum channel noise and classical error correction via the [24,12,8] Golay code. It simulates the full QKD pipeline—from qubit encoding to secure key reconciliation—entirely in Python.

## 🚀 Features

- BB84 protocol simulation using quantum circuits
- Bit-flip noise modeling to emulate quantum channel imperfections
- Basis reconciliation and key sifting
- Error correction using the [24,12,8] Golay code
- Modular design for reuse and customization
- Powered by Amazon Braket's density matrix simulator (`braket_dm`)

## 📁 Project Structure

```
bb84-with-noise-and-golay/
│
├── bb84-with-noise-and-golay.ipynb      # Main notebook for step-by-step protocol simulation
└── utils/
    ├── bb84.py                          # BB84 core protocol logic
    ├── error_correction.py             # Syndrome calculation and key reconciliation
    ├── golay_code.py                   # Golay code matrices and encoding functions
    ├── secret_utils.py                 # Key conversion utilities
    └── __init__.py
```

## 🔧 Requirements

- Python 3.10+
- Amazon Braket SDK
- NumPy
- Jupyter Notebook

Install dependencies:

pip install amazon-braket-sdk numpy

## ▶️ Running the Demo

1. Launch Jupyter Notebook:

   jupyter notebook bb84-with-noise-and-golay.ipynb

2. Step through each section:
   - Quantum state preparation and measurement
   - Bit-flip noise injection
   - Basis sifting and raw key extraction
   - Golay-based error correction and final key reconciliation

## ⚙️ Configuration Parameters

| Parameter                     | Description                                                       | Default |
|------------------------------|-------------------------------------------------------------------|---------|
| BIT_FLIP_PROBABILITY         | Probability of bit-flip error to simulate quantum channel noise   | 0.1     |
| NUMBER_OF_QUBITS             | Qubits per round; should match Golay block size for alignment     | 12      |
| ERROR_CORRECTION_CHUNK_SIZE  | Number of bits needed before applying error correction             | 12      |

## 💡 Business Value

This project showcases how quantum cryptography can be implemented and tested in a simulated cloud environment. It enables businesses and researchers to evaluate QKD under noisy conditions and explore how classical error correction (e.g., the Golay code) enhances key reliability and integrity.

## 👥 Authors

- Miriam Kosik – Quantum Blockchains (kosik@quantumblockchains.io)
- Juan Moreno – AWS Quantum Networks Engineering (juanmb@amazon.com)
- Xinhua Ling – AWS Quantum Networks Engineering

## 📄 License

MIT-0


