from tests.base_case import TestCase
from pymesh.aabb_tree import distance_to_mesh, BVH
from pymesh.meshutils import generate_box_mesh

import numpy as np


class DistanceToMeshTest(TestCase):
    def test_boundary_pts_cgal(self):
        mesh = generate_box_mesh(np.array([0, 0, 0]), np.array([1, 1, 1]))
        pts = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])

        sq_dist, face_idx, closest_pts = distance_to_mesh(mesh, pts, "cgal")
        self.assert_array_equal(sq_dist, np.zeros(2))

    def test_boundary_pts_geogram(self):
        mesh = generate_box_mesh(np.array([0, 0, 0]), np.array([1, 1, 1]))
        pts = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])

        if "geogram" in BVH.available_engines:
            sq_dist, face_idx, closest_pts = distance_to_mesh(mesh, pts, "geogram")
            self.assert_array_equal(sq_dist, np.zeros(2))
