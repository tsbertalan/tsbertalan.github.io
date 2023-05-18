#!/bin/bash
set -e
source ${HOME}/.virtualenvs/tomsbdotnetPy3/bin/activate
THISFILEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python -m http.server 8080 --directory "${THISFILEDIR}/.."

