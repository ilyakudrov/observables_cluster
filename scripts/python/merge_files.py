import json
import os

conf_size = "40^4"
theory_type = "su2"
conf_type = "qc2dstag"
# smearing = "/"
smearing = "HYP5_alpha=1_1_0.5_APE0_alpha=0.5"

for monopole in ['monopoless']:
    for beta in ['/']:
        for mu in ['mu0.00', 'mu0.05', 'mu0.35', 'mu0.45']:
            f = open(
                f'/home/clusters/rrcmpi/kudrov/conf/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/parameters.json')
            data = json.load(f)
            chains = data['chains']
            for chain, range in chains.items():
                for i in range(range[0], range[1] + 1):
                    file_path = f'/home/clusters/rrcmpi/kudrov/observables_cluster/result/polaykov_loop/{theory_type}/{conf_type}/{conf_size}/{beta}/{mu}/{monopole}/{smearing}/{chain}'
                    if(os.path.isfile(file_path)):
                        with open(file_path, 'r') as f:
                            lines = f.readlines()
