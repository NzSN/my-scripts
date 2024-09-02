#!/usr/bin/python3

import os
import shutil
import subprocess
from pathlib import Path
from typing_extensions import Self
from typing import Any, Optional

from build_process import BuildProcess, BuildArgs


class NodeFFINapiBuilder(BuildProcess):

    module_path: Optional[Path] = None

    def setup(self, args: Any) -> Self:
        self.args = BuildArgs(args)
        return self

    def build(self) -> Self:
        build_path = Path("./build")
        build_path.mkdir(mode=0o755, exist_ok=True)

        node_ffi_napi_path = Path(str(build_path.absolute()) + "/node-ffi-napi")
        if not node_ffi_napi_path.exists():
            subprocess.run("git clone https://github.com/node-ffi-napi/node-ffi-napi.git",
                           shell=True,
                           check=True,
                           cwd=build_path.absolute())

        subprocess.run("npm install node-addon-api",
                       shell=True, check=True, cwd=node_ffi_napi_path.absolute())
        subprocess.run("npm install get-uv-event-loop-napi-h",
                       shell=True, check=True, cwd=node_ffi_napi_path.absolute())
        subprocess.run("npm install ref-napi",
                       shell=True, check=True, cwd=node_ffi_napi_path.absolute())

        # Setup cross toolchain
        env = os.environ.copy()

        # Build
        subprocess.run("node-gyp configure; node-gyp build",
                       shell=True, check=True, env=env,
                       cwd=node_ffi_napi_path.absolute())
        self.module_path = Path(str(node_ffi_napi_path.absolute()) + "/build/Release/ffi_bindings.node")
        return self

    def finish(self) -> Any:
        if self.module_path is None:
            raise Exception("Failed to compile")
        dest_path = Path(self.args.dest)
        dest_path.mkdir(mode=0o755, exist_ok=True)
        result_path = Path(str(dest_path.absolute()) + "/" + os.path.basename(self.module_path))
        shutil.copyfile(self.module_path.absolute(), result_path.absolute())
        os.chmod(result_path, os.stat(self.module_path.absolute()).st_mode)

        return str(result_path.absolute())
