#!/bin/bash

for((i=$conf1;i<=${conf2};i++))
do

a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))

conf_path_qc2dstag="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.75_$a$b$c$d"
conf_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_path_monopoless="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/monopoless/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.75_$a$b$c$d"

#conf_path_qc2dstag="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/SU2_dinam/conf_APE_alpha=0.7_$a$b$c$d"
#conf_path_monopole="/home/clusters/01/vborn/Copy_from_lustre/SU2_dinam/MAG/mu0p0_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_$b$c$d.LAT"
#conf_path_monopoless="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/monopoless/SU2_dinam/conf_APE_alpha=0.7_$a$b$c$d"

if [[ ${monopole} == "/" ]] ; then

conf_path=$conf_path_qc2dstag

else

path1="conf_path_${monopole}"
conf_path=("${!path1}")

fi

if [[ ${conf_type} == "su2_suzuki" ]] ; then

conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p${beta}/CON_fxd_MAG_$b$c$d.LAT"

if [[ ${monopole} == "monopoless" ]] ; then

conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p${beta}/DECOMPOS/CONFIGS/CON_OFF_MAG_$b$c$d.LAT"

elif [[ ${monopole} == "monopole" ]] ; then

conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p${beta}/DECOMPOS/CONFIGS/CON_MON_MAG_$b$c$d.LAT"

fi

fi

#echo ${conf_path}

if [ -f ${conf_path} ] ; then

if [[ ${smearing} == "/" ]] ; then

smearing1="unsmeared"

else

smearing1="smeared"

fi

#output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${axis}/${monopole}/${conf_type}/${smearing1}/${conf_size}/mu${mu}/$chain"
output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${axis}/${monopole}/${conf_type}/${conf_size}/beta2.${beta}/mu${mu}/$chain"
#output_path_wilson="/home/clusters/rrcmpi/kudrov/observables_cluster/result/wilson_loop/${axis}/${monopole}/SU2_dinam/${conf_size}/mu${mu}"
mkdir -p ${output_path_wilson}
output_path_wilson="${output_path_wilson}/wilson_loop_$a$b$c$d"

if [ ! -f ${output_path_wilson} ] || [  ${calculate_absent} == "false" ] ; then

#echo output_path_wilson $output_path_wilson

parameters="-conf_format $conf_format -conf_path $conf_path -output_path_wilson $output_path_wilson -bites_skip ${bites_skip} -L_spat ${L_spat} -L_time ${L_time} -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/wilson_${axis}_${matrix_type} $parameters

fi

fi

done
