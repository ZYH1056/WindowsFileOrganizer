import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class FileInfo:
    path: str
    name: str
    size: int
    ext: str
    modified: str
    is_dir: bool = False

    @property
    def size_str(self):
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.2f} MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.2f} GB"


def scan_directory(path: str) -> List[FileInfo]:
    files = []
    if not os.path.isdir(path):
        return files
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_symlink():
                    continue
                if entry.is_dir():
                    files.append(FileInfo(
                        path=entry.path,
                        name=entry.name,
                        size=0,
                        ext="",
                        modified="",
                        is_dir=True
                    ))
                elif entry.is_file():
                    stat = entry.stat()
                    files.append(FileInfo(
                        path=entry.path,
                        name=entry.name,
                        size=stat.st_size,
                        ext=Path(entry.name).suffix.lower(),
                        modified=str(stat.st_mtime)
                    ))
            except OSError:
                continue
    except PermissionError:
        pass
    return sorted(files, key=lambda x: (not x.is_dir, x.name.lower()))


def get_desktop_path() -> str:
    return str(Path.home() / "Desktop")


def get_downloads_path() -> str:
    return str(Path.home() / "Downloads")
