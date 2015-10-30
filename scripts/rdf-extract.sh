#!/usr/bin/env bash
#
# Executes an RDF extraction.
#
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
cd "${DIR}" || exit 1
. "$DIR"/env.sh || exit 1

require-cmd-or-die rlwrap
use-gosh-contrib-or-die
assert-env-or-die RG_PYTHON_ENVS
assert-env-or-die RG_RDF_EXTRACT
assert-env-or-die GOSH_CONTRIB_PYTHON_VIRTUALENV

GOSH_CONTRIB_PYTHON_VENV="$RG_PYTHON_ENVS"/rdf-extract
GOSH_CONTRIB_PYTHON_REQ_DEPS="$RG_RDF_EXTRACT"/deps.req
GOSH_CONTRIB_PYTHON_OPT_DEPS="$RG_RDF_EXTRACT"/deps.opt

# Create the virtual environment if needed...
create_python_env "python3"

# Execute RDF extraction
cd "$RG_RDF_EXTRACT" || exit 1
exec python3 src $@
# exec used; nothing else will be executed