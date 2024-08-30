
from typing import Any
from typing_extensions import Self

from base.resources import Resource
from ..build_process import BuildArgs, BuildProcess



class LLVMBuilder(BuildProcess):

  llvm_resources = [
    Resource('loong64', 'linux', '18.1.6-1',
             'http://ftp.loongnix.cn/toolchain/llvm/llvm18/llvm-project_18.1.6-1.src.tar.gz',
             'llvm-project_18.1.6-1.src')
  ]

  def setup(self, args: Any) -> Self:
    self.args = BuildArgs(args)
    return self

  def build(self) -> Self:


  def finish(self) -> str:
      ...
