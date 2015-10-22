#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="pep8"
export SCRIPT_HELP="PEP8 analysis."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./pep8.sh

