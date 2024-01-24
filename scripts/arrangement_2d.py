#!/usr/bin/env python

"""
Compute 2D arrangement from 2D wire networks.
"""

import argparse
from pymesh import wires
from pymesh.arrangement2 import Arrangement2


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_wire_file", help="input wire file")
    parser.add_argument("output_wire_file", help="output wire file")
    return parser.parse_args()


def main():
    args = parse_args()
    wire_network = wires.WireNetwork.create_from_file(args.input_wire_file)
    arrangement = Arrangement2()
    arrangement.points = wire_network.vertices[:, 0:2]
    arrangement.segments = wire_network.edges
    arrangement.run()
    out_wire_network = arrangement.wire_network

    if out_wire_network.num_vertices != wire_network.num_vertices:
        print("Input wire network contains self-intersection!")
    out_wire_network.write_to_file(args.output_wire_file)


if __name__ == "__main__":
    main()
