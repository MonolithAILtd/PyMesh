#!/usr/bin/env python

import argparse
import logging
import pymesh.meshio as mio
import pymesh.meshutils as mu


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--keep-symmetry",
        "-s",
        action="store_true",
        help="Whether to split quad symmetrically",
    )
    parser.add_argument("input_mesh", help="input quad mesh")
    parser.add_argument("output_mesh", help="output triangle mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    if mesh.vertex_per_face != 4:
        logging.warning("Input mesh is not quad mesh.")
        mio.save_mesh(args.output_mesh, mesh, *mesh.get_attribute_names())
    else:
        mesh = mu.quad_to_tri(mesh, args.keep_symmetry)
        mio.save_mesh(args.output_mesh, mesh, *mesh.get_attribute_names())


if __name__ == "__main__":
    main()
