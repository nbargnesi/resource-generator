#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA_OUTPUT
assert-env-or-die RG_JENA_HOME
assert-env-or-die RG_TDB_DATA
uuids="$RG_JAVA_OUTPUT/uuids.nt"

echo "Loading UUIDs $uuids."
"$RG_JENA_HOME"/bin/tdbloader --loc "$RG_TDB_DATA" "$uuids"
echo "Done loading UUIDs."

