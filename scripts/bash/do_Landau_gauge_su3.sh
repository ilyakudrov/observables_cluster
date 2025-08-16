#!/bin/bash
echo $HOSTNAME

for((i=${conf_start};i<=${conf_end};i++))
do

if [[ ${conf_path_end} == "/" ]]; then

conf_path_end=""

fi

if [[ ${gauge_copies} == 0 ]]; then
ending_copy=1
else
ending_copy=${gauge_copies}
fi

if [[ ${conf_format} == "ildg" ]]; then
conf_format="ILDG"
fi
if [[ ${conf_format} == "qc2dstag" ]]; then
conf_format="QCDSTAG"
fi

for((copy=0;copy<${ending_copy};copy++))
do

SA_steps=100
samax=3.5
samin=0.001
seed=$(date +%s)

path_conf="${conf_path_start}/${conf_name}`printf %0${padding}d $i`${conf_path_end}"
if [[ ${gauge_copies} == 0 ]]; then
path_conf="${path_conf}"
else
path_conf="${path_conf}_${copy}"
fi
echo ${path_conf}

if [ -f ${path_conf} ] && [ -s ${path_conf} ] ; then

conf_out="${output_conf_path}/conf_Landau_`printf %0${padding}d $i`$conf_path_end"
if [[ ${gauge_copies} == 0 ]]; then
conf_out="${conf_out}"
conf_path_end1="$conf_path_end"
echo conf_path_end1 ${conf_path_end1}
echo conf_path_end ${conf_path_end}
else
conf_out="${conf_out}_${copy}"
conf_path_end1="${conf_path_end}_${copy}"
fi

echo output_conf_path ${output_conf_path}
echo conf_out ${conf_out}

if [[ ! -f ${conf_decomp} && ! -f ${conf_out} ]] || [ ! $calculate_absent -eq 1 ] ; then

mkdir -p ${output_conf_path}
output_conf_path1="${output_conf_path}/conf_Landau_"

echo conf_format ${conf_format}
echo ftype ${conf_format} fbasename "${conf_path_start}/${conf_name}" fending "$conf_path_end1" reinterpret DOUBLE fnumberformat ${padding}\
	m 1 fstartnumber ${i} sasteps ${SA_steps} gaugecopies ${gaugecopies} samin ${samin} samax ${samax} output_conf "${output_conf_path1}"\
	output_ending "$conf_path_end" seed ${seed} ormaxiter 2000 microupdates 6 precision 1e-11

/home/clusters/rrcmpi/kudrov/SU3_MA_gauge_GPU/src/gaugefixing/apps/U1xU1GaugeFixingSU3_4D_DP_N${L_spat}T${L_time} --ftype ${conf_format} --fbasename "${conf_path_start}/${conf_name}" \
	--fending "$conf_path_end1" --reinterpret DOUBLE --fnumberformat ${padding}\
        -m 1 --fstartnumber ${i} --sasteps ${SA_steps} --gaugecopies 1 --samin ${samin}\
        --samax ${samax} --output_conf "${output_conf_path1}" --output_ending "$conf_path_end1" --seed ${seed} --ormaxiter 2000 --microupdates 6 --precision 1e-11

fi
fi

#fi
done
done
