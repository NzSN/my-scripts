import platform

from typing import Any, Protocol
from typing_extensions import Self

class BuildArgs:
    def __init__(self, args: Any) -> None:
        self.host_os = platform.system().lower() \
            if args.host_os == None else args.host_os
        self.target_os = platform.system().lower() \
            if args.target_os == None else args.target_os
        self.host_arch = platform.machine().lower() \
            if args.host_arch == None else args.host_arch
        self.target_arch = platform.machine().lower() \
            if args.target_arch == None else args.target_arch
        self.sysroot = args.sysroot
        self.builddir = "./build" if args.builddir == None else args.builddir
        self.dest = "./dist" if args.dest == None else args.dest
        self.version = args.version


class BuildProcess(Protocol):
    def setup(self, args: BuildArgs) -> Self:
        ...
    def build(self) -> Self:
        ...
    def finish(self) -> Any:
        ...
