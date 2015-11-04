#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="test"
export SCRIPT_HELP="Execute unit tests."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./test.sh

