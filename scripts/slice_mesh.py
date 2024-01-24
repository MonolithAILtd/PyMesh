#!/usr/bin/env python

""" Slice a given 3D model
"""

import argparse
import pymesh.meshio as mio
import pymesh.meshutils as mu
from pymesh.slice_mesh import slice_mesh
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-N", type=int, required=True, help="number of slices")
    parser.add_argument(
        "--axis", nargs=3, type=float, default=[0.0, 0.0, 1.0], help="slicing direction"
    )
    parser.add_argument("input_mesh")
    parser.add_argument("output_slices")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    slices = slice_mesh(mesh, np.array(args.axis), args.N)

    slices = mu.merge_meshes(slices)
    mio.save_mesh(args.output_slices, slices, *slices.get_attribute_names())


if __name__ == "__main__":
    main()
