#!/bin/bash
conf_type="qc2dstag"
smearing="HYP_APE"
conf_size="32^4"
result_dir="/home/clusters/rrcmpi/kudrov/observables/result/flux_tube/${conf_type}/${conf_size}/${smearing}"
for mu in 5 0 10 15 25 30 40 45 50
do
w=$(($mu/10))
q=$(($mu-$w*10))
for chain in ""
do
for T in 8 10 12 14 16 18
do
for R in 8 10 12 14 16 18 20
do
mkdir -p $result_dir/mu0.$w$q/${chain}/T=$T/R=$R
done
done
done
done
