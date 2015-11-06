#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Pull in standard functions, e.g., default.
source "$DIR/.gosh.sh" || return 1
default CUSTOM_ENV_SH "$DIR/env.sh.custom"
assert-source "$CUSTOM_ENV_SH" || return 1

### PATHS ###
default RG_DIR              "$DIR"
default CUSTOM_ENV_SH       "$RG_DIR/env.sh.custom"
default RG_SCRIPTS          "$RG_DIR"/scripts
default RG_PYTHON           "$RG_DIR"/python
default RG_JAVA             "$RG_DIR"/java
default RG_PYTHON_SCRIPTS   "$RG_PYTHON"/scripts
default RG_JAVA_SCRIPTS     "$RG_JAVA"/scripts
default RG_PYTHON_TOOLS     "$RG_PYTHON"/tools
default RG_PYTHON_ENVS      "$RG_PYTHON"/.envs
default RG_QUERY_LOOP       "$RG_PYTHON_TOOLS"/query-loop
default RG_RDF_EXTRACT      "$RG_PYTHON_TOOLS"/rdf-extract
default RG_JAVA_TEMPLATES   "$RG_JAVA"/templates

### RDF ###
default RG_RDF_SPARQL_URL   "http://localhost:3030/openbel"

### THE GO SHELL ###
default GOSH_SCRIPTS                    "$DIR"/scripts
default GOSH_PROMPT                     "reggie (?|#|#?)> "
default GOSH_CONTRIB                    "$RG_SCRIPTS"/gosh-contrib
default GOSH_CONTRIB_PYTHON_VIRTUALENV  "$RG_SCRIPTS"/virtualenv/virtualenv.py