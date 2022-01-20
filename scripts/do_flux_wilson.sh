#!/bin/bash

for i in $(seq -f "%0${padding}g" ${conf_start} ${conf_end})
#for((i=$conf1;i<=${conf2};i++))
do

conf_path="${conf_path_start}${i}${conf_path_end}"

conf_path_qc2dstag="/home/clusters/rrcmpi/kudrov/conf/qc2dstag/${conf_size}/mu${mu}/$chain/confs/CONF$a$b$c$d"
conf_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_path_monopoless="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopoless/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopoless_$a$b$c$d"

conf_smeared_path_qc2dstag="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.7_$a$b$c$d"
conf_smeared_path_monopole="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/monopole/qc2dstag/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"
conf_smeared_path_monopoless="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/monopoless/qc2dstag/${conf_size}/mu${mu}/${smearing}/$chain/conf_APE_alpha=0.7_$a$b$c$d"

if [[ ${conf_type} == "qc2dstag" ]] ; then

if [[ ${monopole} == "/" ]] ; then

conf_path=$conf_path_qc2dstag
smeared_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/${conf_type}/${conf_size}/mu${mu}/${smearing}/$chain/conf_$a$b$c$d"

elif [[ ${monopole} == "monopole" ]] ; then

conf_path="/home/clusters/rrcmpi/kudrov/conf/${conf_type}/${conf_size}/mu${mu}/$chain/confs/CONF$a$b$c$d"
#conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p5/DECOMPOS/CONFIGS/CON_MON_MAG_$b$c$d.LAT"
smeared_path="/home/clusters/rrcmpi/kudrov/decomposition/confs_decomposed/${monopole}/${conf_type}/${conf_size}/mu${mu}/$chain/conf_monopole_$a$b$c$d"

elif [[ ${monopole} == "monopoless" ]] ; then

conf_path="/home/clusters/rrcmpi/kudrov/conf/${conf_type}/${conf_size}/mu${mu}/$chain/confs/CONF$a$b$c$d"
#conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p5/DECOMPOS/CONFIGS/CON_MON_MAG_$b$c$d.LAT"
smeared_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/${conf_type}/${conf_size}/mu${mu}/${smearing}/$chain/conf_$a$b$c$d"

else

path1="conf_path_${monopole}"
conf_path=("${!path1}")
path2="conf_smeared_path_${monopole}"
smeared_path=("${!path2}")

fi

fi

if [[ ${conf_type} == "su2_suzuki" ]] ; then

conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p4/CON_fxd_MAG_$b$c$d.LAT"
smeared_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/${conf_type}/${conf_size}/mu${mu}/${smearing}/$chain/conf_$a$b$c$d"
bites_skip_nonabelian=4

if [[ ${monopole} == "monopoless" ]] ; then

#smeared_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p${beta}/CON_fxd_MAG_$b$c$d.LAT"
smeared_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/${conf_type}/${conf_size}/mu${mu}/${smearing}/$chain/conf_$a$b$c$d"

elif [[ ${monopole} == "monopole" ]] ; then

conf_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p4/CON_fxd_MAG_$b$c$d.LAT"
#smeared_path="/home/clusters/01/vborn/Copy_from_lustre/SU2/SUZUKI/L24/MAG/B2p4/DECOMPOS/CONFIGS/CON_MON_MAG_$b$c$d.LAT"
smeared_path="/home/clusters/rrcmpi/kudrov/smearing_cluster/confs_smeared/${monopole}/${conf_type}/${conf_size}/mu${mu}/${smearing}/$chain/conf_$a$b$c$d"

fi

fi

#echo conf_path ${conf_path}
#echo smeared_path ${smeared_path}
#echo monopole ${monopole}
#echo path1 ${path1}

if [ -f ${conf_path} ] && [ -s ${conf_path} ] && [ -f ${smeared_path} ] && [ -s ${smeared_path} ] ; then

#echo conf_path ${conf_path}
#echo smeared_path ${smeared_path}

if [[ $conf_size == "40^4" ]] ; then

R_sizes=(6 8 10)
T_sizes=(6 8 10)
#x_trans=0

#R_sizes=(6 8 10 12 14 16 18 20)
#T_sizes=(6 8 10 12 14 16 18)
x_trans=0

elif [[ $conf_size == "32^4" ]] ; then

R_sizes=(8 10 12 14 16)
T_sizes=(8 10 12 14 16)
x_trans=0

elif [[ $conf_size == "24^4" ]] ; then

R_sizes=(4 6 8)
T_sizes=(4 6 8)
#R_sizes=(1 6)
#T_sizes=(1 8)
x_trans=0

else

echo wrong conf_size ${conf_size}

fi

for R in ${R_sizes[@]}; do
for T in ${T_sizes[@]}; do

echo R $R T $T

output_path1="/home/clusters/rrcmpi/kudrov/observables_cluster/result/flux_tube_wilson/${monopole}/${conf_type}/${conf_size}/mu${mu}/$chain"

output_path="${output_path1}/T=${T}/R=${R}"
#echo ${output_path}
mkdir -p ${output_path}

output_path_electric="${output_path}/electric_${a}${b}${c}${d}"
output_path_magnetic="${output_path}/magnetic_${a}${b}${c}${d}"

parameters="-conf_format $conf_format -smeared_format ${smeared_format} -conf_path $conf_path -smeared_path ${smeared_path} -bites_skip ${bites_skip} -bites_skip_smeared ${bites_skip_smeared} $smeared_path -output_path_electric ${output_path_electric} -output_path_magnetic ${output_path_magnetic} -R_size ${R} -T_size ${T} -L_spat ${L_spat} -L_time ${L_time} -x_trans ${x_trans}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/flux_wilson_${matrix_type}_${matrix_type_smeared} $parameters


done
done

fi

done
