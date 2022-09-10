#!/bin/bash

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

SA_steps=500
gaugecopies=10
samax=4
samin=0.1
seed=$(date +%s)

starting_conf=conf_start
number_of_confs_to_fix=$((${conf_end} - ${conf_start} + 1))

mkdir -p ${output_conf_path}
output_conf_path1="${output_conf_path}/conf_Coulomb_"

/home/itep/kudrov/source/culgt/src/gaugefixing/apps/CoulombGaugeFixingSU3_4D_DP_N${L_spat}T${L_time} --ftype ${conf_format} --fbasename ${conf_path_start} --fending "$conf_path_end" --reinterpret DOUBLE --fnumberformat ${padding}\
        -m ${number_of_confs_to_fix} --fstartnumber ${conf_start} --sasteps ${SA_steps} --gaugecopies ${gaugecopies} --samin ${samin}\
        --samax ${samax} --output_conf "${output_conf_path1}" --output_ending "" --seed ${seed}