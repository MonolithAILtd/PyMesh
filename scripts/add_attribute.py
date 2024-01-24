#!/usr/bin/env python

"""
Add face index attribute to mesh.
"""

import argparse
import pymesh.meshio as mio
from pymesh.timethis import timethis


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attribute-name", "-n", help="Attribute name")
    parser.add_argument("input_mesh", help="input mesh")
    parser.add_argument("output_mesh", help="output mesh")
    return parser.parse_args()


@timethis
def add_attribute(mesh, name):
    mesh.add_attribute(name)


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    add_attribute(mesh, args.attribute_name)
    mio.save_mesh(args.output_mesh, mesh, args.attribute_name)
    timethis.summarize()


if __name__ == "__main__":
    main()
