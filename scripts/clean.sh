#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../
. "$DIR"/env.sh || exit 1
assert-env-or-die RG_RDF_ARTIFACTS
assert-env-or-die RG_JAVA_OUTPUT
assert-env-or-die RG_JAVA_BUILD
rm -fr "$RG_RDF_ARTIFACTS"/*
rm -fr "$RG_JAVA_OUTPUT"/*
rm -fr "$RG_JAVA_BUILD"
