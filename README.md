# Quantum BB84

A notebook implementation of BB84 that uses quantum teleportation to transmit
qubits, optionally simulates an eavesdropper, and demonstrates one-time-pad
message encryption.

**[Read the rendered notebook](https://zacaria.github.io/quantum-bb84/)** ·
[Download the notebook](quantumbb84tp.ipynb) ·
[Archived Jovian page](https://jovian.com/zacaria/quantumbb84tp)

The rendered page keeps the outputs and circuit diagrams preserved by Jovian,
so it can be read without installing the historical Qiskit environment.

## Features

- BB84 key generation
- qubit teleportation between Alice and Bob
- optional intercept-and-resend eavesdropping by Eve
- configurable debug output and simulation shot count
- circuit reuse between qubit transmissions
- one-time-pad message encryption with an optional integrity hash

## Run locally

The notebook was written for Python 3.9 and Qiskit 0.37 in July 2022.

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook quantumbb84tp.ipynb
```

`utils.py` and `otpUtils.py` must remain beside the notebook. Both files were
recovered from the original local project rather than reverse-engineered from
the notebook output.

## Tests

```bash
python -m unittest discover -s tests -v
```

## GitHub Pages

`docs/index.html` is a static `nbconvert` rendering of the notebook and its
preserved outputs. Regenerate it after changing the notebook with:

```bash
jupyter nbconvert --to html --output index --output-dir docs quantumbb84tp.ipynb
```
