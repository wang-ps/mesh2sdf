#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>

#include "makelevelset3.h"

void load_obj(std::vector<Vec3f>& vertList, std::vector<Vec3ui>& faceList,
              const std::string filename) {
  std::cout << "Reading data.\n";
  std::ifstream infile(filename);
  if (!infile) {
    std::cerr << "Failed to open. Terminating.\n";
    exit(-1);
  }

  int ignored_lines = 0;
  std::string line;
  while (!infile.eof()) {
    std::getline(infile, line);
    //.obj files sometimes contain vertex normals indicated by "vn"
    if (line.substr(0, 1) == std::string("v") &&
        line.substr(0, 2) != std::string("vn")) {
      std::stringstream data(line);
      char c;
      Vec3f point;
      data >> c >> point[0] >> point[1] >> point[2];
      vertList.push_back(point);
    } else if (line.substr(0, 1) == std::string("f")) {
      std::stringstream data(line);
      char c;
      int v0, v1, v2;
      data >> c >> v0 >> v1 >> v2;
      faceList.push_back(Vec3ui(v0 - 1, v1 - 1, v2 - 1));
    } else if (line.substr(0, 2) == std::string("vn")) {
      std::cerr << "Obj-loader is not able to parse vertex normals, please "
                   "strip them from the input file. \n";
      exit(-2);
    } else {
      ++ignored_lines;
    }
  }
  infile.close();
  if (ignored_lines > 0) {
    std::cout << "Warning: " << ignored_lines
              << " lines were ignored since they did not contain faces or"
                 " vertices.\n";
  }
  std::cout << "Read in " << vertList.size() << " vertices and "
            << faceList.size() << " faces." << std::endl;
}

int main(int argc, char* argv[]) {
  if (argc != 3) {
    std::cout << "SDFGen - A utility for converting closed oriented triangle "
                 "meshes into grid-based signed distance fields.\n";
    std::cout << "\nThe output file format is:";
    std::cout << "<value_1> <value_2> <value_3> [...]\n\n";
    std::cout << "<value_n> are the signed distance data values, in ascending "
                 "order of i, then j, then k.\n";

    std::cout << "The output filename will match that of the input, with the "
                 "OBJ suffix replaced with SDF.\n\n";

    std::cout << "Usage: SDFGen <filename> <dx>\n\n";
    std::cout << "Where:\n";
    std::cout << "\t<filename> specifies a Wavefront OBJ (text) file "
                 "representing a *triangle* mesh (no quad or poly meshes "
                 "allowed). File must use the suffix \".obj\".\n";
    std::cout << "\t<dx> specifies the length of grid cell in the resulting "
                 "distance field.\n";

    exit(-1);
  }

  // Parse cmd paramters
  std::string filename(argv[1]);
  if (filename.size() < 5 ||
      filename.substr(filename.size() - 4) != std::string(".obj")) {
    std::cerr
        << "Error: Expected OBJ file with filename of the form <name>.obj.\n";
    exit(-1);
  }

  std::stringstream arg2(argv[2]);
  float dx;
  arg2 >> dx;

  // Load the obj file
  std::vector<Vec3f> vertList;
  std::vector<Vec3ui> faceList;
  load_obj(vertList, faceList, filename);

  // Set bounding box
  Vec3f min_box(-1.0f, -1.0f, -1.0f);
  Vec3f max_box(1.0f, 1.0f, 1.0f);

  // Add padding around the box.
  Vec3f unit(1, 1, 1);
  Vec3ui sizes = Vec3ui((max_box - min_box) / dx);
  std::cout << "Bound box size: (" << min_box << ") to (" << max_box
            << ") with dimensions " << sizes << "." << std::endl;

  // Make level sets
  std::cout << "Computing signed distance field.\n";
  Array3f phi_grid;
  make_level_set3(faceList, vertList, min_box, dx, sizes[0], sizes[1], sizes[2],
                  phi_grid);

  // Save to binary files
  std::string outname;
  outname = filename.substr(0, filename.size() - 4) + std::string(".sdf");
  std::cout << "Writing results to: " << outname << "\n";
  std::ofstream outfile(outname, std::ios::binary);
  outfile.write((char*)phi_grid.a.data, phi_grid.a.size() * sizeof(float));
  outfile.close();
  std::cout << "Processing complete.\n";

  

  return 0;
}
