#include <memory>

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <ManifoldPlus/Manifold.h>

namespace py = pybind11;
using namespace PyMesh;

void init_ManifoldPlus(py::module &m) {
  py::class_<Manifold, std::shared_ptr<Manifold>>(m, "ManifoldPlus")
      .def(py::init<>())
      .def("set_mesh", &Manifold::setMesh)
      .def("run", &Manifold::run)
      .def("get_manifold_vertices", &Manifold::getManifoldVertices)
      .def("get_manifold_faces", &Manifold::getManifoldFaces);
}
