# Quantum BB84

A notebook implementation of BB84 that uses quantum teleportation to transmit
qubits, optionally simulates an eavesdropper, and demonstrates one-time-pad
message encryption.

**[Read the rendered notebook](https://zacaria.github.io/quantum-bb84/)** ·
[Run the live demo](https://mybinder.org/v2/gh/Zacaria/quantum-bb84/master?urlpath=tree/demo.ipynb) ·
[Download the notebook](quantumbb84tp.ipynb) ·
[Archived Jovian page](https://jovian.com/zacaria/quantumbb84tp)

The rendered page keeps the outputs and circuit diagrams preserved by Jovian,
so it can be read without installing the historical Qiskit environment.

## Run live

[![Launch the live demo on Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Zacaria/quantum-bb84/master?urlpath=tree/demo.ipynb)

Binder opens `demo.ipynb` in a temporary Jupyter environment. Change the
values in **Demo controls**, then choose **Kernel → Restart & Run All**.

- `EVE_RATE = 0` demonstrates successful key exchange and decryption.
- `EVE_RATE = 100` deterministically demonstrates Eve being detected.
- Keep the short defaults for a quick presentation; enabling the full hash
  increases the simulated message and therefore the run time.

## Features

- BB84 key generation
- qubit teleportation between Alice and Bob
- optional intercept-and-resend eavesdropping by Eve
- configurable debug output and simulation shot count
- circuit reuse between qubit transmissions
- one-time-pad message encryption with an optional integrity hash

## Run locally

The local launcher recreates the historical Python 3.9/Qiskit 0.37 environment
and handles the legacy Apple Silicon dependency workaround automatically.

```bash
just start
```

The first run requires [`uv`](https://docs.astral.sh/uv/) and may take a few
minutes. Later runs reuse `.venv` and open `demo.ipynb` directly in Brave on
macOS when Brave is installed.

```bash
brew install just uv
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
