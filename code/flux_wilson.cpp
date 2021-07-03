#include "basic_observables.h"
#include "data.h"
#include "flux_tube.h"
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
  std::string smeared_format;
  std::string conf_path;
  std::string smeared_path;
  std::string output_path_electric;
  std::string output_path_magnetic;
  int L_spat, L_time;
  int R, T;
  int x_trans;
  // int T_min, T_max;
  // FLOAT R_min, R_max;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (std::string(argv[i]) == "-smeared_format") {
      smeared_format = argv[++i];
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
  std::cout << "smeared_format " << smeared_format << std::endl;
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
  data<MATRIX> smeared;

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

  if (std::string(smeared_format) == "float") {
    smeared.read_float(smeared_path);
  } else if (std::string(smeared_format) == "double") {
    smeared.read_double(smeared_path);
  } else if (std::string(conf_format) == "double_fortran") {
    smeared.read_double_fortran(smeared_path);
  } else if (std::string(conf_format) == "float_fortran") {
    smeared.read_float_fortran(smeared_path);
  } else if (std::string(conf_format) == "double_qc2dstag") {
    smeared.read_double_qc2dstag(smeared_path);
  }
  double c1 = plaket_time(conf.array);
  double c2 = plaket_space(conf.array);

  double a;
  double aver[2];
  result vec(0);
  result vec_plaket_time;
  result vec_plaket_space;

  start_time = clock();

  vec.array = calculate_wilson_loop_tr(smeared.array, R, T);
  vec_plaket_time.array = calculate_plaket_time_tr(conf.array);
  vec_plaket_space.array = calculate_plaket_space_tr(conf.array);
  vec.average(aver);
  double b = aver[0];
  vec_plaket_time.average(aver);
  std::cout << "plaket_time " << c1 << " " << aver[0] << std::endl;
  vec_plaket_space.average(aver);
  std::cout << "plaket_space " << c2 << " " << aver[0] << std::endl;

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << "preparation time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  start_time = clock();
  vector<FLOAT> res1 = wilson_plaket_correlator_electric(
      vec.array, vec_plaket_time.array, R, T, x_trans, d_min, d_max);
  vector<FLOAT> res2 = wilson_plaket_correlator_magnetic(
      vec.array, vec_plaket_space.array, R, T, x_trans, d_min, d_max);

  end_time = clock();
  search_time = end_time - start_time;
  std::cout << "T=" << T << " R=" << R
            << " calculating time: " << search_time * 1. / CLOCKS_PER_SEC
            << std::endl;

  ofstream stream_electric;
  ofstream stream_magnetic;

  stream_electric.precision(17);
  stream_magnetic.precision(17);

  stream_electric.open(output_path_electric);
  stream_magnetic.open(output_path_magnetic);

  stream_electric << "d,wilson-plaket-correlator,wilson-loop,plaket"
                  << std::endl;

  for (int i = 0; i < res1.size(); i++) {
    stream_electric << d_min + i << "," << res1[i] << "," << b << "," << c1
                    << std::endl;
  }

  for (int i = 0; i < res2.size(); i++) {
    stream_magnetic << d_min + i << "," << res2[i] << "," << b << "," << c2
                    << std::endl;
  }

  stream_electric.close();
  stream_magnetic.close();
}
