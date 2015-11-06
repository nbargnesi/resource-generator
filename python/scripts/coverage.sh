#!/usr/bin/env bash
#
# Runs coverage.
#
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh
"$RG_PYTHON_SCRIPTS"/test.sh || exit 1
coverage report -m || exit 1

