#!/bin/bash
set -e
HERE=$(dirname $0)
source ${HOME}/.virtualenvs/tomsbdotnetPy3/bin/activate
cd bin
export PYTHONPATH=`pwd`/../src/
python -m pdb createSiteFromDirs.py
