import subprocess
from collections import namedtuple
from typing import Optional
from ..base.utility import uncompress

Toolchain = namedtuple('Toolchain', ['arch', 'os', 'repo'])

toolchains = [
    Toolchain('loong64', 'linux', 'http://ftp.loongnix.cn/toolchain/gcc/release/loongarch/gcc8/loongson-gnu-toolchain-8.3-x86_64-loongarch64-linux-gnu-rc1.5.tar.xz')
]

# Return the path of root of toolchain
def GetToolchain(arch: str, os: str, path: str, retry: int = 5) -> Optional[str]:
    retried = retry
    for toolchain in toolchains:
        if toolchain.arch is arch and toolchain.os is os:
            filename = toolchain.repo.rsplit('/', 1)[-1]
            while True:
                try:
                    subprocess.run("wget " + toolchain.repo + " -O " + filename,
                                   shell=True, check=True, cwd=path)
                    # Uncompress tarball
                    toolchain_root = uncompress(path + "/" + filename)
                    if toolchain_root is None:
                        return None
                except subprocess.CalledProcessError as e:
                    retried += 1
                    if retried < 5:
                        continue
                    else:
                        break

                break
