#!/bin/bash

SCRIPTS_DIR="$(dirname $(readlink -e "$0"))"

$SCRIPTS_DIR/preparation.py

CUR_DIR=$(pwd)
cd $SCRIPTS_DIR/../docs

pandoc -B ../scripts/titul.md ../scripts/toc.md -V colorlinks --css=../scripts/style.css \
		1_natch.md \
		2_setup.md \
		3_natch_cmd.md \
		4_launch_test_samples.md \
		5_setup_env.md \
		6_create_project.md \
		7_taint_source.md \
		8_scenario_work.md \
		9_snatch.md \
		10_additional.md \
		11_automation.md \
		13_applications.md \
		14_faq.md \
		15_app_license.md \
		16_app_qemu_cmdline.md \
		17_app_configs.md \
		18_app_module_cfg.md \
		19_app_graphs.md \
		20_app_coverage.md \
		21_app_cmd_line.md \
		22_app_requirements.md \
		23_app_oo_preparation.md \
		24_app_releases.md \
		-o $CUR_DIR/natch_docs.pdf \
        --pdf-engine=weasyprint \
        --metadata pagetitle="Natch documentation" \
        --metadata lang="Ru" \
#       --verbose > gen.html \
#       -N

if [[ -d ../.git ]]; then
    git reset --hard > /dev/null
fi


