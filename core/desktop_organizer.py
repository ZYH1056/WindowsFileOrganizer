import os
import shutil
from pathlib import Path
from typing import Dict, List


def organize_desktop() -> Dict[str, List[str]]:
    desktop = str(Path.home() / "Desktop")
    archive_dir = os.path.join(desktop, "桌面归档")
    os.makedirs(archive_dir, exist_ok=True)

    moved = []
    skipped = []

    try:
        for entry in os.scandir(desktop):
            if entry.path == archive_dir:
                continue
            if entry.is_symlink():
                skipped.append(entry.name)
                continue
            if entry.is_file() and entry.name.lower().endswith(".lnk"):
                skipped.append(entry.name)
                continue
            if entry.is_file() or entry.is_dir():
                dest = os.path.join(archive_dir, entry.name)
                if os.path.exists(dest):
                    base, ext = os.path.splitext(entry.name)
                    counter = 1
                    while os.path.exists(dest):
                        dest = os.path.join(archive_dir, f"{base}_{counter}{ext}")
                        counter += 1
                shutil.move(entry.path, dest)
                moved.append(entry.name)
    except PermissionError:
        skipped.append("权限不足，部分文件无法移动")

    return {"moved": moved, "skipped": skipped}
