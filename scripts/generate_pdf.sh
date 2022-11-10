#!/bin/bash

SCRIPTS_DIR="$(dirname $(readlink -e "$0"))"

$SCRIPTS_DIR/preparation.py

pandoc -B $SCRIPTS_DIR/titul.md $SCRIPTS_DIR/toc.md -V colorlinks --css=$SCRIPTS_DIR/style.css $SCRIPTS_DIR/../[^Rt]*.md -o natch_docs.pdf \
		--pdf-engine=weasyprint \
       	--metadata pagetitle="Natch documentation" \
		--metadata lang="Ru" \
#		--pdf-engine-opt="-Oimages" \
#		--verbose > gen.html \
#		-N

if [[ -d $SCRIPTS_DIR/../.git ]]; then
	cd $SCRIPTS_DIR/..
	git reset --hard > /dev/null
fi

