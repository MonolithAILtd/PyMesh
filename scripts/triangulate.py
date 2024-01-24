#!/usr/bin/env python
"""
Triangulate the input.
"""

import argparse
import pymesh.meshio as mio
import pymesh.meshutils as mu
from pymesh.timethis import timethis
from pymesh.triangulate import triangulate_beta


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--engine",
        choices=[
            "igl_lexicographic",
            "igl_delaunay",
            "shewchuk_triangle",
            "cgal_delaunay",
            "geogram_delaunay",
        ],
    )
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh, drop_zero_dim=True)
    mesh, __ = mu.split_long_edges(mesh, 0.01)
    points = mesh.vertices[mesh.boundary_vertices, :]
    mesh = triangulate_beta(points, args.engine)
    mio.save_mesh(args.output_mesh, mesh)
    timethis.summarize()


if __name__ == "__main__":
    main()
