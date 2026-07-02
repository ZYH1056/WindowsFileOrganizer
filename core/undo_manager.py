import shutil
import os
from datetime import datetime
from typing import List, Tuple


class UndoManager:
    def __init__(self, log_path: str = "operation_log.txt"):
        self.log_path = log_path
        self.last_operation = None
        self.backup_dir = os.path.join(os.getcwd(), ".undo_backup")
        os.makedirs(self.backup_dir, exist_ok=True)

    def record_move(self, moves: List[Tuple[str, str]]):
        self.last_operation = ("move", moves)
        self._write_log("移动", moves)

    def record_delete(self, files: List[str]):
        backed = []
        for f in files:
            try:
                dest = os.path.join(self.backup_dir, os.path.basename(f))
                counter = 1
                while os.path.exists(dest):
                    base, ext = os.path.splitext(os.path.basename(f))
                    dest = os.path.join(self.backup_dir, f"{base}_{counter}{ext}")
                    counter += 1
                shutil.copy2(f, dest)
                backed.append((f, dest))
            except OSError:
                continue
        self.last_operation = ("delete", backed)
        self._write_log("删除", [(f, "备份") for f in files])

    def record_rename(self, renames: List[Tuple[str, str]]):
        self.last_operation = ("rename", renames)
        self._write_log("重命名", renames)

    def undo(self) -> bool:
        if not self.last_operation:
            return False

        action, data = self.last_operation
        success = True

        if action == "move":
            for src, dest in reversed(data):
                try:
                    if os.path.exists(dest):
                        shutil.move(dest, src)
                except OSError:
                    success = False

        elif action == "delete":
            for orig, backup in reversed(data):
                try:
                    if os.path.exists(backup):
                        shutil.move(backup, orig)
                        os.remove(backup)
                except OSError:
                    success = False

        elif action == "rename":
            for old_path, new_path in reversed(data):
                try:
                    if os.path.exists(new_path):
                        os.rename(new_path, old_path)
                except OSError:
                    success = False

        self.last_operation = None
        return success

    def has_undo(self) -> bool:
        return self.last_operation is not None

    def _write_log(self, action: str, items: List[Tuple[str, str]]):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {action}:\n")
            for src, dest in items:
                f.write(f"  {src} -> {dest}\n")

    def clear_backup(self):
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir, ignore_errors=True)
