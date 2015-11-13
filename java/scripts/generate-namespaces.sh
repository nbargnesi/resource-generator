#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_JAVA
cd "${RG_JAVA}" || exit 1
jars=$(find lib -name "*.jar" -printf "%p:")
java -Dorg.apache.logging.log4j.simplelog.StatusLogger.level=OFF \
    -cp build:$jars org.openbel.reggie.rdf.generate.namespaces.Main

