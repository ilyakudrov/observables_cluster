#!/bin/bash

for((i=$conf1;i<=${conf2};i++))
do

a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))

conf_path_qc2dstag="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/qc2dstag/${conf_size}/mu${mu}/${smearing}/${chains[j]}/conf_APE_alpha=0.7_$a$b$c$d"
conf_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_path_monopoless="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/monopoless/qc2dstag/${conf_size}/mu${mu}/${smearing}/${chains[j]}/conf_APE_alpha=0.7_$a$b$c$d"

if [[ ${monopole} == "/" ]] ; then

conf_path=$conf_path_qc2dstag

else

conf_path=("${!path1}")

fi

echo $conf_path

if [ -f ${conf_path} ] ; then

output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${axis}/${monopole}/${conf_type}/${conf_size}/mu${mu}/$chain"
mkdir -p ${output_path_wilson}
output_path_wilson="${output_path_wilson}/wilson_loop_$a$b$c$d"

if [ ! -f ${output_path_wilson} ] || [  ! ${calculate_absent} ] ; then

parameters="-conf_format $conf_format -conf_path $conf_path -output_path_wilson $output_path_wilson -L_spat ${L_spat} -L_time ${L_time} -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/wilson_${axis}_${matrix_type} $parameters

fi

fi

done
