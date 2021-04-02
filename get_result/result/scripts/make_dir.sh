#!/bin/bash
conf_type="mon_wl"
smearing=""
result_dir="/home/clusters/rrcmpi/kudrov/observables/get_result/result/flux_tube/${conf_type}${smearing}"
for mu in 0 10 15 25 30 40
do
w=$(($mu/10))
q=$(($mu-$w*10))
for T in 6 8 10 12 14 16 18
do
for R in 6 8 10 12 14 16 18 20
do
mkdir -p $result_dir/mu0.$w$q
done
done
done
