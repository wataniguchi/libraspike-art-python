## Python CFFI Bindings for libraspike-art

# Installation

Get this repository:

    git clone https://github.com/wataniguchi/libraspike-art-python.git
    cd libraspike-art-python

If you are on a modern Linux you will probably want to create a venv:

    python3 -m venv venv
    source venv/bin/activate

Build the bindings and install libraspike-art-python package:

    pip install -e .

Use libraspike-art:

    python3 sample/raspike_test.py
