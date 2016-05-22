#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_RDF_ARTIFACTS
assert-env-or-die RG_JENA_HOME
assert-env-or-die RG_TDB_DATA
cd "${RG_RDF_ARTIFACTS}" || exit 1
if not-in-path "$RG_JENA_HOME"/bin; then
    prepend PATH "$RG_JENA_HOME"/bin
fi
require-cmd-or-die "tdbloader2"
require-cmd-or-die "tdbloader"

echo -e "Starting $0"

# mismatched patterns expand to null strings
shopt -s nullglob

for x in *.bz2; do
    echo -n "Uncompressing $x... "
    bunzip2 "$x"
    echo "done."
done
for x in *.gz; do
    echo -n "Uncompressing $x... "
    gunzip "$x"
    echo "done."
done

if [ "$(ls -A "$RG_TDB_DATA")" ]; then
    echo "ERROR: directory not empty ($RG_TDB_DATA)" >&2
    exit 1
fi

# ls all files in RG_RDF_ARTIFACTS, largest first
rdf_artifacts=($(ls -S "$RG_RDF_ARTIFACTS"))

# Use tdbloader2 for largest artifact
artifact="${rdf_artifacts[0]}"
echo "Loading $artifact."
tdbloader2 --loc "$RG_TDB_DATA" $artifact
echo "Done loading $artifact."

# Use tdbloader to load the remaining artifacts
rdf_artifacts=("${rdf_artifacts[@]:1}")
for artifact in "${rdf_artifacts[@]}"; do
    echo "Loading $artifact."
    tdbloader --loc "$RG_TDB_DATA" $artifact
    echo "Done loading $artifact."
done

echo -e "Finished $0"
