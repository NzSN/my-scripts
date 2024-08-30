import subprocess
import pathlib
from typing import Any
from typing_extensions import Self
from build_process import BuildArgs, BuildProcess
from collections import namedtuple

class RustBuilder(BuildProcess):

    Resource = namedtuple('Resource', ['arch', 'os', 'version', 'repo'])

    rust_resources = [
        Resource('loong64', 'linux', '1.80', 'http://ftp.loongnix.cn/toolchain/rust/rust-1.80/2024-07-29/abi1.0/rustc-1.80.0-src.tar.xz'),
        Resource('loong64', 'linux', '1.79', 'http://ftp.loongnix.cn/toolchain/rust/rust-1.79/2024-07-05/abi1.0/rustc-1.79.0-src.tar.xz')
    ]

    def setup(self, args: Any) -> Self:
        self.args = BuildArgs(args)
        return self

    def prepare(self) -> Self:
        # Check existence of resources
        selecteds = [r for r in self.rust_resources
                    if r.arch == self.args.target_arch and
                       r.os   == self.args.target_os and
                       r.version == self.args.version]
        if len(selecteds) < 1:
            raise Exception("No matched rust resource found")
        elif len(selecteds) > 1:
            raise Exception("Multiple resources is matched, please report as a bug")

        selected = selecteds[0]

        buildPath = pathlib.Path(self.args.builddir)
        buildPath.mkdir(mode=755, exist_ok=True);

        # Prepare toolchain to compile rust
        if self.args.target_arch != self.args.host_arch:
            # Cross compile is required. Need to find out an llvm
            # with target that match self.args.target_arch


        subprocess.run("wget " + selected.repo + " -O rust_src",
                       shell=True, check=True, cwd=str(buildPath))

        return self

    def build(self) -> Self:

        return self
