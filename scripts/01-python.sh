#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="Python menu"
export SCRIPT_HELP="Go to the Python submenu."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh

assert-env-or-die RG_PYTHON_SCRIPTS

GOSH_SCRIPTS="$RG_PYTHON_SCRIPTS" \
    GOSH_PROMPT="Python submenu (?|#)> " \
    $GOSH_PATH $@
exit 0

