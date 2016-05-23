#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA
assert-env-or-die RG_JAVA_BUILD
assert-env-or-die RG_JAVA_DIST
cd "${RG_JAVA}" || exit 1
gradle clean \
        shadowJar \
        integrityCheckScripts \
        assignUUIDsScripts \
        runScripts \
        annotationsScripts \
        equivalencesScripts \
        namespacesScripts \
        showNamespacesScripts

rm -fr "$RG_JAVA_DIST" && mkdir "$RG_JAVA_DIST"
cp -a "$RG_JAVA_BUILD" "$RG_JAVA_DIST"
