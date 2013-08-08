#!/usr/bin/env bash
DEST=/home/jhourani/openbel-contributions/resource_generator/touchdown1/datasets2
for i in *
do
   head -1000 "${i}" > ${DEST}/${i}
done