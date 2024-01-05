# Enumerate source files
file(GLOB SRC_FILES *.cpp)
file(GLOB INC_FILES *.h)

add_library(lib_ManifoldPlus SHARED)
add_library(PyMesh::ManifoldPlus ALIAS lib_ManifoldPlus)
set_target_properties(lib_ManifoldPlus PROPERTIES OUTPUT_NAME "PyMesh-ManifoldPlus")
target_link_libraries(lib_ManifoldPlus
    PUBLIC
        PyMesh::Mesh
        PyMesh::Tools
        PyMesh::third_party::libigl 
)

target_sources(lib_ManifoldPlus PRIVATE ${INC_FILES} ${SRC_FILES})
