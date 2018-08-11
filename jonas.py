#!/bin/env python3
import argparse
import common
import os.path
import sys
import subprocess

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('-i', '--image', dest='image',
                    type=str, required=True)

parser.add_argument('--entrypoint', dest='entrypoint', default=common.DEFAULT_VAL,
                    type=str, help="Image's entrypoint override")

[args, passthrough] = parser.parse_known_args()

def find_mounts(candidates):
    """
    Filter parameters looking for paths having a prefix describing existing directory.
    :param path: Initial path
    :return: longest prefix describing existing path or None
    """

    paths = []
    for c in candidates:
        prefix = find_existing_prefix(c)
        if prefix is not None:
            paths.append(prefix)
    return paths


def find_existing_prefix(path):
    """
    Searche given path and its parents until an existing directory other than root is found.
    :param path: Initial path
    :return: longest prefix describin existing path or None
    """
    while path not in ['', '/']:
        if(os.path.exists(path)):
            return os.path.abspath(path)
        path = os.path.dirname(path)
    return None


def get_uid_guid():
    return str(os.getuid()) + ':' + str(os.getgid())


if __name__ == '__main__':
    if passthrough[0] != common.ARGS_SEP:
        raise ValueError("Bad arguments!")
    passthrough=passthrough[1:]

    cmd = ['docker', 'run', '-i', '-t', '--rm']

    mounts = find_mounts(passthrough)
    if mounts:
        cmd = ['--workdir', os.getcwd()]
        for path in mounts:
            cmd += ['-v', path + ':' + path]

        cmd += ['-u', get_uid_guid()]

    if args.entrypoint not in [common.DEFAULT_VAL, None]:
        cmd += ['--entrypoint', args.entrypoint]

    print(cmd, file=sys.stderr)

    subprocess.run(cmd)
