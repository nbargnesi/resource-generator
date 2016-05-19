#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA
cd "${RG_JAVA}" || exit 1
gradle shadowJar
