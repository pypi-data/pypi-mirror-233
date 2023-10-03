# File converter

Fast converter using Python and Rust.

## Binding

Binding between Rust and Python is done using [PyO3](https://github.com/PyO3/pyo3), a library like PyBind11 for C++.

Check [Userguide](https://pyo3.rs/).

## Build

Create venv and build the Rust lib. Needs also Rust installation. https://www.rust-lang.org/tools/install

```bash
sudo apt install libopencv-dev clang libclang-dev

python3 -m venv .env
source .env/bin activate
pip install -r requirements.txt

# Test:
maturin develop -r

# Publish:
maturin publish -i python3.10 python3.11

```

