#!/bin/bash

SA_steps=100
gaugecopies=10
samax=6
samin=0.2
seed=$(date +%s)

output_conf_path1 = "${output_conf_path}/conf_Landau_"

parameters="--ftype ${file_type} --fbasename ${conf_path_start} --fending ${conf_path_end} --reinterpret DOUBLE --fnumberformat ${padding}\
        -m ${number_of_confs_to_fix} --fstartnumber ${starting_conf} --sasteps ${SA_steps} --gaugecopies ${gaugecopies} --samin ${samin}\
        --samax ${samax} --output_conf "${output_conf_path1}" --output_ending "" --seed ${seed}"

/home/ilya/soft/source/culgt/src/gaugefixing/apps/LandauGaugeFixingSU3_4D_DP_N${L_spat}T${L_time} $parameters
