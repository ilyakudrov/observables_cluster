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
  std::string output_path_wilson;
  std::string output_path_sizes;
  int L_spat, L_time;
  int T_min, T_max;
  FLOAT R_min, R_max;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (std::string(argv[i]) == "-conf_path") {
      conf_path = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_wilson") {
      output_path_wilson = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_sizes") {
      output_path_sizes = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-T_min") {
      T_min = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-T_max") {
      T_max = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_min") {
      R_min = stod(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_max") {
      R_max = stod(std::string(argv[++i]));
    }
  }

  std::cout << "conf_format " << conf_format << std::endl;
  std::cout << "conf_path " << conf_path << std::endl;
  std::cout << "output_path_wilson " << output_path_wilson << std::endl;
  std::cout << "output_path_sizes " << output_path_sizes << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;
  std::cout << "T_min " << T_min << std::endl;
  std::cout << "T_max " << T_max << std::endl;
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

  std::vector<std::vector<int>> directions;
  directions = generate_directions(4);
  // directions.push_back({1, 0, 0});

  std::vector<wilson_result> wilson_offaxis_result =
      wilson_offaxis(conf.array, directions, R_min, R_max, T_min, T_max);

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << " calculating time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  wilson_offaxis_reduce(wilson_offaxis_result);

  // write data into two separate files
  // one is for wilson loops and the second is for sizes

  std::ofstream ofstream_wilson;

  ofstream_wilson.precision(17);

  ofstream_wilson.open(output_path_wilson);

  ofstream_wilson << "time_size,space_size,wilson_loop" << std::endl;

  for (int i = 0; i < wilson_offaxis_result.size(); i++) {
    ofstream_wilson << wilson_offaxis_result[i].time_size << ","
                    << wilson_offaxis_result[i].space_size << ","
                    << wilson_offaxis_result[i].wilson_loop << std::endl;
  }

  ofstream_wilson.close();
}
