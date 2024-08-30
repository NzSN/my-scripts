import platform

from typing import Any, Protocol
from typing_extensions import Self

class BuildArgs:
    def __init__(self, args: Any) -> None:
        self.host_os = platform.system \
            if args.host_os == None else args.host_os
        self.target_os = platform.system \
            if args.target_os == None else args.target_os
        self.host_arch = platform.architecture \
            if args.host_arch == None else args.host_arch
        self.target_arch = platform.architecture \
            if args.target_arch == None else args.host_arch
        self.sysroot = args.sysroot
        self.builddir = "./build" if args.builddir == None else args.builddir
        self.dest = "./dist" if args.dest == None else args.dest
        self.version = args.version


class BuildProcess(Protocol):
    def setup(self, args: BuildArgs) -> Self:
        ...
    def build(self) -> Self:
        ...
