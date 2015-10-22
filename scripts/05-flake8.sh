#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="flake8"
export SCRIPT_HELP="Flake8 analysis."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./flake8.sh

