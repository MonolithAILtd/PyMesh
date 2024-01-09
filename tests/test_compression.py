from pymesh.compression import compress, decompress
from pymesh.meshutils import generate_icosphere
from pymesh.meshio import form_mesh
from tests.base_case import TestCase

import numpy as np
import numpy.random


class TestCompression(TestCase):
    def test_simple(self):
        mesh = generate_icosphere(1.0, np.zeros(3), 2)
        data = compress(mesh)
        mesh2 = decompress(data)

        self.assertEqual(mesh.num_vertices, mesh2.num_vertices)
        self.assertEqual(mesh.num_faces, mesh2.num_faces)
        self.assert_array_almost_equal(mesh.bbox, mesh2.bbox)

    def test_point_cloud(self):
        vertices = numpy.random.rand(100, 3)
        mesh = form_mesh(vertices, np.zeros((0, 3)))
        data = compress(mesh)
        mesh2 = decompress(data)

        self.assertEqual(mesh.num_vertices, mesh2.num_vertices)
        self.assertEqual(mesh.num_faces, mesh2.num_faces)
        self.assert_array_almost_equal(mesh.bbox, mesh2.bbox)

    def test_2D(self):
        vertices = numpy.array(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
                [0.0, 1.0],
            ]
        )
        faces = np.array([[0, 1, 2], [0, 2, 3]])
        mesh = form_mesh(vertices, faces)
        data = compress(mesh)
        mesh2 = decompress(data)

        self.assertEqual(mesh.num_vertices, mesh2.num_vertices)
        self.assertEqual(mesh.num_faces, mesh2.num_faces)
        self.assert_array_almost_equal(mesh.bbox, mesh2.bbox)

    def test_quad(self):
        vertices = numpy.array(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [1.0, 1.0],
                [0.0, 1.0],
            ]
        )
        faces = np.array(
            [
                [0, 1, 2, 3],
            ]
        )
        mesh = form_mesh(vertices, faces)

        with self.assertRaises(RuntimeError):
            _ = compress(mesh)

    def test_empty_mesh(self):
        vertices = numpy.zeros((0, 3), dtype=float)
        faces = np.zeros((0, 3), dtype=int)
        mesh = form_mesh(vertices, faces)

        data = compress(mesh)
        mesh2 = decompress(data)

        self.assertEqual(mesh.num_vertices, mesh2.num_vertices)
        self.assertEqual(mesh.num_faces, mesh2.num_faces)

    def test_attributes(self):
        mesh = generate_icosphere(1.0, np.zeros(3), 2)
        mesh.add_attribute("vertex_index")
        mesh.add_attribute("vertex_normal")
        mesh.add_attribute("face_index")
        mesh.add_attribute("face_normal")
        data = compress(mesh)
        mesh2 = decompress(data)

        self.assertEqual(mesh.num_vertices, mesh2.num_vertices)
        self.assertEqual(mesh.num_faces, mesh2.num_faces)
        self.assert_array_almost_equal(mesh.bbox, mesh2.bbox)
        self.assertTrue(mesh2.has_attribute("vertex_index"))
        self.assertTrue(mesh2.has_attribute("vertex_normal"))
        # self.assertTrue(mesh2.has_attribute("face_index"))
        # self.assertTrue(mesh2.has_attribute("face_normal"))

        vertex_index_map = mesh2.get_attribute("vertex_index").ravel().astype(int)
        out_vertices = mesh2.vertices
        in_vertices = mesh.vertices[vertex_index_map]
        self.assert_array_equal(in_vertices, out_vertices)

        # face_index_map = mesh2.get_attribute("face_index").ravel().astype(int)
        # self.assertEqual(mesh.num_faces, len(face_index_map))
