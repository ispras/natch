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
		12_applications.md \
		13_faq.md \
		app1_license.md \
		app2_configs.md \
		app3_module_cfg.md \
		app4_graphs.md \
		app5_coverage.md \
		app6_cmd_line.md \
		app7_requirements.md \
		app8_oo_preparation.md \
		app9_releases.md \
		-o $CUR_DIR/natch_docs.pdf \
        --pdf-engine=weasyprint \
        --metadata pagetitle="Natch documentation" \
        --metadata lang="Ru" \
    #   --verbose > gen.html \
    #   -N

if [[ -d ../.git ]]; then
    git reset --hard > /dev/null
fi


