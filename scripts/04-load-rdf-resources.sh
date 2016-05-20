#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="Loads RDF resources"
export SCRIPT_HELP="Loads all RDF resources into Apache Jena."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh

assert-env-or-die RG_SCRIPTS
"$RG_SCRIPTS"/load-rdf-resources.sh
