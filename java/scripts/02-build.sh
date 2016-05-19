#!/usr/bin/env bash

# The next three lines are for the go shell.
export SCRIPT_NAME="build"
export SCRIPT_HELP="Runs gradle shadowJar."
[[ "$GOGO_GOSH_SOURCE" -eq 1 ]] && return 0

# Normal script execution starts here.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA_SCRIPTS
"$RG_JAVA_SCRIPTS"/build.sh
