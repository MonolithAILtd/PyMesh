from tests.base_case import TestCase
from pymesh.csg_tree import CSGTree
from pymesh.meshutils import generate_box_mesh

import numpy as np


class CSGTreeTest(TestCase):
    def test_single_mesh(self):
        mesh = generate_box_mesh(np.zeros(3), np.ones(3))
        tree = CSGTree({"mesh": mesh})
        self.assert_array_equal(mesh.vertices, tree.vertices)
        self.assert_array_equal(mesh.faces, tree.faces)
