#include "basic_observables.h"
#include "data.h"
#include "link.h"
#include "loop.h"
#include "matrix.h"
#include "monopoles.h"
#include "result.h"

#include <cstring>
#include <ctime>
#include <iostream>
#include <map>
#include <vector>

#include <iostream>

int x_size;
int y_size;
int z_size;
int t_size;

int main(int argc, char *argv[]) {
  unsigned int start_time;
  unsigned int end_time;
  unsigned int search_time;

  std::string conf_format;
  std::string conf_path;
  std::string output_lengths;
  std::string output_windings;
  std::string output_observables;
  int L_spat, L_time;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (std::string(argv[i]) == "-conf_path") {
      conf_path = argv[++i];
    } else if (std::string(argv[i]) == "-output_lengths") {
      output_lengths = argv[++i];
    } else if (std::string(argv[i]) == "-output_windings") {
      output_windings = argv[++i];
    } else if (std::string(argv[i]) == "-output_observables") {
      output_observables = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    }
  }

  std::cout << "conf_format " << conf_format << std::endl;
  std::cout << "conf_path " << conf_path << std::endl;
  std::cout << "output_lengths " << output_lengths << std::endl;
  std::cout << "output_windings " << output_windings << std::endl;
  std::cout << "output_observables " << output_observables << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;

  x_size = L_spat;
  y_size = L_spat;
  z_size = L_spat;
  t_size = L_time;

  // data<MATRIX> conf;

  std::vector<FLOAT> angles = read_angles_double_fortran(conf_path);

  // if (std::string(conf_format) == "float") {
  //   conf.read_float(conf_path);
  // } else if (std::string(conf_format) == "double") {
  //   conf.read_double(conf_path);
  // } else if (std::string(conf_format) == "double_fortran") {
  //   conf.read_double_fortran(conf_path);
  // } else if (std::string(conf_format) == "float_fortran") {
  //   conf.read_float_fortran(conf_path);
  // } else if (std::string(conf_format) == "double_qc2dstag") {
  //   conf.read_double_qc2dstag(conf_path);
  // }
  start_time = clock();

  std::vector<FLOAT> J = calculate_current(angles);
  std::vector<loop *> LL = calculate_clusters(J);

  std::cout << "number of clusters " << LL.size() << std::endl;

  int length;

  std::map<int, int> lengths;
  std::map<int, int> windings;
  std::vector<int> lengths_mu;

  double mass = 0;
  double dimension = 0;
  int length_max = 0;
  int length_max_id;

  for (int i = 0; i < LL.size(); i++) {
    length = cluster_length(LL[i]);
    lengths[length]++;
    lengths_mu = length_mu(LL[i]);

    for (int j = 0; j < 4; j++) {
      if (lengths_mu[j] != 0) {
        windings[abs(lengths_mu[j])]++;
      }
    }

    if (lengths_mu[0] != 0 && lengths_mu[1] != 0 && lengths_mu[2] != 0 &&
        lengths_mu[3] != 0) {
      mass += length / cluster_variation(LL[i]);
    }

    if (length > length_max) {
      length_max_id = i;
      length_max = length;
    }
  }

  length = cluster_length(LL[length_max_id]);
  dimension =
      1. * cluster_length(LL[length_max_id]) / site_number(LL[length_max_id]);

  std::ofstream ofstream_lengths;
  std::ofstream ofstream_windings;
  std::ofstream ofstream_observables;

  ofstream_lengths.precision(17);
  ofstream_windings.precision(17);
  ofstream_observables.precision(17);

  ofstream_lengths.open(output_lengths);
  ofstream_windings.open(output_windings);
  ofstream_observables.open(output_observables);

  ofstream_lengths << "length,number" << std::endl;

  for (auto it = lengths.begin(); it != lengths.end(); ++it) {
    ofstream_lengths << it->first << "," << it->second << std::endl;
  }

  ofstream_windings << "windings,number" << std::endl;

  for (auto it = windings.begin(); it != windings.end(); ++it) {
    ofstream_windings << it->first << "," << it->second << std::endl;
  }

  ofstream_observables << "mass,dimension" << std::endl;

  ofstream_observables << mass << "," << dimension << std::endl;

  ofstream_lengths.close();
  ofstream_windings.close();
  ofstream_observables.close();
}
