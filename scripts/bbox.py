#!/usr/bin/env python

"""
Create bbox of a given mesh.
"""

import argparse
import pymesh.meshio as mio
import pymesh.meshutils as mu


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    bbox = mesh.bbox
    bbox_mesh = mu.generate_box_mesh(bbox[0], bbox[1], 1)
    mio.save_mesh(args.output_mesh, bbox_mesh)


if __name__ == "__main__":
    main()
