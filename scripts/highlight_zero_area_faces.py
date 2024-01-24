#!/usr/bin/env python

"""
Highlight faces with zero area in floating point computation.
"""

import argparse
import numpy as np
import pymesh.meshio as mio


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_mesh", help="input mesh")
    parser.add_argument("output_mesh", help="output mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    mesh.add_attribute("face_area")
    areas = mesh.get_attribute("face_area")
    zero_faces = areas == 0.0

    roi = np.zeros(mesh.num_vertices)
    roi[mesh.faces[zero_faces]] = 1.0
    mesh.add_attribute("zero_faces")
    mesh.set_attribute("zero_faces", roi)

    mio.save_mesh(args.output_mesh, mesh, "zero_faces")


if __name__ == "__main__":
    main()
