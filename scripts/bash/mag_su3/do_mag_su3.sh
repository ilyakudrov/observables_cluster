#!/bin/bash

echo ${conf_format}

if [[ ${conf_format} == "ildg" ]]; then
conf_format="ILDG"
fi
if [[ ${conf_format} == "double_qc2dstag" ]]; then
conf_format="QCDSTAG"
fi

echo ${conf_format}

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

path_conf="${conf_path_start}`printf %0${padding}d $i`${conf_path_end}"
echo ${conf_path_end}
echo ${conf_path_start}
echo ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

echo conf_path_output ${conf_path_output}
echo functional_path_output ${functional_path_output}

mkdir -p ${conf_path_output}
mkdir -p ${functional_path_output}

path_functional_output="${functional_path_output}/functional"

seed=$(date +%s)

echo --ftype ${conf_format} --fbasename ${conf_path_start} \
 --fending ${conf_path_end} --reinterpret DOUBLE --fnumberformat ${padding} -m 1 --fstartnumber ${i} --sasteps 5 --samin 2.5 --samax 0.5\
 --output_SA_functional ${path_functional_output} --gaugecopies ${copies} --output_conf "${conf_path_output}/conf_" --output_ending "${conf_path_end}" --seed ${seed} --microupdates 6 --precision ${tolerance}

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/MAGaugeFixingSU3_4D_DP_N${L_spat}T${L_time}  --ftype ${conf_format} --fbasename ${conf_path_start} \
 --fending "$conf_path_end" --reinterpret DOUBLE --fnumberformat ${padding} -m 1 --fstartnumber ${i} --sasteps ${steps} --samin 2.5 --samax 0.5\
 --output_SA_functional ${path_functional_output} --gaugecopies ${copies} --output_conf "${conf_path_output}/conf_" --output_ending "${conf_path_end}" --seed ${seed} --microupdates 6 --precision ${tolerance} --ormaxiter 5000 

fi

done
