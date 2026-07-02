import zipfile
import os
from typing import List, Dict
from .file_scanner import FileInfo
from .classifier import Classifier


def pack_files_to_zip(files: List[str], output_path: str) -> bool:
    try:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                if os.path.isfile(f) and not os.path.islink(f):
                    arcname = os.path.basename(f)
                    zf.write(f, arcname)
        return True
    except Exception:
        return False


def pack_by_category(files: List[FileInfo], output_dir: str, classifier: Classifier) -> Dict[str, str]:
    results = {}
    cat_files = {}

    for f in files:
        if f.is_dir:
            continue
        cat = classifier.get_category(f.ext)
        cat_files.setdefault(cat, []).append(f.path)

    for cat, paths in cat_files.items():
        zip_path = os.path.join(output_dir, f"{cat}.zip")
        counter = 1
        while os.path.exists(zip_path):
            zip_path = os.path.join(output_dir, f"{cat}_{counter}.zip")
            counter += 1
        if pack_files_to_zip(paths, zip_path):
            results[cat] = zip_path

    return results
