import shutil
from pathlib import Path


def copy(src, dst):
    p_src = Path(src)
    p_dst = Path(dst)
    if not p_src.exists():
        raise FileNotFoundError(p_src.as_posix())
    p_dst.parent.mkdir(parents=True, exist_ok=True)
    if p_src.is_file():
        shutil.copy(src, dst)
    else:
        shutil.copytree(src, dst, dirs_exist_ok=True)

