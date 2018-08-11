#!/bin/env python3

"""
Generates wrapper for given command.
"""

import argparse
import common

JONAS_BIN = 'jonas'

parser = argparse.ArgumentParser()

parser.add_argument('name')

parser.add_argument('-i', '--image', dest='image',
                    type=str, required=True)

parser.add_argument('--entrypoint', dest='entrypoint', default=common.DEFAULT_VAL,
                    type=str, help="Image's entrypoint override")

args = parser.parse_args()


def generate_sh():
    return \
"""#!/bin/bash

{JONAS_BIN} -i {IMAGE} --entrypoint {ENTRYPOINT} {SEP} \"$@\"""" \
        .format(JONAS_BIN=JONAS_BIN, IMAGE=args.image, ENTRYPOINT=args.entrypoint, SEP=common.ARGS_SEP)


if __name__ == '__main__':
    sh = generate_sh()
    print(sh)
