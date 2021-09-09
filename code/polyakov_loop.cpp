#include "basic_observables.h"
#include "data.h"
#include "link.h"
#include "matrix.h"
#include "result.h"

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
  std::string output_path_polyakov;
  std::string output_path_sizes;
  int L_spat, L_time;
  FLOAT R_min, R_max;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (std::string(argv[i]) == "-conf_path") {
      conf_path = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_polyakov") {
      output_path_polyakov = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_sizes") {
      output_path_sizes = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_min") {
      R_min = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_max") {
      R_max = stoi(std::string(argv[++i]));
    }
  }

  std::cout << "conf_format " << conf_format << std::endl;
  std::cout << "conf_path " << conf_path << std::endl;
  std::cout << "output_path_polyakov " << output_path_polyakov << std::endl;
  std::cout << "output_path_sizes " << output_path_sizes << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;
  std::cout << "R_min " << R_min << std::endl;
  std::cout << "R_max " << R_max << std::endl;

  x_size = L_spat;
  y_size = L_spat;
  z_size = L_spat;
  t_size = L_time;

  data<MATRIX> conf;

  if (std::string(conf_format) == "float") {
    conf.read_float(conf_path);
  } else if (std::string(conf_format) == "double") {
    conf.read_double(conf_path);
  } else if (std::string(conf_format) == "double_fortran") {
    conf.read_double_fortran(conf_path);
  } else if (std::string(conf_format) == "float_fortran") {
    conf.read_float_fortran(conf_path);
  } else if (std::string(conf_format) == "double_qc2dstag") {
    conf.read_double_qc2dstag(conf_path);
  }
  start_time = clock();

  std::map<int, FLOAT> polyakov_correlator =
      polyakov_loop_correlator(conf.array, R_min, R_max);

  for (auto it = polyakov_correlator.begin(); it != polyakov_correlator.end();
       ++it) {
    std::cout << "distance: " << it->first
              << " polyakov_correlator: " << it->second << std::endl;
  }

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << " calculating time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  // write data into two separate files
  // one is for wilson loops and the second is for sizes

  std::ofstream ofstream_polyakov;

  ofstream_polyakov.precision(17);

  ofstream_polyakov.open(output_path_polyakov);

  ofstream_polyakov << "distance,polyakov_loop" << std::endl;

  for (auto it = polyakov_correlator.begin(); it != polyakov_correlator.end();
       ++it) {
    ofstream_polyakov << it->first << "," << it->second << std::endl;
  }

  ofstream_polyakov.close();
}
