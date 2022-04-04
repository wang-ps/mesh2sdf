#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <vector>

#include "makelevelset3.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

py::array_t<float> compute(py::array_t<float> vertices,
                           py::array_t<unsigned int> faces, int size) {
  // input
  std::vector<Vec3f> V;
  for (int i = 0; i < vertices.shape(0); ++i) {
    V.push_back(Vec3f(vertices.at(i, 0), vertices.at(i, 1), vertices.at(i, 2)));
  }
  std::vector<Vec3ui> F;
  for (int i = 0; i < faces.shape(0); ++i) {
    F.push_back(Vec3ui(faces.at(i, 0), faces.at(i, 1), faces.at(i, 2)));
  }

  // bounding box
  Vec3f bbmin(-1.0f, -1.0f, -1.0f);
  Vec3f bbmax(1.0f, 1.0f, 1.0f);
  float dx = 2.0f / (float)size;

  // compute level sets
  Array3f grid;
  make_level_set3(F, V, bbmin, dx, size, size, size, grid);

  // output
  py::array_t<float> sdf({size, size, size});
  for (int x = 0; x < size; x++) {
    for (int y = 0; y < size; y++) {
      for (int z = 0; z < size; z++) {
        sdf.mutable_at(x, y, z) = grid(x, y, z);
      }
    }
  }
  return sdf;
}

PYBIND11_MODULE(core, m) {
  m.def("compute", &compute, R"pbdoc(
        Compute the SDF from an input mesh.

        Args:
          vertices (np.ndarray): The vertex array with shape (Nv, 3), and
              vertices MUST be in range [-1, 1].
          faces (np.ndarray): The face array with shape (Nf, 3).
          size (int): The resolution of resulting SDF.
        )pbdoc",
        py::arg("vertices"), py::arg("faces"), py::arg("size") = 128);

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
