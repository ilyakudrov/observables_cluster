#!/bin/bash

for((i=$conf1;i<=${conf2};i++))
do

a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))

conf_path_qc2dstag="/home/clusters/rrcmpi/kudrov/conf/qc2dstag/${conf_size}/mu${mu}/$chain/confs/CONF$a$b$c$d"
conf_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_path_monopoless="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopoless/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopoless_$a$b$c$d"

conf_smeared_path_qc2dstag="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.7_$a$b$c$d"
conf_smeared_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_smeared_path_monopoless="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/monopoless/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.7_$a$b$c$d"

if [[ ${monopole} == "/" ]] ; then

conf_path=$conf_path_qc2dstag
smeared_path=$conf_smeared_path_qc2dstag

else

path1="conf_path_${monopole}"
conf_path=("${!path1}")
path2="conf_smeared_path_${monopole}"
smeared_path=("${!path2}")

fi

echo conf_path ${conf_path}
echo monopole ${monopole}
echo path1 ${path1}

if [ -f ${conf_path} ] ; then

echo conf_path ${conf_path}
echo smeared_path ${smeared_path}

for R in ${R_sizes[@]}; do
for T in ${T_sizes[@]}; do

output_path1="/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_wilson/${monopole}/${conf_type}/${conf_size}/mu${mu}/$chain"

output_path="${output_path1}/T=${T}/R=${R}"
echo ${output_path}
mkdir -p ${output_path}

output_path_electric="${output_path}/electric_${a}${b}${c}${d}"
output_path_magnetic="${output_path}/magnetic_${a}${b}${c}${d}"

parameters="-conf_format $conf_format -smeared_format ${smeared_format} -conf_path $conf_path -smeared_path $smeared_path -output_path_electric ${output_path_electric} -output_path_magnetic ${output_path_magnetic} -R_size ${R} -T_size ${T} -L_spat ${L_spat} -L_time ${L_time} -x_trans ${x_trans}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/flux_wilson_${matrix_type} $parameters


done
done

fi

done
