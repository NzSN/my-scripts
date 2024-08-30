import subprocess
from typing import Optional

def findClang(expected_target: str) -> Optional[str]:
    try:
        subprocess.run("which clang", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return None

    # Ok, clang is found then to check whether targets
    # are all supported
    try:
        subprocess.run("clang --print-targets | " + expected_target,
                       shell=True, check=True)
    except subprocess.CalledProcessError as e:
        return None
