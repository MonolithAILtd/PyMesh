#!/usr/bin/env python

"""
Compute the outer hull of the input mesh.
"""

import argparse
import pymesh.meshio as mio
from pymesh.outerhull import compute_outer_hull
import os.path


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=["auto", "igl"], default="auto")
    parser.add_argument(
        "--recursive",
        "-R",
        help="Recursively peel all outer hull layers",
        default=None,
        action="store_true",
    )
    parser.add_argument("input_mesh", help="input mesh")
    parser.add_argument("output_mesh", help="output mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)

    result = compute_outer_hull(mesh, engine=args.engine, all_layers=args.recursive)

    if args.recursive:
        basename, ext = os.path.splitext(args.output_mesh)
        for i, outer_hull in enumerate(result):
            out_name = "{}_{}{}".format(basename, i, ext)
            mio.save_mesh(out_name, outer_hull, *outer_hull.get_attribute_names())
    else:
        mio.save_mesh(args.output_mesh, result, *result.get_attribute_names())


if __name__ == "__main__":
    main()
