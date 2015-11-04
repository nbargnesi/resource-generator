#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="pyflakes"
export SCRIPT_HELP="Pyflakes analysis."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./pyflakes.sh

