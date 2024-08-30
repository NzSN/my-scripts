
from typing import Any
from typing_extensions import Self
from ..build_process import BuildProcess


class LLVMBuilder(BuildProcess):

  def setup(self, args: Any) -> Self:
      ...

  def build(self) -> Self:
      ...

  def finish(self) -> str:
      ...
