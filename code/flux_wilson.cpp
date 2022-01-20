#include "basic_observables.h"
#include "data.h"
#include "flux_tube.h"
#include "link.h"
#include "matrix.h"
#include "result.h"

#include <numeric>
#include <iostream>
#include <map>

int x_size;
int y_size;
int z_size;
int t_size;

using namespace std;

int main(int argc, char *argv[]) {
  unsigned int start_time;
  unsigned int end_time;
  unsigned int search_time;

  std::string conf_format;
  std::string smeared_format;
  std::string conf_path;
  std::string smeared_path;
  std::string output_path_electric;
  std::string output_path_magnetic;
  int L_spat, L_time;
  int R, T;
  int x_trans;
  int bites_skip = 4;
  int bites_skip_smeared = 4;
  // int T_min, T_max;
  // FLOAT R_min, R_max;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (string(argv[i]) == "-bites_skip") {
      bites_skip = stoi(string(argv[++i]));
    } else if (std::string(argv[i]) == "-smeared_format") {
      smeared_format = argv[++i];
    } else if (string(argv[i]) == "-bites_skip_smeared") {
      bites_skip_smeared = stoi(string(argv[++i]));
    } else if (std::string(argv[i]) == "-conf_path") {
      conf_path = argv[++i];
    } else if (std::string(argv[i]) == "-smeared_path") {
      smeared_path = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_electric") {
      output_path_electric = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_magnetic") {
      output_path_magnetic = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_size") {
      R = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-T_size") {
      T = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-x_trans") {
      x_trans = stoi(std::string(argv[++i]));
    }
    // else if (std::string(argv[i]) == "-T_min") { T_min =
    // stoi(std::string(argv[++i])); } else if (std::string(argv[i]) ==
    // "-T_max") { T_max = stoi(std::string(argv[++i])); } else if
    // (std::string(argv[i]) ==
    // "-R_min") { R_min = stoi(std::string(argv[++i])); } else if
    // (std::string(argv[i]) == "-R_max") { R_max =
    // stoi(std::string(argv[++i]));
    // }
  }

  std::cout << "conf_format " << conf_format << std::endl;
  cout << "bites_skip " << bites_skip << endl;
  std::cout << "smeared_format " << smeared_format << std::endl;
  cout << "bites_skip_smeared " << bites_skip_smeared << endl;
  std::cout << "conf_path " << conf_path << std::endl;
  std::cout << "smeared_path " << smeared_path << std::endl;
  std::cout << "output_path_electric " << output_path_electric << std::endl;
  std::cout << "output_path_magnetic " << output_path_magnetic << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;
  std::cout << "R " << R << std::endl;
  std::cout << "T " << T << std::endl;
  std::cout << "x_trans " << x_trans << std::endl;
  
  // std::cout<<"T_min "<<T_min<<std::endl;
  // std::cout<<"T_max "<<T_max<<std::endl;
  // std::cout<<"R_min "<<R_min<<std::endl;
  // std::cout<<"R_max "<<R_max<<std::endl;

  x_size = L_spat;
  y_size = L_spat;
  z_size = L_spat;
  t_size = L_time;

  int d_min = -5;
  int d_max = R + 5;

  data<MATRIX> conf;
  data<MATRIX_SMEARED> smeared;

  if (std::string(conf_format) == "float") {
    conf.read_float(conf_path);
  } else if (std::string(conf_format) == "double") {
    conf.read_double(conf_path);
  } else if (std::string(conf_format) == "double_fortran") {
    conf.read_double_fortran(conf_path, bites_skip);
  } else if (std::string(conf_format) == "float_fortran") {
    conf.read_float_fortran(conf_path, bites_skip);
  } else if (std::string(conf_format) == "double_qc2dstag") {
    conf.read_double_qc2dstag(conf_path);
  }

  if (std::string(smeared_format) == "float") {
    smeared.read_float(smeared_path);
  } else if (std::string(smeared_format) == "double") {
    smeared.read_double(smeared_path);
  } else if (std::string(smeared_format) == "double_fortran") {
    smeared.read_double_fortran(smeared_path, bites_skip_smeared);
  } else if (std::string(smeared_format) == "float_fortran") {
    smeared.read_float_fortran(smeared_path, bites_skip_smeared);
  } else if (std::string(smeared_format) == "double_qc2dstag") {
    smeared.read_double_qc2dstag(smeared_path);
  }
  double plaket_time_average = plaket_time(conf.array);
  double plaket_space_average = plaket_space(conf.array);

  start_time = clock();

  vector<FLOAT> wilson_loop_trace = calculate_wilson_loop_tr(smeared.array, R, T);
  vector<FLOAT> plaket_time_trace = calculate_plaket_time_tr(conf.array);
  vector<FLOAT> plaket_space_trace = calculate_plaket_space_tr(conf.array);

  double wilson_loop_average = accumulate(wilson_loop_trace.cbegin(), wilson_loop_trace.cend(), 0.0) / wilson_loop_trace.size();
  cout<<"wilson_loop_average = "<<wilson_loop_average<<endl;

  std::cout << "plaket_time " << plaket_time_average << " smeared_plaket_time "<< plaket_time(smeared.array) << std::endl;
  std::cout << "plaket_space " << plaket_space_average << " smeared_plaket_space "<< plaket_space(smeared.array) << std::endl;

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << "preparation time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  start_time = clock();
  std::map<int, FLOAT> res1 = wilson_plaket_correlator_electric(
       wilson_loop_trace, plaket_time_trace, R, T, x_trans, d_min, d_max);
  std::vector<FLOAT> res2 = wilson_plaket_correlator_magnetic(
       wilson_loop_trace, plaket_space_trace, R, T, x_trans, d_min, d_max);

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << "T=" << T << " R=" << R
            << " calculating time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  std::ofstream stream_electric;
  std::ofstream stream_magnetic;

  stream_electric.precision(17);
  stream_magnetic.precision(17);

  stream_electric.open(output_path_electric);
  stream_magnetic.open(output_path_magnetic);

  stream_electric << "d,wilson-plaket-correlator,wilson-loop,plaket"
                  << std::endl;

  stream_magnetic << "d,wilson-plaket-correlator,wilson-loop,plaket"
                  << std::endl;

  for (auto it = res1.begin(); it != res1.end(); ++it) {
    stream_electric << it->first << "," << it->second << "," << wilson_loop_average << "," << plaket_time_average
                    << std::endl;
  }

  for (int i = 0; i < res2.size(); i++) {
    stream_magnetic << d_min + i << "," << res2[i] << "," << wilson_loop_average << "," << plaket_space_average
                    << std::endl;
  }

  stream_electric.close();
  stream_magnetic.close();
}
