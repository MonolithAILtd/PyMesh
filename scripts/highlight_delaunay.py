#!/usr/bin/env python

""" Highlight all tets that are not locally Delaunay.
"""

import argparse
import pymesh.meshio as mio
import pymesh.meshutils as mu
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("input_mesh")
    parser.add_argument("output_mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.input_mesh)
    delaunay = mu.is_delaunay(mesh)
    mesh.add_attribute("delaunay")
    mesh.set_attribute("delaunay", delaunay)

    strictly_delaunay = np.count_nonzero(delaunay > 0)
    cospherical = np.count_nonzero(delaunay == 0)
    not_delaunay = np.count_nonzero(delaunay < 0)

    print(
        "Strictly Delaunay: {:10} ({:>6.3%})".format(
            strictly_delaunay, float(strictly_delaunay) / mesh.num_voxels
        )
    )
    print(
        "      Cospherical: {:10} ({:>6.3%})".format(
            cospherical, float(cospherical) / mesh.num_voxels
        )
    )
    print(
        "     Not Delaunay: {:10} ({:>6.3%})".format(
            not_delaunay, float(not_delaunay) / mesh.num_voxels
        )
    )

    mio.save_mesh(args.output_mesh, mesh, "delaunay")


if __name__ == "__main__":
    main()
