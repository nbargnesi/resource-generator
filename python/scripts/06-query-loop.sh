#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="query-loop"
export SCRIPT_HELP="Run the SPARQL query loop tool."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./query-loop.sh

