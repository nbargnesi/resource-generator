#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="Java menu"
export SCRIPT_HELP="Go to the Java submenu."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh

assert-env-or-die RG_JAVA_SCRIPTS

GOSH_SCRIPTS="$RG_JAVA_SCRIPTS" \
    GOSH_PROMPT="Java submenu (?|#)> " \
    $GOSH_PATH $@
exit 0

