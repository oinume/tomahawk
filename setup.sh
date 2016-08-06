#!/bin/sh

if [ ! -d .venv ]; then
    virtualenv --distribute --python /usr/local/bin/python .venv
    . .venv/bin/activate
    python setup.py
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -e .
fi
