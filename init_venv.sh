#!/bin/sh
virtualenv --no-site-packages venv && \
    . venv/bin/activate && \
    pip install -r requirements.txt
