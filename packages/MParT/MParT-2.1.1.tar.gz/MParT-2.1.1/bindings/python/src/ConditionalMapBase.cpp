#include "CommonPybindUtilities.h"
#include "MParT/ConditionalMapBase.h"
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

#include <Kokkos_Core.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace mpart::binding;

template<typename MemorySpace>
void mpart::binding::ConditionalMapBaseWrapper(py::module &m)
{
    std::string tName = "ConditionalMapBase";
    if(!std::is_same<MemorySpace,Kokkos::HostSpace>::value) tName = "d" + tName;

    // ConditionalMapBase
    py::class_<ConditionalMapBase<MemorySpace>, ParameterizedFunctionBase<MemorySpace>, std::shared_ptr<ConditionalMapBase<MemorySpace>>>(m, tName.c_str())

        .def("LogDeterminant", static_cast<Eigen::VectorXd (ConditionalMapBase<MemorySpace>::*)(Eigen::Ref<const Eigen::RowMatrixXd> const&)>(&ConditionalMapBase<MemorySpace>::LogDeterminant))
        .def("Inverse", static_cast<Eigen::RowMatrixXd (ConditionalMapBase<MemorySpace>::*)(Eigen::Ref<const Eigen::RowMatrixXd> const&, Eigen::Ref<const Eigen::RowMatrixXd> const&)>(&ConditionalMapBase<MemorySpace>::Inverse))
        .def("LogDeterminantCoeffGrad", static_cast<Eigen::RowMatrixXd (ConditionalMapBase<MemorySpace>::*)(Eigen::Ref<const Eigen::RowMatrixXd> const&)>(&ConditionalMapBase<MemorySpace>::LogDeterminantCoeffGrad))
        .def("LogDeterminantInputGrad", static_cast<Eigen::RowMatrixXd (ConditionalMapBase<MemorySpace>::*)(Eigen::Ref<const Eigen::RowMatrixXd> const&)>(&ConditionalMapBase<MemorySpace>::LogDeterminantInputGrad))
        .def("GetBaseFunction", &ConditionalMapBase<MemorySpace>::GetBaseFunction)
        ;

}

template void mpart::binding::ConditionalMapBaseWrapper<Kokkos::HostSpace>(py::module&);
#if defined(MPART_ENABLE_GPU)
template void mpart::binding::ConditionalMapBaseWrapper<mpart::DeviceSpace>(py::module&);
#endif // MPART_ENABLE_GPU