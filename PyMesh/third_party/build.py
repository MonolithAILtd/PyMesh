#!/usr/bin/env python

""" Build and install third party dependencies for PyMesh.
"""

import argparse
import subprocess
import os
import os.path
import shutil
from pathlib import Path


def get_third_party_dependencies():
    return [
        "cgal",
        "cork",
        "eigen",
        "tetgen",
        "triangle",
        "qhull",
        "clipper",
        "draco",
        "tbb",
        "mmg",
        "json",
        "WindingNumber",
    ]


cwd = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--cleanup", action="store_true", help="Clean up the build folder after done."
    )
    parser.add_argument("package", choices=["all"] + get_third_party_dependencies())
    return parser.parse_args()


def build_generic(libname, build_flags="", cleanup=True):
    build_dir = cwd / "build" / libname

    if cleanup:
        shutil.rmtree(build_dir, ignore_errors=True)

    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    # Configure cgal
    cmd = (
        "cmake"
        + " {}".format(cwd / libname)
        + " -DBUILD_SHARED_LIBS=Off"
        + " -DCMAKE_POSITION_INDEPENDENT_CODE=On"
        + build_flags
        + " -DCMAKE_INSTALL_PREFIX={}/pymesh/third_party/".format(cwd.parent.parent)
    )
    # print(cmd)
    subprocess.check_call(cmd.split(), cwd=build_dir)

    # Build cgal
    cmd = "cmake --build {}".format(build_dir)
    subprocess.check_call(cmd.split())

    cmd = "cmake --build {} --target install".format(build_dir)
    subprocess.check_call(cmd.split())

    # Clean up
    if cleanup:
        shutil.rmtree(build_dir)


def build(package, cleanup):
    if package == "all":
        for libname in get_third_party_dependencies():
            build(libname, cleanup)
    elif package == "cgal":
        build_generic(
            "cgal", " -DWITH_CGAL_ImageIO=Off -DWITH_CGAL_Qt5=Off", cleanup=cleanup
        )
    elif package == "clipper":
        build_generic("Clipper/cpp", cleanup=cleanup)
    elif package == "tbb":
        build_generic(
            "tbb", " -DTBB_BUILD_SHARED=On -DTBB_BUILD_STATIC=Off", cleanup=cleanup
        )
    elif package == "json":
        build_generic("json", " -DJSON_BuildTests=Off", cleanup=cleanup)
    else:
        build_generic(package, cleanup=cleanup)


def main():
    args = parse_args()
    build(args.package, args.cleanup)


if __name__ == "__main__":
    main()
