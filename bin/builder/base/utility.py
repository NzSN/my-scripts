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
        ret = subprocess.run("clang --print-targets | grep " + expected_target ,
                             shell=True, check=True, capture_output=True)
        if not ret.stdout.decode().find(expected_target):
            return None
        else:
            return "clang"
    except subprocess.CalledProcessError as e:
        return None

def uncompress(tar_path: str) -> Optional[str]:
    dest_dir = '/'.join(tar_path.split('/')[0:-1])
    if tar_path.endswith('zip'):
        import zipfile
        with zipfile.ZipFile(tar_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    elif tar_path.endswith('tar.gz'):
        import tarfile
        with tarfile.open(tar_path, "r:gz") as tar_ref:
            tar_ref.extractall(dest_dir)
    elif tar_path.endswith('tar.xz'):
        import tarfile
        with tarfile.open(tar_path, "r:xz") as tar_ref:
            tar_ref.extractall(dest_dir)
    elif tar_path.endswith('tar'):
        import tarfile
        with tarfile.open(tar_path, "r:") as tar_ref:
            tar_ref.extractall(dest_dir)
    else:
        return None

    return dest_dir
