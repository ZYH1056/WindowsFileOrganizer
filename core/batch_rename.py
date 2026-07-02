import re
import os
from datetime import datetime
from typing import List, Tuple

WINDOWS_FORBIDDEN = r'[<>:"/\\|?*]'


def add_prefix(name: str, prefix: str) -> str:
    return prefix + name


def add_suffix(name: str, suffix: str) -> str:
    name_part, ext = os.path.splitext(name)
    return name_part + suffix + ext


def add_sequence(name: str, index: int, start: int = 1) -> str:
    name_part, ext = os.path.splitext(name)
    return f"{name_part}_{start + index}{ext}"


def add_date(name: str, fmt: str = "%Y%m%d") -> str:
    date_str = datetime.now().strftime(fmt)
    name_part, ext = os.path.splitext(name)
    return f"{name_part}_{date_str}{ext}"


def filter_forbidden_chars(name: str) -> str:
    return re.sub(WINDOWS_FORBIDDEN, "_", name)


def preview_rename(files: List[str], rule: str, **kwargs) -> List[Tuple[str, str, str]]:
    results = []
    for i, f in enumerate(files):
        original_name = os.path.basename(f)
        new_name = original_name

        if rule == "prefix":
            new_name = add_prefix(original_name, kwargs.get("prefix", ""))
        elif rule == "suffix":
            new_name = add_suffix(original_name, kwargs.get("suffix", ""))
        elif rule == "sequence":
            start = kwargs.get("start", 1)
            new_name = add_sequence(original_name, i, start)
        elif rule == "date":
            date_fmt = kwargs.get("date_fmt", "%Y%m%d")
            new_name = add_date(original_name, date_fmt)

        new_name = filter_forbidden_chars(new_name)
        new_path = os.path.join(os.path.dirname(f), new_name)
        results.append((f, original_name, new_name))

    return results


def apply_rename(files: List[str], rule: str, **kwargs) -> List[Tuple[str, str]]:
    results = []
    renamed = preview_rename(files, rule, **kwargs)
    for old_path, _, new_name in renamed:
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
                results.append((old_path, new_path))
            except OSError:
                pass
    return results
