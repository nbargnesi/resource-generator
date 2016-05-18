#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="Get RDF resources"
export SCRIPT_HELP="Gets all RDF resources from the OpenBEL build server."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh

assert-env-or-die RG_SCRIPTS
"$RG_SCRIPTS"/get-latest-rdf-resources.sh
