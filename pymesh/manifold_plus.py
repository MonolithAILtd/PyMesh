import PyMesh
from .mesh import Mesh
from .meshio import form_mesh


def compute_manifold_mesh_plus(mesh: Mesh, depth: int):
    engine = PyMesh.ManifoldPlus()
    engine.set_mesh(mesh.vertices, mesh.faces)
    engine.run(depth)
    manifold_mesh = form_mesh(
        engine.get_manifold_vertices(), engine.get_manifold_faces()
    )
    return manifold_mesh
