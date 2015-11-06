#!/usr/bin/env bash
#
# Executes pep8 check.
#
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh
cd "$RG_PYTHON" || exit 1
echo "Running pep8 check."

PEP8_OPTS+="--show-source "
PEP8_OPTS+="--count "

pys=($(find src tests tools -name "*.py"))
pys+=('setup.py')
pep8 $PEP8_OPTS ${pys[@]}

PEP8_RC=$?

if [ ${PEP8_RC} -eq 1 ]; then
    echo "FAIL"
elif [ ${PEP8_RC} -eq 0 ]; then
    echo "You did a good job."
fi
exit ${PEP8_RC}

