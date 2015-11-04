#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="coverage"
export SCRIPT_HELP="Get coverage metrics."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./coverage.sh

