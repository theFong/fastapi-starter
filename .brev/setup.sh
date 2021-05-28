#!/bin/bash

sudo apt-get install -y build-essential

sudo apt-get install -y python3-distutils

sudo apt-get install -y python3-apt

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

rm get-pip.py

source $HOME/.poetry/env