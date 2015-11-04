#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="rdf-extract"
export SCRIPT_HELP="Execute an RDF extraction."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
./rdf-extract.sh

