import subprocess
from collections import namedtuple
from typing import Optional
from base.utility import uncompress

Toolchain = namedtuple('Toolchain', ['arch', 'os', 'repo', 'strip'])

toolchains = [
    Toolchain('loong64',
              'linux',
              'http://ftp.loongnix.cn/toolchain/gcc/release/loongarch/gcc8/loongson-gnu-toolchain-8.3-x86_64-loongarch64-linux-gnu-rc1.5.tar.xz',
              'loongson-gnu-toolchain-8.3-x86_64-loongarch64-linux-gnu-rc1.5')
]

# Return the path of root of toolchain
def GetToolchain(arch: str, os: str, path: str, retry: int = 5) -> Optional[str]:
    retried = retry
    toolchain_root = ""
    for toolchain in toolchains:
        if toolchain.arch == arch and toolchain.os == os:
            filename = toolchain.repo.rsplit('/', 1)[-1]
            while True:
                try:
                    subprocess.run("wget " + toolchain.repo + " -O " + filename,
                                   shell=True, check=True, cwd=path)
                except subprocess.CalledProcessError as e:
                    retried += 1
                    if retried < 5:
                        continue
                    else:
                        break

                # Uncompress tarball
                toolchain_at_dir = uncompress(path + "/" + filename)
                if toolchain_at_dir is None:
                    return None
                toolchain_root = toolchain_at_dir + '/' + toolchain.strip
                break
    return toolchain_root
