#!/bin/bash
parameters="-conf_format $conf_format -conf_path $conf_path -output_lengths $output_lengths -output_windings $output_windings -output_observables $output_observables -L_spat ${L_spat} -L_time ${L_time}"

/home/clusters/rrcmpi/kudrov/observables_cluster/code/exe/monopole_observables_${matrix_type} $parameters
