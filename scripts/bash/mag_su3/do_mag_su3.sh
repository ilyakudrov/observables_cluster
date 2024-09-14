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

if [ ! -f "${conf_path_output}/conf_gaugefixed_`printf %0${padding}d $i`${conf_path_end}" ] || [ $calculate_absent -eq 0 ] ; then

echo conf_path_output ${conf_path_output}
echo functional_path_output ${functional_path_output}

mkdir -p ${conf_path_output}
mkdir -p ${functional_path_output}

path_functional_output="${functional_path_output}/functional"

seed=$(date +%s)

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/MAGaugeFixingSU3_4D_DP_N${L_spat}T${L_time}  --ftype ${conf_format} --fbasename ${conf_path_start} \
 --fending "$conf_path_end" --reinterpret DOUBLE --fnumberformat ${padding} -m 1 --fstartnumber ${i} --sasteps ${steps} --samin ${T_min} --samax 1.25\
 --output_SA_functional ${path_functional_output} --gaugecopies ${copies} --output_conf "${conf_path_output}/conf_" --output_ending "${conf_path_end}" --seed ${seed} \
 --microupdates 6 --precision ${tolerance} --ormaxiter 10000 --doSA ${doSA} --save_each ${save_each} --save_best ${save_best}

fi
fi

done
