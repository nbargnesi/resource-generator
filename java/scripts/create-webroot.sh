#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"/../../
. "$DIR"/env.sh || exit 1

if [ $# -ne 2 ]; then
    echo "Usage: $0 [PATH] [WEB ROOT]"
    echo "E.g. '$0 $(date +%Y-%m-%d) \"http://localhost:8000\"'"
    exit 1
fi

assert-env-or-die RG_NS_OUTPUT
assert-env-or-die RG_EQ_OUTPUT
assert-env-or-die RG_ANNO_OUTPUT

output_dir="$1"
if [ -d "$output_dir" ]; then
    echo "Output directory \"$output_dir\" already exists." >&2
    exit 1
fi
webroot="$2"

mkdir "$output_dir" && cd "$output_dir"

echo -en "Mirroring latest BEL framework resources... "
wget --quiet --mirror --no-parent --cut-dirs=2 "http://resource.belframework.org/belframework/latest-release/"
mv resource.belframework.org/* .
rmdir resource.belframework.org
echo "done"

rm -fr namespace annotation equivalence index.xml*

cp -a "$RG_NS_OUTPUT" .
cp -a "$RG_EQ_OUTPUT" .
cp -a "$RG_ANNO_OUTPUT" .

echo '<idx:index
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.belscript.org/schema/index index.xsd"
    xmlns:idx="http://www.belscript.org/schema/index"
    idx:belframework_version="2.0">

    <idx:annotationdefinitions>' > index.xml

find -name "*.belanno" | while read belanno; do
    belanno=annotation/$(basename $belanno)
    echo "    <idx:annotationdefinition idx:resourceLocation=\"$webroot/$belanno\" />" >> index.xml
done

echo '    </idx:annotationdefinitions>

    <idx:namespaces>' >> index.xml

find -name "*.belns" | while read belns; do
    belns=namespace/$(basename $belns)
    echo "       <idx:namespace idx:resourceLocation=\"$webroot/$belns\" />" >> index.xml
done

echo '    </idx:namespaces>

    <idx:equivalences>' >> index.xml

find -name "*.beleq" | while read beleq; do
    beleq=equivalence/$(basename $beleq)
    belns=namespace/$(basename $beleq | sed 's/beleq/belns/')
    echo "        <idx:equivalence idx:resourceLocation=\"$webroot/$beleq\" >" >> index.xml
    echo "            <idx:namespace-ref idx:resourceLocation=\"$webroot/$belns\" />" >> index.xml
    echo "        </idx:equivalence>" >> index.xml
done

echo "    </idx:equivalences>

    <idx:knowledge>
        <idx:protein-families idx:resourceLocation=\"$webroot/resource/protein-families.bel\" />
        <idx:named-complexes idx:resourceLocation=\"$webroot/resource/named-complexes.bel\" />
        <idx:gene-scaffolding idx:resourceLocation=\"$webroot/resource/gene_scaffolding_document_9606_10090_10116.bel\" />
        <idx:orthologies>
            <idx:orthology idx:resourceLocation=\"$webroot/resource/gene-orthology.bel\" />
        </idx:orthologies>
    </idx:knowledge>
</idx:index>" >> index.xml

sha256sum index.xml > index.xml.sha256

base=$(pwd)
# create sha256 hashes for each namespace
cd namespace || exit 1
for x in *.belns; do sha256sum "$x" > "$x.sha256"; done
cd "$base"

# create sha256 hashes for each equivalence
cd equivalence || exit 1
for x in *.beleq; do sha256sum "$x" > "$x.sha256"; done
cd "$base"

# create sha256 hashes for each annotation
cd annotation || exit 1
for x in *.belanno; do sha256sum "$x" > "$x.sha256"; done
cd "$base"

echo "Done!"

