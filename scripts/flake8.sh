#!/usr/bin/env bash
#
# Executes flake8 check.
#
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
cd "${DIR}" || exit 1
echo "Running pyflakes check."

pys=($(find src tests -name "*.py"))
pys+=('setup.py')
flake8 ${pys[@]}
FLAKE8_RC=$?

if [ ${FLAKE8_RC} -eq 1 ]; then
    echo "FAIL"
elif [ ${FLAKE8_RC} -eq 0 ]; then
    echo "You did a good job."
fi
exit ${FLAKE8_RC}

