#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA_SCRIPTS
assert-env-or-die RG_JAVA_BUILD
"$RG_JAVA_SCRIPTS"/dist.sh && "$RG_JAVA_BUILD"/export-turtle

