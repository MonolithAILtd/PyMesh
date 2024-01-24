#!/usr/bin/env python

"""
Extract the surface triangle mesh from a tet mesh.
"""

import argparse
import pymesh.meshutils as mu
import pymesh.meshio as mio


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    mesh = mio.form_mesh(mesh.vertices, mesh.faces)
    mesh, __ = mu.remove_isolated_vertices(mesh)
    mio.save_mesh(args.output_mesh, mesh)


if __name__ == "__main__":
    main()
