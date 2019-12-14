#!/bin/bash
set -e
source ${HOME}/.virtualenvs/tomsbdotnet/bin/activate
cd bin
export PYTHONPATH=`pwd`/../src/
python createSiteFromDirs.py