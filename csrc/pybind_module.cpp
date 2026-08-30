#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "simpson.cpp"
#include <cstdint>

namespace py = pybind11;

PYBIND11_MODULE(simpson_ext, m) {
    m.doc() = "Integration module for SimpsonIntegrator";

    py::class_<SimpsonIntegrator>(m, "SimpsonIntegrator")
        .def_static("integrate", py::overload_cast<const std::vector<double>&, const std::vector<double>&>(&SimpsonIntegrator::integrate), "Integration using discrete vectors")
        .def_static("integrate", py::overload_cast<const std::function<double(double)>&, const double, const double, const uint64_t>(&SimpsonIntegrator::integrate), "Integration using a function")
        .def_static("integrate", py::overload_cast<const std::string&, const double, const double, const uint64_t, const std::string&>(&SimpsonIntegrator::integrate),
            py::arg("expression_str"), py::arg("a"), py::arg("b"), py::arg("n"), py::arg("var_name") = "x",
            "Integration evaluating the function with exprtk");
}