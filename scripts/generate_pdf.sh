#!/bin/bash

SCRIPTS_DIR="$(dirname $(readlink -e "$0"))"

$SCRIPTS_DIR/preparation.py

CUR_DIR=$(pwd)
cd $SCRIPTS_DIR/../docs

pandoc -B ../scripts/titul.md ../scripts/toc.md -V colorlinks --css=../scripts/style.css \
		1_natch.md \
		2_setup.md \
		3_quickstart.md \
		4_setup_env.md \
		5_create_project.md \
		6_taint_source.md \
		7_scenario_work.md \
		8_snatch.md \
		9_additional.md \
		10_automation.md \
		11_utils.md \
		12_applications.md \
		13_faq.md \
		14_app_license.md \
		15_app_qemu_cmdline.md \
		16_app_configs.md \
		17_app_module_cfg.md \
		18_app_coverage.md \
		19_app_natch_cmds.md \
		20_app_requirements.md \
		21_app_oo_preparation.md \
		22_app_releases.md \
		-o $CUR_DIR/natch_docs.pdf \
        --pdf-engine=weasyprint \
        --metadata pagetitle="Natch documentation" \
        --metadata lang="Ru" \
#       --verbose > gen.html \
#       -N

if [[ -d .git ]]; then
       git reset --hard > /dev/null
fi


