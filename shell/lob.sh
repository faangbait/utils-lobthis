#!/bin/sh

#Edit these.

#This is the path to the python3 binary inside the virtualenv created for the project
#e.g. /home/user/projects/utils-lobthis/venv/bin/python3
VIRTUAL_ENV_PYTHON3_PATH=

#This is location of the project file lobit.py
#e.g. /home/user/projects/utils-lobthis/lobit.py
LOBITPY_PATH=

"$VIRTUAL_ENV_PYTHON3_PATH" "$LOBITPY_PATH" $0
