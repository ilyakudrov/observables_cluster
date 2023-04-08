#!/bin/bash

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

SA_steps=100
gaugecopies=2
samax=4
samin=1
seed=$(date +%s)

path_conf="${conf_path_start}/${conf_name}`printf %0${padding}d $i`${conf_path_end}"
echo ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

if [ ! -f "${output_conf_path}/conf_Landau_gaugefixed_`printf %04d $i`${conf_path_end}" ] || [  ! ${calculate_absent} ] ; then

mkdir -p ${output_conf_path}
output_conf_path1="${output_conf_path}/conf_Landau_"

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/LandauGaugeFixingSU3_4D_DP_N${L_spat}T${L_time} --ftype ${conf_format} --fbasename "${conf_path_start}/${conf_name}" \
	--fending "$conf_path_end" --reinterpret DOUBLE --fnumberformat ${padding}\
        -m 1 --fstartnumber ${i} --sasteps ${SA_steps} --gaugecopies ${gaugecopies} --samin ${samin}\
        --samax ${samax} --output_conf "${output_conf_path1}" --output_ending "$conf_path_end" --seed ${seed} --ormaxiter 2000 --microupdates 6 --precision 1e-13

fi

fi
done
