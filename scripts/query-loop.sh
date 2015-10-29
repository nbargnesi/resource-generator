#!/usr/bin/env bash
#
# Executes a SPARQL query loop.
#
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
cd "${DIR}" || exit 1
. "$DIR"/env.sh || exit 1

require-cmd-or-die rlwrap
use-gosh-contrib-or-die
assert-env-or-die RG_PYTHON_ENVS
assert-env-or-die RG_QUERY_LOOP
assert-env-or-die GOSH_CONTRIB_PYTHON_VIRTUALENV

GOSH_CONTRIB_PYTHON_VENV="$RG_PYTHON_ENVS"/query-loop
GOSH_CONTRIB_PYTHON_REQ_DEPS="$RG_QUERY_LOOP"/deps.req
GOSH_CONTRIB_PYTHON_OPT_DEPS="$RG_QUERY_LOOP"/deps.opt

# Create the virtual environment if needed...
create_python_env "python3"

# Execute query-loop with rlwrap
cd "$RG_QUERY_LOOP" || exit 1
exec rlwrap python3 src $@
# exec used; nothing else will be executed