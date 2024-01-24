#!/usr/bin/env python

""" Refine 2D triangulation
"""

import argparse
import pymesh.meshio as mio
import pymesh.meshutils as mu
from pymesh.aabb_tree import AABBTree2
from pymesh.triangulate import refine_triangulation
import numpy as np
from numpy.linalg import norm


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--engine",
        help="Triangulation engine",
        choices=("triangle_refiner", "mmg_delaunay"),
        default="auto",
    )
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def compute_metric(mesh):
    if mesh.has_attribute("cell"):
        cell_ids = mesh.get_attribute("cell").astype(int).ravel()
        cut_mesh = mu.cut_mesh(mesh, cell_ids)
    else:
        cut_mesh = mesh

    tree = AABBTree2()
    tree.load_data(cut_mesh.vertices, cut_mesh.boundary_edges)
    sq_dist, indices = tree.look_up(mesh.vertices)
    dist = np.sqrt(sq_dist)

    bbox_min, bbox_max = mesh.bbox
    tol = norm(bbox_max - bbox_min) / 20.0

    metric = np.clip(dist / tol, 0.1, 1.0) * tol
    return metric


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh, drop_zero_dim=True)
    metric = compute_metric(mesh)
    mesh = refine_triangulation(mesh, metric, engine=args.engine)
    mio.save_mesh(args.output_mesh, mesh)


if __name__ == "__main__":
    main()
