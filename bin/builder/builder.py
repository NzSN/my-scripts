#!/usr/bin/python3

import argparse


parser = argparse.ArgumentParser(
    prog = "builder.py",
    description = "A system that used to build softwares from sources")

parser.add_argument('project', type=str)
parser.add_argument('--host_os', required=False)
parser.add_argument('--target_os', required=False)
parser.add_argument('--host_arch', required=False)
parser.add_argument('--target_arch', required=False)
parser.add_argument('--sysroot', required=False)
parser.add_argument('--builddir', required=False)
parser.add_argument('--dest', required=False)
parser.add_argument('--version', required=False)
args = parser.parse_args()

if args.project == 'rust':
    from rust.build_rust import RustBuilder
    RustBuilder()    \
        .setup(args) \
        .prepare()   \
        .build()
elif args.project == 'node-ffi-napi':
    from node.build_node_ffi_napi import NodeFFINapiBuilder
    NodeFFINapiBuilder() \
        .setup(args)     \
        .build()         \
        .finish()
