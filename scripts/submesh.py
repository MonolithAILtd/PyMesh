#!/usr/bin/env python

"""
Extract a subset of faces of the input mesh.
"""

import argparse
import pymesh.meshio as mio
from pymesh.submesh import submesh


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--n-ring", "-n", type=int, default=0, help="Expand the selection by n-rings"
    )
    parser.add_argument("input_mesh", help="input mesh")
    parser.add_argument("output_mesh", help="output mesh")
    parser.add_argument(
        "face_indices", nargs="+", type=int, help="indices of faces to be extracted"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    mesh = submesh(mesh, args.face_indices, args.n_ring)
    mio.save_mesh(args.output_mesh, mesh, *mesh.get_attribute_names())


if __name__ == "__main__":
    main()
