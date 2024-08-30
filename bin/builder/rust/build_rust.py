import subprocess
import pathlib
from typing import Any, Optional
from typing_extensions import Self
from build_process import BuildArgs, BuildProcess
from collections import namedtuple

from base.utility import findClang
from base.toolchains import GetToolchain

class RustBuilder(BuildProcess):

    compiler: Optional[str] = ""

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

        build_path = pathlib.Path(self.args.builddir)
        build_path.mkdir(mode=755, exist_ok=True);

        # Prepare toolchain to compile rust
        if self.args.target_arch != self.args.host_arch:
            # Cross compile is required. Need to find out an llvm
            # with target that match self.args.target_arch
            if self.args.target_arch == "loong64":
                # Community does not support abi-1.0 of loongarch64
                # have to use toolchain provided from LoongArch.
                toolchain_root = GetToolchain(
                    self.args.target_arch, self.args.target_os, str(build_path))
                assert(not (toolchain_root is None))

        # Get Rust source
        subprocess.run("wget " + selected.repo + " -O rust_src",
                       shell=True, check=True, cwd=str(build_path))

        return self

    def build(self) -> Self:

        return self


    def finish(self) -> str:
        ...
