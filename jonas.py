#!/bin/env python3
import argparse
import common
import os.path
import subprocess

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-i', '--image', dest='image',
                    type=str, required=True)

parser.add_argument('--entrypoint', dest='entrypoint', default=common.DEFAULT_VAL,
                    type=str, help="Image's entrypoint override")

[args, passthrough] = parser.parse_known_args()

def find_mounts(candidates):
    paths = []
    for c in candidates:
        prefix = find_existing_prefix(c)
        if prefix is not None:
            paths.append(prefix)
    return paths


def find_existing_prefix(path):
    while path not in ['', '/']:
        if(os.path.exists(path)):
            return os.path.abspath(path)
        path = os.path.dirname(path)
    return None


if __name__ == '__main__':
    if passthrough[0] != common.ARGS_SEP:
        raise ValueError("Bad arguments!")
    passthrough=passthrough[1:]

    mounts = find_mounts(passthrough)

    mounts_args = ['--workdir', os.getcwd()]
    for path in mounts:
        mounts_args += ['-v', path + ':' + path]

    entrypoint = ['--entrypoint', args.entrypoint] if args.entrypoint not in [common.DEFAULT_VAL, None] else []

    user_map = ['-u', str(os.getuid()) + ':' + str(os.getgid())]

    cmd = ['docker', 'run', '-i', '-t', '--rm'] + user_map + mounts_args + entrypoint + [args.image] + passthrough

    print(cmd)

    subprocess.run(cmd)
