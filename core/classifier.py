import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from .file_scanner import FileInfo


class Classifier:
    def __init__(self):
        self.rules_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "default_rules.json"
        )
        if not os.path.exists(self.rules_path):
            self.rules_path = os.path.join("data", "default_rules.json")

        with open(self.rules_path, "r", encoding="utf-8") as f:
            self.rules: Dict[str, List[str]] = json.load(f)

        self.reverse_map: Dict[str, str] = {}
        for category, exts in self.rules.items():
            for ext in exts:
                self.reverse_map[ext.lower()] = category

    def get_category(self, ext: str) -> str:
        return self.reverse_map.get(ext.lower(), "其他")

    def classify_files(self, files: List[FileInfo], target_dir: str) -> List[Tuple[str, str]]:
        moves = []
        for f in files:
            if f.is_dir:
                continue
            cat = self.get_category(f.ext)
            dest_dir = os.path.join(target_dir, cat)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, f.name)
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(f.name)
                dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                counter += 1
            shutil.move(f.path, dest_path)
            moves.append((f.path, dest_path))
        return moves

    def get_categories(self) -> List[str]:
        return list(self.rules.keys()) + ["其他"]

    def update_rules(self, new_rules: Dict[str, List[str]]):
        self.rules = new_rules
        self.reverse_map.clear()
        for category, exts in self.rules.items():
            for ext in exts:
                self.reverse_map[ext.lower()] = category
        with open(self.rules_path, "w", encoding="utf-8") as f:
            json.dump(self.rules, f, ensure_ascii=False, indent=2)
