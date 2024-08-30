import os
import subprocess
from pathlib import Path
from typing import Any, DefaultDict, Optional
from typing_extensions import Self
from build_process import BuildArgs, BuildProcess
from collections import namedtuple

from base.utility import findClang, uncompress
from base.toolchains import GetToolchain
from base.resources import Resource


rust_build_config_default = \
"""
# Use different pre-set defaults than the global defaults.
#
# See `src/bootstrap/defaults` for more information.
# Note that this has no default value (x.py uses the defaults in `config.example.toml`).

profile = 'dist'

[llvm]

[build]
target = [{target}]
profiler = true

# Arguments passed to the `./configure` script, used during distcheck. You
# probably won't fill this in but rather it's filled in by the `./configure`
# script. Useful for debugging.
configure-args = ['--set', '{dest}']

[install]

# Where to install the generated toolchain. Must be an absolute path.
prefix = '{dest}'
sysconfdir = '{dest}'
"""

class RustBuilder(BuildProcess):

    compiler: Optional[str] = None
    toolchain: Optional[str] = None
    rust_src: Optional[str] = None
    build_path: Optional[Path] = None
    custom_config: Optional[str] = None
    code_model: Optional[str] = None

    rust_resources = [
        Resource('loong64', 'linux', '1.80.0',
                 'http://ftp.loongnix.cn/toolchain/rust/rust-1.80/2024-07-29/abi1.0/rustc-1.80.0-src.tar.xz',
                 'rustc-1.80.0-src'),
        Resource('loong64', 'linux', '1.79.0', 'http://ftp.loongnix.cn/toolchain/rust/rust-1.79/2024-07-05/abi1.0/rustc-1.79.0-src.tar.xz',
                 'rustc-1.79.0-src')
    ]

    def set_codemodel(self, cmodel: str) -> Self:
        self.code_model = cmodel
        return self

    def set_config(self, config: str) -> Self:
        self.custom_config = config
        return self

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

        build_path = Path(self.args.builddir)
        build_path.mkdir(mode=0o755, exist_ok=True);
        self.build_path = build_path

        # Prepare toolchain to compile rust
        if self.args.target_arch != self.args.host_arch:
            # Cross compile is required. Need to find out an llvm
            # with target that match self.args.target_arch
            if self.args.target_arch == "loong64":
                # Community does not support abi-1.0 of loongarch64
                # have to use toolchain provided from LoongArch.
                self.toolchain = GetToolchain(
                    self.args.target_arch, self.args.target_os, str(build_path))
                assert(not (self.toolchain is None))

        # Get Rust source
        subprocess.run("wget " + selected.repo,
                      shell=True, check=True, cwd=str(build_path))
        uncompress(str(build_path) + '/' + selected.repo.rsplit('/', 1)[-1])

        self.rust_src = str(build_path) + '/' + selected.strip

        return self

    def build(self) -> Self:
        if self.rust_src == None:
            raise Exception("Need to prepare env to build rust")

        # Setup config.toml for rust building
        config = rust_build_config_default.format_map({
            'target': '"' + self.args.target_arch + "-unknown-" + self.args.target_os + "-gnu" + '"' + \
                      ',' + '"' + self.args.host_arch + "-unknown-" + self.args.host_os + "-gnu" + '"',
            'dest'  : self.args.dest
        })

        with open(self.rust_src + "/config.toml", "w") as file:
            file.write(config)

        # Cargo.lock of repo of loong64 are generated on loong64 machine
        if self.args.target_arch == "loong64" and self.args.host_arch != "loong64":
            subprocess.run("rm $(find . | grep Cargo.lock | xargs)",
                           shell=True, check=True, cwd=str(self.rust_src))
        subprocess.run("./x.py install", shell=True, check=True, cwd=str(self.rust_src))

        # In pratice, I find that use a code-model for different archs
        # may trigger problems so apply this env only for target arch.
        if not (self.code_model is None):
            build_env = os.environ.copy()
            build_env["RUSTFLAGS"] = f"-Ccode-model=" + self.code_model
            subprocess.run("./x.py install --keep-stage 0 --keep-stage 1",
                           shell=True, check=True, cwd=str(self.rust_src),
                           env=build_env)
        return self


    def finish(self) -> str:
        return self.args.dest
