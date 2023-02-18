#!/bin/bash

VENV=${1:-venv}

python3.8 -m venv $VENV && \
  source $VENV/bin/activate && \
  pip install --upgrade pip && \
  pip install -e '.[build]' && \
  python -m spacy download en_core_web_trf && \
  
