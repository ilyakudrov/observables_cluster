#include "basic_observables.h"
#include "data.h"
#include "link.h"
#include "matrix.h"

#include <iostream>

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
  std::string conf_path;
  std::string output_path;
  int L_spat, L_time;
  int bites_skip = 0;
  for (int i = 1; i < argc; i++) {
    if (std::string(argv[i]) == "-conf_format") {
      conf_format = argv[++i];
    } else if (string(argv[i]) == "-bites_skip") {
      bites_skip = stoi(string(argv[++i]));
    } else if (std::string(argv[i]) == "-conf_path") {
      conf_path = argv[++i];
    } else if (std::string(argv[i]) == "-output_path") {
      output_path = argv[++i];
    } else if (std::string(argv[i]) == "-L_spat") {
      L_spat = stoi(std::string(argv[++i]));
    } else if (std::string(argv[i]) == "-L_time") {
      L_time = stoi(std::string(argv[++i]));
    }
  }

  std::cout << "conf_format " << conf_format << std::endl;
  std::cout << "conf_path " << conf_path << std::endl;
  cout << "bites_skip " << bites_skip << endl;
  std::cout << "output_path " << output_path << std::endl;
  std::cout << "L_spat " << L_spat << std::endl;
  std::cout << "L_time " << L_time << std::endl;

  x_size = L_spat;
  y_size = L_spat;
  z_size = L_spat;
  t_size = L_time;

  data<MATRIX_PLAKET> conf;

  if (std::string(conf_format) == "float") {
    conf.read_float(conf_path, bites_skip);
  } else if (std::string(conf_format) == "double") {
    conf.read_double(conf_path, bites_skip);
  } else if (std::string(conf_format) == "double_qc2dstag") {
    conf.read_double_qc2dstag(conf_path);
  }
  start_time = clock();

  std::ofstream ofstream_wilson;

  ofstream_wilson.precision(17);

  ofstream_wilson.open(output_path);

  double plaket_result = plaket(conf.array);

  cout << "plaket = " << plaket_result << endl;

  ofstream_wilson << "plaket" << std::endl;

  ofstream_wilson << plaket_result << std::endl;

  ofstream_wilson.close();
}
