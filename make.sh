#!/bin/bash
set -e
HERE=$(dirname $0)
source ${HOME}/.virtualenvs/tomsbdotnetPy3/bin/activate
cd bin
export PYTHONPATH=`pwd`/../src/
python createSiteFromDirs.py
bash ~/Dropbox/Projects/Next\ Task\ Decider/bin/generate_pw_protected_project_index.sh
