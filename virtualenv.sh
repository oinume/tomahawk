#!/bin/sh

if [ ! -d .venv ]; then
    virtualenv --distribute .venv
    source .venv/bin/activate
    pip install -e .
    pip install -r requirements-dev.txt
fi
