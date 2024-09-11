
import os
import subprocess
import tempfile

from pathlib import Path
from typing import Any, Optional
from typing_extensions import Self

from base.utility import findClang, uncompress
from base.resources import Resource
from build_process import BuildArgs, BuildProcess



class LLVMBuilder(BuildProcess):

  llvm_src: Optional[str] = ""

  llvm_resources = [
    Resource('loong64', 'linux', '18.1.6-1',
             'http://ftp.loongnix.cn/toolchain/llvm/llvm18/llvm-project_18.1.6-1.src.tar.gz',
             'llvm-project-18.1.6-1')
  ]

  def setup(self, args: Any) -> Self:
    self.args = BuildArgs(args)
    return self

  def prepare(self) -> Self:
    selecteds = [r for r in self.llvm_resources
                 if r.arch == self.args.target_arch and
                 r.os   == self.args.target_os and
                 r.version == self.args.version]
    if len(selecteds) < 1:
      raise Exception("No matched resource found")
    elif len(selecteds) > 1:
      raise Exception("Multiple resources is matched, please report as a bug")

    build_path = Path(self.args.builddir)
    #build_path.mkdir(mode=0o755, exist_ok=True);
    self.build_path = build_path

    #subprocess.run("wget " + selecteds[0].repo,
    #               shell=True, check=True, cwd=str(build_path))
    #uncompress(str(build_path) + '/' + selecteds[0].repo.rsplit('/', 1)[-1])
    self.llvm_src = str(build_path.absolute()) + '/' + selecteds[0].strip

    return self

  def build(self) -> Self:
    print(str(self.llvm_src))

    assert(self.llvm_src is not None)
    clang_build_script = os.path.dirname(os.path.realpath(__file__)) + "/scripts/build_clang.sh"
    rt_build_script = os.path.dirname(os.path.realpath(__file__)) + "/scripts/build_rt.sh"
    subprocess.run([clang_build_script, self.llvm_src, self.args.dest, str(self.build_path.absolute())])

    tmpdir = tempfile.TemporaryDirectory()
    subprocess.run([rt_build_script, self.llvm_src, tmpdir.name])

    return self

  def finish(self) -> str:
      ...
