#!/usr/bin/env python

"""
Compute the convex hull of a given mesh.
"""

import argparse
import pymesh.meshio as mio
from pymesh.convex_hull import convex_hull


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--engine", default="qhull", choices=["qhull", "cgal", "triangle", "tetgen"]
    )
    parser.add_argument("--with-timing", help="output timing info", action="store_true")
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh, drop_zero_dim=True)
    r = convex_hull(mesh, args.engine, args.with_timing)
    if args.with_timing:
        hull, running_time = r
        print("Running time: {}s".format(running_time))
    else:
        hull = r
    mio.save_mesh(args.output_mesh, hull, *hull.attribute_names)


if __name__ == "__main__":
    main()
