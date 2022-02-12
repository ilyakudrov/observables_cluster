#include "basic_observables.h"
#include "data.h"
#include "flux_tube.h"
#include "link.h"
#include "matrix.h"

#include <cstring>
#include <iostream>
#include <map>
#include <numeric>
#include <string>

int x_size;
int y_size;
int z_size;
int t_size;

using namespace std;

int main(int argc, char *argv[]) {
  unsigned int start_time;
  unsigned int end_time;
  unsigned int search_time;

  std::string conf_format_plaket;
  std::string conf_format_wilson;
  std::string conf_path_plaket;
  std::string conf_path_wilson;
  std::string output_path_electric;
  std::string output_path_magnetic;
  int L_spat, L_time;
  int x_trans_max;
  int bites_skip_plaket = 0;
  int bites_skip_wilson = 0;
  int T_min, T_max;
  int R_min, R_max;
  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-conf_format_plaket") == 0) {
      conf_format_plaket = argv[++i];
    } else if (string(argv[i]) == "-bites_skip_plaket") {
      bites_skip_plaket = stoi(string(argv[++i]));
    } else if (std::string(argv[i]) == "-conf_format_wilson") {
      conf_format_wilson = argv[++i];
    } else if (string(argv[i]) == "-bites_skip_wilson") {
      bites_skip_wilson = stoi(string(argv[++i]));
    } else if (std::string(argv[i]) == "-conf_path_plaket") {
      conf_path_plaket = argv[++i];
    } else if (std::string(argv[i]) == "-conf_path_wilson") {
      conf_path_wilson = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_electric") {
      output_path_electric = argv[++i];
    } else if (std::string(argv[i]) == "-output_path_magnetic") {
      output_path_magnetic = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-x_trans_max") {
      x_trans_max = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-T_min") {
      T_min = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-T_max") {
      T_max = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_min") {
      R_min = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-R_max") {
      R_max = stoi(std::string(argv[++i]));
    }
  }

  std::cout << "conf_format_plaket " << conf_format_plaket << std::endl;
  cout << "bites_skip_plaket " << bites_skip_plaket << endl;
  std::cout << "conf_format_wilson " << conf_format_wilson << std::endl;
  cout << "bites_skip_wilson " << bites_skip_wilson << endl;
  std::cout << "conf_path_plaket " << conf_path_plaket << std::endl;
  std::cout << "conf_path_wilson " << conf_path_wilson << std::endl;
  std::cout << "output_path_electric " << output_path_electric << std::endl;
  std::cout << "output_path_magnetic " << output_path_magnetic << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;
  std::cout << "R_min " << R_min << std::endl;
  std::cout << "R_max " << R_max << std::endl;
  std::cout << "T_min " << T_min << std::endl;
  std::cout << "T_max " << T_max << std::endl;
  std::cout << "x_trans_max " << x_trans_max << std::endl;

  x_size = L_spat;
  y_size = L_spat;
  z_size = L_spat;
  t_size = L_time;

  data<MATRIX_PLAKET> conf_plaket;
  data<MATRIX_WILSON> conf_wilson;

  if (std::string(conf_format_plaket) == "float") {
    conf_plaket.read_float(conf_path_plaket, bites_skip_plaket);
  } else if (std::string(conf_format_plaket) == "double") {
    conf_plaket.read_double(conf_path_plaket, bites_skip_plaket);
  } else if (std::string(conf_format_plaket) == "double_qc2dstag") {
    conf_plaket.read_double_qc2dstag(conf_path_plaket);
  }

  if (std::string(conf_format_wilson) == "float") {
    conf_wilson.read_float(conf_path_wilson, bites_skip_wilson);
  } else if (std::string(conf_format_wilson) == "double") {
    conf_wilson.read_double(conf_path_wilson, bites_skip_wilson);
  } else if (std::string(conf_format_wilson) == "double_qc2dstag") {
    conf_wilson.read_double_qc2dstag(conf_path_wilson);
  }
  double plaket_time_average = plaket_time(conf_plaket.array);
  double plaket_space_average = plaket_space(conf_plaket.array);

  start_time = clock();

  vector<double> wilson_loop_trace;
  vector<double> plaket_time_trace =
      calculate_plaket_time_tr(conf_plaket.array);
  vector<double> plaket_space_trace =
      calculate_plaket_space_tr(conf_plaket.array);
  double wilson_loop_average;

  std::cout << "plaket_time " << plaket_time_average << " smeared_plaket_time "
            << plaket_time(conf_wilson.array) << std::endl;
  std::cout << "plaket_space " << plaket_space_average
            << " smeared_plaket_space " << plaket_space(conf_wilson.array)
            << std::endl;

  std::ofstream stream_electric;
  std::ofstream stream_magnetic;

  stream_electric.precision(17);
  stream_magnetic.precision(17);

  stream_electric.open(output_path_electric);
  stream_magnetic.open(output_path_magnetic);

  cout << output_path_electric << endl;
  cout << output_path_magnetic << endl;

  stream_electric << "T,R,x_tr,wilson-plaket-correlator,wilson-loop,plaket"
                  << std::endl;

  stream_magnetic << "T,R,x_tr,wilson-plaket-correlator,wilson-loop,plaket"
                  << std::endl;

  std::map<int, double> correlator_electric;
  std::map<int, double> correlator_magnetic;

  for (int T = T_min; T <= T_max; T += 2) {
    for (int R = R_min; R <= R_max; R += 2) {

      int d = R / 2;

      wilson_loop_trace = calculate_wilson_loop_tr(conf_wilson.array, R, T);

      wilson_loop_average = accumulate(wilson_loop_trace.cbegin(),
                                       wilson_loop_trace.cend(), 0.0) /
                            wilson_loop_trace.size();
      cout << "wilson_loop_average = " << wilson_loop_average << endl;

      end_time = clock();
      search_time = end_time - start_time;
      std::cout << "preparation time: " << search_time * 1. / CLOCKS_PER_SEC
                << std::endl;

      start_time = clock();
      correlator_electric = wilson_plaket_correlator_electric_x(
          wilson_loop_trace, plaket_time_trace, R, T, x_trans_max, d);
      correlator_magnetic = wilson_plaket_correlator_magnetic_x(
          wilson_loop_trace, plaket_space_trace, R, T, x_trans_max, d);

      end_time = clock();
      search_time = end_time - start_time;
      std::cout << "T=" << T << " R=" << R
                << " calculating time: " << search_time * 1. / CLOCKS_PER_SEC
                << std::endl;

      for (auto it = correlator_electric.begin();
           it != correlator_electric.end(); ++it) {
        stream_electric << T << "," << R << "," << it->first << ","
                        << it->second << "," << wilson_loop_average << ","
                        << plaket_time_average << std::endl;
      }

      for (auto it = correlator_magnetic.begin();
           it != correlator_magnetic.end(); ++it) {
        stream_magnetic << T << "," << R << "," << it->first << ","
                        << it->second << "," << wilson_loop_average << ","
                        << plaket_space_average << std::endl;
      }
    }
  }

  stream_electric.close();
  stream_magnetic.close();
}
