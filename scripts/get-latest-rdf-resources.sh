#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_RDF_ARTIFACTS
mkdir -p "$RG_RDF_ARTIFACTS"
cd "${RG_RDF_ARTIFACTS}" || exit 1

echo -e "Starting $0"
if [ "$(ls -A "$RG_RDF_ARTIFACTS")" ]; then
echo """
WARNING: I found files in RG_RDF_ARTIFACTS. Remove the old files if you need to
         ensure a clean set of RDF artifacts are being used. RG_RDF_ARTIFACTS
         is set to:

         	$RG_RDF_ARTIFACTS

         (you normally do not need to do this)
"""
fi

ci_server="http://build.openbel.org"
path="browse/OR-PRR/latestSuccessful/artifact/shared/openbel-rdf-resources"
listing="$ci_server/$path/artifact-list"

response=($(wget -q "$listing" -O -))
ec=$?
if [ $ec -ne 0 ]; then
	echo "Failed to get RDF resources from: $listing" >&2
	exit 1
fi

for artifact in "${response[@]}"; do
	echo -en "Getting $artifact... "
	artifact_url="$ci_server/$path/$artifact"
	wrslt=$(wget -N "$artifact_url" 2>&1)
	ec=$?
	if [ $ec -ne 0 ]; then
		echo "$wrslt" >&2
		echo "Failed to get RDF artifact: $artifact_url" >&2
		exit 1
	fi
	echo "done"
done

echo -e "Finished $0"