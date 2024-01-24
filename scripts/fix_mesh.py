#!/usr/bin/env python

"""
Remesh the input mesh to remove degeneracies and improve triangle quality.
"""

import argparse
import numpy as np
from numpy.linalg import norm

import pymesh.meshutils as mu
import pymesh.meshio as mio
import pymesh.outerhull as oh
import pymesh.selfintersection as si
from pymesh.timethis import timethis


def fix_mesh(mesh, detail="normal"):
    bbox_min, bbox_max = mesh.bbox
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 5e-3
    elif detail == "high":
        target_len = diag_len * 2.5e-3
    elif detail == "low":
        target_len = diag_len * 1e-2
    print("Target resolution: {} mm".format(target_len))

    count = 0
    mesh, __ = mu.remove_degenerated_triangles(mesh, 100)
    mesh, __ = mu.split_long_edges(mesh, target_len)
    num_vertices = mesh.num_vertices
    while True:
        mesh, __ = mu.collapse_short_edges(mesh, 1e-6)
        mesh, __ = mu.collapse_short_edges(mesh, target_len, preserve_feature=True)
        mesh, __ = mu.remove_obtuse_triangles(mesh, 150.0, 100)
        if mesh.num_vertices == num_vertices:
            break

        num_vertices = mesh.num_vertices
        print("#v: {}".format(num_vertices))
        count += 1
        if count > 10:
            break

    mesh = si.resolve_self_intersection(mesh)
    mesh, __ = mu.remove_duplicated_faces(mesh)
    mesh = oh.compute_outer_hull(mesh)
    mesh, __ = mu.remove_duplicated_faces(mesh)
    mesh, __ = mu.remove_obtuse_triangles(mesh, 179.0, 5)
    mesh, __ = mu.remove_isolated_vertices(mesh)

    return mesh


def old_fix_mesh(vertices, faces, detail="normal"):
    bbox_min = np.amin(vertices, axis=0)
    bbox_max = np.amax(vertices, axis=0)
    diag_len = norm(bbox_max - bbox_min)
    if detail == "normal":
        target_len = diag_len * 5e-3
    elif detail == "high":
        target_len = diag_len * 2.5e-3
    elif detail == "low":
        target_len = diag_len * 1e-2
    print("Target resolution: {} mm".format(target_len))

    count = 0
    vertices, faces = mu.split_long_edges(vertices, faces, target_len)
    num_vertices = len(vertices)
    while True:
        vertices, faces = mu.collapse_short_edges(vertices, faces, 1e-6)
        vertices, faces = mu.collapse_short_edges(
            vertices, faces, target_len, preserve_feature=True
        )
        vertices, faces = mu.remove_obtuse_triangles(vertices, faces, 150.0, 100)
        if num_vertices == len(vertices):
            break
        num_vertices = len(vertices)
        print("#v: {}".format(num_vertices))
        count += 1
        if count > 10:
            break

    vertices, faces = si.resolve_self_intersection(vertices, faces)
    vertices, faces = mu.remove_duplicated_faces(vertices, faces)
    vertices, faces, _ = oh.compute_outer_hull(vertices, faces, False)
    vertices, faces = mu.remove_duplicated_faces(vertices, faces)
    vertices, faces = mu.remove_obtuse_triangles(vertices, faces, 179.0, 5)
    vertices, faces, voxels = mu.remove_isolated_vertices(vertices, faces)
    return vertices, faces


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timing", help="print timing info", action="store_true")
    parser.add_argument(
        "--detail",
        help="level of detail to preserve",
        choices=["low", "normal", "high"],
        default="normal",
    )
    parser.add_argument("in_mesh", help="input mesh")
    parser.add_argument("out_mesh", help="output mesh")
    return parser.parse_args()


def main():
    args = parse_args()
    mesh = mio.load_mesh(args.in_mesh)

    mesh = fix_mesh(mesh, detail=args.detail)

    mio.save_mesh(args.out_mesh, mesh)

    if args.timing:
        timethis.summarize()


if __name__ == "__main__":
    main()
