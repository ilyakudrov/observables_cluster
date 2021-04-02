#!/bin/bash
conf_type="qc2dstag"
matrix_type="su2"
conf_format="double_qc2dstag"
L_spat=32
L_time=32
conf_size="32^4"
#parameters_dir="/home/clusters/rrcmpi/kudrov/matrix_parameters"
#source ${parameters_dir}/${conf_type}
smearing="HYP_APE"
smeared_format="double"
x_trans="0"

i=$conf_num
a=$(($i/1000))
b=$((($i-$a*1000)/100))
c=$((($i-$a*1000-$b*100)/10))
d=$(($i-$a*1000-$b*100-$c*10))
for mu in 25
do
w=$(($mu/10))
q=$(($mu-$w*10))

smeared_path="/home/clusters/rrcmpi/kudrov/smearing/conf/${conf_type}/${conf_size}/${smearing}/mu0.$w$q/${conf_chain}/smeared_$a$b$c$d"

for R in 8 10 12 14 16 18 20
do
for T in 8 10 12 14 16 18
do

output_path_electric="/home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}/${conf_size}/${smearing}/mu0.$w$q/${conf_chain}/T=${T}/R=${R}/electric_${a}${b}${c}${d}"
output_path_magnetic="/home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}/${conf_size}/${smearing}/mu0.$w$q/${conf_chain}/T=${T}/R=${R}/magnetic_${a}${b}${c}${d}"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/OFFD/CON_OFF_MAG_${a}${b}${c}${d}.LAT"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/CON_32^3x32_${a}${b}${c}${d}.LAT"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${a}${b}${c}${d}.LAT"
#conf_path="/home/clusters/rrcmpi/nikolaev/SU_2_staggered/configurations/N_f=2/improved/32^3x32/mu=0.$w$q/beta=1.8/ma=0.0075/lambda=0.00075/converted_Fort/conf_$a$b$c$d.fl"
#smeared_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${a}${b}${c}${d}.LAT"
#smeared_path=$conf_path
conf_path="/home/clusters/rrcmpi/kudrov/conf/${conf_size}/mu0.$w$q/${conf_chain}/confs/CONF${a}${b}${c}${d}"

parameters="-conf_format $conf_format -smeared_format ${smeared_format} -conf_path $conf_path -smeared_path $smeared_path -output_path_electric ${output_path_electric} -output_path_magnetic ${output_path_magnetic} -R_size ${R} -T_size ${T} -L_spat ${L_spat} -L_time ${L_time} -x_trans ${x_trans}"

if [ -f ${conf_path} ] && [ -f ${smeared_path} ]; then
	/home/clusters/rrcmpi/kudrov/observables/code/exe/flux_wilson_${matrix_type} $parameters
fi
#if test $i -lt 1000; then
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/OFFD/CON_OFF_MAG_${b}${c}${d}.LAT"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/CON_32^3x32_${b}${c}${d}.LAT"
#conf_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${b}${c}${d}.LAT"
#conf_path="/home/clusters/rrcmpi/nikolaev/SU_2_staggered/configurations/N_f=2/improved/32^3x32/mu=0.$w$q/beta=1.8/ma=0.0075/lambda=0.00075/converted_Fort/conf_$b$c$d.fl"
#smeared_path="/lustre/rrcmpi/vborn/SU2_dinam/MAG/mu0p${mu}_b1p8_m0p0075_lam0p00075/MON_WL/CON_MON_MAG_${b}${c}${d}.LAT"
#smeared_path=$conf_path
#conf_path="/home/clusters/rrcmpi/kudrov/conf/qc2dstag/mu0.$w$q/CONF${a}${b}${c}"

#parameters="-conf_format $conf_format -smeared_format ${smeared_format} -conf_path $conf_path -smeared_path $smeared_path -output_path_electric ${output_path_electric} -output_path_magnetic ${output_path_megnetic} -R_size ${R} -T_size ${T} -x_trans ${x_trans}"

#if [ -f ${conf_path} ] && [ -f ${smeared_path} ]; then
#	/home/clusters/rrcmpi/kudrov/observables/code/exe/flux_wilson_${matrix_type} $parameters
#fi
#fi
done
done
done
