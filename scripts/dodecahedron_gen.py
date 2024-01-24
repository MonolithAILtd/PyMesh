#!/usr/bin/env python

"""
Generate dodecahedron
"""

import argparse

import pymesh.meshio as mio
import pymesh.meshutils as mu


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", "-r", type=float, default=1.0, help="sphere radius")
    parser.add_argument(
        "--center", "-c", type=float, nargs=3, default=[0, 0, 0], help="sphere center"
    )
    parser.add_argument("output_mesh", help="output mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mu.generate_dodecahedron(args.radius, center=args.center)
    mio.save_mesh(args.output_mesh, mesh)


if __name__ == "__main__":
    main()
