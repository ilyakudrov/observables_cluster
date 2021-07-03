#!/bin/bash
parameters="-conf_format $conf_format -conf_path $conf_path -output_path_wilson $output_path_wilson -L_spat ${L_spat} -L_time ${L_time} -T_min ${T_min} -T_max ${T_max} -R_min ${R_min} -R_max ${R_max}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/wilson_${matrix_type} $parameters
