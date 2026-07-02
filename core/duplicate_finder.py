import hashlib
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DuplicateGroup:
    hash_value: str
    files: List[str]
    size: int

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


def compute_file_hash(path: str) -> str:
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, IOError):
        return ""


def find_duplicates(paths: List[str]) -> List[DuplicateGroup]:
    size_map = defaultdict(list)
    for p in paths:
        try:
            if os.path.isfile(p) and not os.path.islink(p):
                size_map[os.path.getsize(p)].append(p)
        except OSError:
            continue

    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) < 2:
            continue
        for f in files:
            h = compute_file_hash(f)
            if h:
                hash_map[h].append(f)

    results = []
    for h, files in hash_map.items():
        if len(files) > 1:
            try:
                size = os.path.getsize(files[0])
            except OSError:
                size = 0
            results.append(DuplicateGroup(
                hash_value=h,
                files=files,
                size=size
            ))
    return sorted(results, key=lambda x: x.size, reverse=True)


def delete_files(files: List[str]) -> bool:
    for f in files:
        try:
            os.remove(f)
        except OSError:
            return False
    return True
