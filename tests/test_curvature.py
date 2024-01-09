from tests.base_case import TestCase
from pymesh.meshutils import generate_icosphere
import numpy as np


class CurvatureTest(TestCase):
    def test_balls(self):
        ball_r1 = generate_icosphere(1.0, [0.0, 0.0, 0.0], 4)
        ball_r2 = generate_icosphere(2.0, [1.0, 0.0, 0.0], 4)
        ball_r3 = generate_icosphere(3.0, [0.0, 1.0, 0.0], 4)

        ball_r1.add_attribute("vertex_gaussian_curvature")
        ball_r2.add_attribute("vertex_gaussian_curvature")
        ball_r3.add_attribute("vertex_gaussian_curvature")

        ball_r1.add_attribute("vertex_mean_curvature")
        ball_r2.add_attribute("vertex_mean_curvature")
        ball_r3.add_attribute("vertex_mean_curvature")

        gaussian_r1 = ball_r1.get_attribute("vertex_gaussian_curvature")
        gaussian_r2 = ball_r2.get_attribute("vertex_gaussian_curvature")
        gaussian_r3 = ball_r3.get_attribute("vertex_gaussian_curvature")

        mean_r1 = ball_r1.get_attribute("vertex_mean_curvature")
        mean_r2 = ball_r2.get_attribute("vertex_mean_curvature")
        mean_r3 = ball_r3.get_attribute("vertex_mean_curvature")

        self.assertAlmostEqual(1.0, np.amin(gaussian_r1), 2)
        self.assertAlmostEqual(1.0 / 4.0, np.amin(gaussian_r2), 2)
        self.assertAlmostEqual(1.0 / 9.0, np.amin(gaussian_r3), 2)

        self.assertAlmostEqual(1.0, np.amin(mean_r1), 2)
        self.assertAlmostEqual(1.0 / 2.0, np.amin(mean_r2), 2)
        self.assertAlmostEqual(1.0 / 3.0, np.amin(mean_r3), 2)
