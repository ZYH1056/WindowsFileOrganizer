# Windows 本地桌面文件整理工具实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个完整的 Windows 本地文件整理 GUI 工具（PyQt6 + Python），支持目录选择、自动分类、重复文件检测、批量重命名、桌面一键规整、操作撤回、日志记录、ZIP打包。

**Architecture:** 采用模块化架构，主窗口（MainWindow）作为容器，左侧目录树、中间文件列表、右侧操作面板、底部日志栏。各功能模块独立封装，通过信号槽通信。核心业务逻辑与 GUI 分离，便于维护。

**Tech Stack:** Python 3.10+ / PyQt6 / hashlib / shutil / zipfile / PyInstaller

---

## 文件结构

```
/workspace/
├── main.py                          # 程序入口
├── ui/
│   ├── __init__.py
│   ├── main_window.py               # 主窗口布局
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── directory_tree.py        # 左侧目录树组件
│   │   ├── file_list.py             # 中间文件列表组件
│   │   ├── operation_panel.py       # 右侧操作面板
│   │   ├── log_bar.py               # 底部日志栏
│   │   └── dialogs/                 # 弹窗
│   │       ├── __init__.py
│   │       ├── confirm_dialog.py    # 确认弹窗
│   │       ├── rename_dialog.py     # 重命名弹窗
│   │       ├── help_dialog.py       # 帮助说明弹窗
│   │       └── custom_rule_dialog.py# 自定义规则弹窗
├── core/
│   ├── __init__.py
│   ├── classifier.py                # 文件分类核心逻辑
│   ├── duplicate_finder.py          # 重复文件检测
│   ├── batch_rename.py               # 批量重命名
│   ├── desktop_organizer.py         # 桌面规整
│   ├── undo_manager.py               # 撤回管理器
│   ├── logger.py                     # 日志记录器
│   └── zipper.py                     # ZIP打包
├── data/
│   └── default_rules.json           # 默认分类规则
├── requirements.txt
├── build.spec                        # PyInstaller 打包配置
├── README.md
└── LICENSE
```

---

## 任务列表

### Task 1: 项目初始化与依赖

**Files:**
- Create: `/workspace/requirements.txt`
- Create: `/workspace/build.spec`

- [ ] **Step 1: 创建 requirements.txt**

```txt
PyQt6>=6.4.0
pyinstaller>=5.0
```

- [ ] **Step 2: 创建 PyInstaller build.spec**

```python
# build.spec
from PyInstaller.utils.hooks import collect_data
import PyInstaller.utils.hooks as utils

a = Analysis(
    ['main.py'],
    hiddenimports=[],
    datas=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='WindowsFileOrganizer',
    console=False,
    icon='icon.ico',
)
```

- [ ] **Step 3: Commit**

```bash
git add requirements.txt build.spec
git commit -m "chore: init project with PyQt6 deps and build spec"
```

---

### Task 2: 主窗口骨架

**Files:**
- Create: `/workspace/ui/__init__.py`
- Create: `/workspace/ui/main_window.py`
- Create: `/workspace/ui/widgets/__init__.py`
- Create: `/workspace/ui/widgets/log_bar.py`

- [ ] **Step 1: 创建主窗口类**

```python
# ui/main_window.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 文件整理工具")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._setup_theme()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # 左侧目录区（占 20%）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.dir_tree = QTreeWidget()
        self.btn_select_dir = QPushButton("选择目录")
        left_layout.addWidget(QLabel("目录"))
        left_layout.addWidget(self.dir_tree)
        left_layout.addWidget(self.btn_select_dir)

        # 中间文件预览区（占 50%）
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        self.file_list = QTableWidget()
        self.file_list.setColumnHeaders(["文件名", "大小", "类型", "修改时间"])
        center_layout.addWidget(QLabel("文件列表"))
        center_layout.addWidget(self.file_list)

        # 右侧操作按钮区（占 30%）
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.btn_auto_classify = QPushButton("自动分类")
        self.btn_find_duplicates = QPushButton("查找重复文件")
        self.btn_batch_rename = QPushButton("批量重命名")
        self.btn_organize_desktop = QPushButton("一键规整桌面")
        self.btn_pack_zip = QPushButton("打包ZIP")
        self.btn_help = QPushButton("使用说明")
        right_layout.addWidget(self.btn_auto_classify)
        right_layout.addWidget(self.btn_find_duplicates)
        right_layout.addWidget(self.btn_batch_rename)
        right_layout.addWidget(self.btn_organize_desktop)
        right_layout.addWidget(self.btn_pack_zip)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_help)

        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(center_panel, 5)
        main_layout.addWidget(right_panel, 3)

        # 底部日志栏
        self.log_bar = QLabel("就绪")
        self.log_bar.setStyleSheet("background: #f0f0f0; padding: 4px;")
        status_bar = QLabel()
        status_bar.addWidget(self.log_bar)
        self.setStatusBar(status_bar)

    def _setup_theme(self):
        # 默认浅色模式，可通过菜单切换
        self.setStyleSheet("")
```

- [ ] **Step 2: 创建入口文件**

```python
# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

- [ ] **Step 3: Commit**

```bash
git add main.py ui/
git commit -m "feat: main window skeleton with 3-panel layout"
```

---

### Task 3: 目录选择与文件扫描

**Files:**
- Modify: `/workspace/ui/main_window.py`
- Create: `/workspace/core/__init__.py`
- Create: `/workspace/core/file_scanner.py`

- [ ] **Step 1: 创建文件扫描模块**

```python
# core/file_scanner.py
import os
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

def scan_directory(path: str) -> List[FileInfo]:
    files = []
    for entry in os.scandir(path):
        if entry.is_file() and not entry.is_symlink():
            stat = entry.stat()
            files.append(FileInfo(
                path=entry.path,
                name=entry.name,
                size=stat.st_size,
                ext=Path(entry.name).suffix.lower(),
                modified=str(stat.st_mtime)
            ))
    return files
```

- [ ] **Step 2: 修改主窗口连接目录选择信号**

```python
# 在 MainWindow._setup_ui 中添加
self.btn_select_dir.clicked.connect(self._on_select_dir)

def _on_select_dir(self):
    path = QFileDialog.getExistingDirectory(self, "选择目录")
    if path:
        self.current_path = path
        files = scan_directory(path)
        self._populate_file_list(files)
```

- [ ] **Step 3: Commit**

```bash
git add core/file_scanner.py ui/main_window.py
git commit -m "feat: directory selection and file scanning"
```

---

### Task 4: 自动分类功能

**Files:**
- Create: `/workspace/data/default_rules.json`
- Create: `/workspace/core/classifier.py`
- Create: `/workspace/ui/widgets/dialogs/__init__.py`
- Create: `/workspace/ui/widgets/dialogs/confirm_dialog.py`
- Create: `/workspace/ui/widgets/dialogs/custom_rule_dialog.py`

- [ ] **Step 1: 创建默认分类规则 JSON**

```json
{
  "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
  "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
  "文档": [".doc", ".docx", ".pdf", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
  "安装包": [".exe", ".msi"],
  "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
  "脚本": [".py", ".js", ".sh", ".bat", ".cmd", ".ps1"]
}
```

- [ ] **Step 2: 创建分类器核心逻辑**

```python
# core/classifier.py
import json
import shutil
import os
from pathlib import Path
from typing import Dict, List

class Classifier:
    def __init__(self, rules_path: str = "data/default_rules.json"):
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules: Dict[str, List[str]] = json.load(f)
        self.reverse_map: Dict[str, str] = {}
        for category, exts in self.rules.items():
            for ext in exts:
                self.reverse_map[ext] = category

    def get_category(self, ext: str) -> str:
        return self.reverse_map.get(ext.lower(), "其他")

    def classify_files(self, files: List, target_dir: str) -> Dict[str, List[str]]:
        moved = {cat: [] for cat in self.rules.keys()}
        moved["其他"] = []
        for f in files:
            cat = self.get_category(f.ext)
            dest_dir = os.path.join(target_dir, cat)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, f.name)
            shutil.move(f.path, dest_path)
            moved[cat].append(dest_path)
        return moved
```

- [ ] **Step 3: 创建确认弹窗和自定义规则弹窗**

```python
# ui/widgets/dialogs/confirm_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

class ConfirmDialog(QDialog):
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(message))
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("确认")
        self.btn_cancel = QPushButton("取消")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
```

- [ ] **Step 4: 连接主窗口分类按钮信号**

```python
# 在 MainWindow._setup_ui 中
self.btn_auto_classify.clicked.connect(self._on_auto_classify)

def _on_auto_classify(self):
    dialog = ConfirmDialog("自动分类", "将文件按规则分类到子文件夹？", self)
    if dialog.exec():
        # 执行分类
        pass
```

- [ ] **Step 5: Commit**

```bash
git add data/default_rules.json core/classifier.py ui/widgets/dialogs/
git commit -m "feat: auto-classify files by extension rules"
```

---

### Task 5: 重复文件检测

**Files:**
- Create: `/workspace/core/duplicate_finder.py`

- [ ] **Step 1: 创建哈希比对核心逻辑**

```python
# core/duplicate_finder.py
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

def compute_file_hash(path: str) -> str:
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def find_duplicates(paths: List[str]) -> List[DuplicateGroup]:
    size_map = defaultdict(list)
    for p in paths:
        try:
            size_map[os.path.getsize(p)].append(p)
        except OSError:
            continue

    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) < 2:
            continue
        for f in files:
            h = compute_file_hash(f)
            hash_map[h].append(f)

    results = []
    for h, files in hash_map.items():
        if len(files) > 1:
            results.append(DuplicateGroup(
                hash_value=h,
                files=files,
                size=os.path.getsize(files[0])
            ))
    return results
```

- [ ] **Step 2: 在主窗口添加重复文件展示逻辑**

```python
# MainWindow 中新增方法
def _on_find_duplicates(self):
    if not hasattr(self, 'current_path'):
        return
    files = scan_directory(self.current_path)
    paths = [f.path for f in files]
    groups = find_duplicates(paths)
    self._show_duplicate_results(groups)
```

- [ ] **Step 3: Commit**

```bash
git add core/duplicate_finder.py
git commit -m "feat: duplicate file detection via SHA-256 hash"
```

---

### Task 6: 批量重命名面板

**Files:**
- Create: `/workspace/core/batch_rename.py`
- Create: `/workspace/ui/widgets/dialogs/rename_dialog.py`

- [ ] **Step 1: 创建批量重命名核心逻辑**

```python
# core/batch_rename.py
import re
import os
from datetime import datetime
from typing import List

WINDOWS_FORBIDDEN = r'[<>:"/\\|?*]'

def add_prefix(name: str, prefix: str) -> str:
    return prefix + name

def add_suffix(name: str, suffix: str) -> str:
    name, ext = os.path.splitext(name)
    return name + suffix + ext

def add_sequence(name: str, start: int, step: int) -> str:
    name, ext = os.path.splitext(name)
    return f"{name}_{start}{ext}"

def add_date(name: str, fmt: str = "%Y%m%d") -> str:
    date_str = datetime.now().strftime(fmt)
    name, ext = os.path.splitext(name)
    return f"{name}_{date_str}{ext}"

def filter_forbidden_chars(name: str) -> str:
    return re.sub(WINDOWS_FORBIDDEN, "_", name)

def preview_rename(files: List[str], rule: str, **kwargs) -> List[tuple]:
    results = []
    for i, f in enumerate(files):
        original = os.path.basename(f)
        name = original
        if rule == "prefix":
            name = add_prefix(original, kwargs.get("prefix", ""))
        elif rule == "suffix":
            name = add_suffix(original, kwargs.get("suffix", ""))
        elif rule == "sequence":
            start = kwargs.get("start", 1)
            step = kwargs.get("step", 1)
            name = add_sequence(original, start + i * step, step)
        elif rule == "date":
            name = add_date(original, kwargs.get("date_fmt", "%Y%m%d"))
        name = filter_forbidden_chars(name)
        results.append((original, name))
    return results
```

- [ ] **Step 2: 创建重命名弹窗**

```python
# ui/widgets/dialogs/rename_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QTableWidget)
from PyQt6.QtCore import Qt

class RenameDialog(QDialog):
    def __init__(self, files: list, parent=None):
        super().__init__(parent)
        self.files = files
        self.setWindowTitle("批量重命名")
        self.setMinimumSize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        rule_layout = QHBoxLayout()
        rule_layout.addWidget(QLabel("规则:"))
        self.rule_combo = QComboBox()
        self.rule_combo.addItems(["前缀", "后缀", "数字序列", "日期"])
        rule_layout.addWidget(self.rule_combo)
        self.param_input = QLineEdit()
        rule_layout.addWidget(self.param_input)
        self.btn_preview = QPushButton("预览")
        rule_layout.addWidget(self.btn_preview)
        layout.addLayout(rule_layout)

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        layout.addWidget(self.preview_table)

        btns = QHBoxLayout()
        self.btn_apply = QPushButton("应用")
        self.btn_cancel = QPushButton("取消")
        btns.addWidget(self.btn_apply)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.btn_preview.clicked.connect(self._on_preview)
        self.btn_apply.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
```

- [ ] **Step 3: Commit**

```bash
git add core/batch_rename.py ui/widgets/dialogs/rename_dialog.py
git commit -m "feat: batch rename with preview"
```

---

### Task 7: 桌面一键规整

**Files:**
- Create: `/workspace/core/desktop_organizer.py`
- Modify: `/workspace/ui/main_window.py`

- [ ] **Step 1: 创建桌面规整核心逻辑**

```python
# core/desktop_organizer.py
import os
import shutil
from pathlib import Path

def organize_desktop() -> dict:
    desktop = str(Path.home() / "Desktop")
    archive_dir = os.path.join(desktop, "桌面归档")
    os.makedirs(archive_dir, exist_ok=True)

    moved = []
    skipped = []
    for entry in os.scandir(desktop):
        if entry.is_symlink():
            skipped.append(entry.name)
            continue
        if entry.is_file() and entry.name.endswith(".lnk"):
            skipped.append(entry.name)
            continue
        if entry.is_file() or entry.is_dir():
            dest = os.path.join(archive_dir, entry.name)
            if os.path.exists(dest):
                base, ext = os.path.splitext(entry.name)
                dest = os.path.join(archive_dir, f"{base}_{len([f for f in os.listdir(archive_dir)])}{ext}")
            shutil.move(entry.path, dest)
            moved.append(entry.name)
    return {"moved": moved, "skipped": skipped}
```

- [ ] **Step 2: 连接主窗口按钮**

```python
self.btn_organize_desktop.clicked.connect(self._on_organize_desktop)

def _on_organize_desktop(self):
    dialog = ConfirmDialog("一键规整", "将桌面所有文件移入「桌面归档」文件夹？\n快捷方式将被忽略。", self)
    if dialog.exec():
        result = organize_desktop()
        self.log_bar.setText(f"已移动 {len(result['moved'])} 个文件，跳过 {len(result['skipped'])} 个")
```

- [ ] **Step 3: Commit**

```bash
git add core/desktop_organizer.py ui/main_window.py
git commit -m "feat: one-click desktop organization"
```

---

### Task 8: 操作撤回与日志

**Files:**
- Create: `/workspace/core/undo_manager.py`
- Create: `/workspace/core/logger.py`

- [ ] **Step 1: 创建撤回管理器（单次操作缓存）**

```python
# core/undo_manager.py
import shutil
import json
import os
from datetime import datetime
from typing import List, Tuple

class UndoManager:
    def __init__(self, log_path: str = "operation_log.txt"):
        self.log_path = log_path
        self.last_operation = None  # (action_type, [(src, dest), ...])

    def record_move(self, moves: List[Tuple[str, str]]):
        self.last_operation = ("move", moves)
        self._write_log("移动", moves)

    def record_delete(self, files: List[str]):
        # 备份到临时目录
        backup_dir = os.path.join(os.getcwd(), ".undo_backup")
        os.makedirs(backup_dir, exist_ok=True)
        backed = []
        for f in files:
            dest = os.path.join(backup_dir, os.path.basename(f))
            shutil.copy2(f, dest)
            backed.append((f, dest))
        self.last_operation = ("delete", backed)
        self._write_log("删除", [(f, "备份") for f in files])

    def undo(self) -> bool:
        if not self.last_operation:
            return False
        action, data = self.last_operation
        if action == "move":
            for src, dest in reversed(data):
                shutil.move(dest, src)
        elif action == "delete":
            for orig, backup in reversed(data):
                shutil.move(backup, orig)
        self.last_operation = None
        return True

    def _write_log(self, action: str, items: List[Tuple[str, str]]):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {action}:\n")
            for src, dest in items:
                f.write(f"  {src} -> {dest}\n")
```

- [ ] **Step 2: 在主窗口添加工具栏按钮**

```python
# 在 MainWindow._setup_ui 右侧面板添加
self.btn_undo = QPushButton("撤回上一次")
self.btn_undo.clicked.connect(self._on_undo)

def _on_undo(self):
    if self.undo_manager.undo():
        self.log_bar.setText("已撤回上一次操作")
```

- [ ] **Step 3: Commit**

```bash
git add core/undo_manager.py core/logger.py
git commit -m "feat: undo manager and operation logging"
```

---

### Task 9: ZIP 打包归档

**Files:**
- Create: `/workspace/core/zipper.py`

- [ ] **Step 1: 创建 ZIP 打包逻辑**

```python
# core/zipper.py
import zipfile
import os
from typing import List

def pack_files_to_zip(files: List[str], output_path: str) -> bool:
    try:
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                arcname = os.path.basename(f)
                zf.write(f, arcname)
        return True
    except Exception as e:
        return False

def pack_by_category(files: List, output_dir: str, classifier) -> dict:
    results = {}
    cat_files = {}
    for f in files:
        cat = classifier.get_category(f.ext)
        cat_files.setdefault(cat, []).append(f.path)

    for cat, paths in cat_files.items():
        zip_path = os.path.join(output_dir, f"{cat}.zip")
        if pack_files_to_zip(paths, zip_path):
            results[cat] = zip_path
    return results
```

- [ ] **Step 2: 在主窗口连接打包按钮**

```python
self.btn_pack_zip.clicked.connect(self._on_pack_zip)

def _on_pack_zip(self):
    save_path, _ = QFileDialog.getSaveFileName(self, "保存ZIP", "", "ZIP Files (*.zip)")
    if save_path:
        # 执行打包
        pass
```

- [ ] **Step 3: Commit**

```bash
git add core/zipper.py
git commit -m "feat: ZIP archive packaging by category"
```

---

### Task 10: 浅色/深色模式切换与帮助弹窗

**Files:**
- Modify: `/workspace/ui/main_window.py`
- Create: `/workspace/ui/widgets/dialogs/help_dialog.py`

- [ ] **Step 1: 创建帮助弹窗**

```python
# ui/widgets/dialogs/help_dialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QTextEdit

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("使用说明")
        self.setMinimumSize(500, 400)
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        content = QTextEdit()
        content.setReadOnly(True)
        content.setHtml("""
        <h2>Windows 文件整理工具</h2>
        <h3>目录选择</h3>
        <p>点击左侧「选择目录」按钮，选择要整理的文件夹。</p>
        <h3>自动分类</h3>
        <p>根据文件后缀自动分拣到对应分类文件夹。</p>
        <h3>查找重复文件</h3>
        <p>通过 SHA-256 哈希比对查找重复文件。</p>
        <h3>批量重命名</h3>
        <p>支持添加前缀、后缀、数字序列、日期命名。</p>
        <h3>一键规整桌面</h3>
        <p>将桌面所有文件移入「桌面归档」文件夹。</p>
        <h3>撤回操作</h3>
        <p>可撤回最近一次文件移动/删除操作。</p>
        """)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        btn = QPushButton("关闭")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
```

- [ ] **Step 2: 添加深色模式支持**

```python
# 在 MainWindow._setup_theme 中添加
self.is_dark_mode = False

def toggle_theme(self):
    self.is_dark_mode = not self.is_dark_mode
    if self.is_dark_mode:
        self.setStyleSheet("""
            QWidget { background: #1e1e1e; color: #d4d4d4; }
            QPushButton { background: #333; color: #d4d4d4; border: 1px solid #555; padding: 4px; }
            QTableWidget { background: #252526; color: #d4d4d4; }
        """)
    else:
        self.setStyleSheet("")
```

- [ ] **Step 3: Commit**

```bash
git add ui/widgets/dialogs/help_dialog.py
git commit -m "feat: help dialog and dark mode toggle"
```

---

### Task 11: PyInstaller 打包脚本与 README

**Files:**
- Create: `/workspace/build.bat`
- Modify: `/workspace/README.md`

- [ ] **Step 1: 创建打包脚本**

```bat
@echo off
pip install -r requirements.txt
pyinstaller build.spec
echo 打包完成！exe位于 dist 目录
pause
```

- [ ] **Step 2: 更新 README**

```markdown
# Windows 文件整理工具

一款运行在 Windows 本地的图形化文件整理工具，完全离线，保护隐私。

## 功能

- 目录选择与文件扫描
- 自动分类（图片/视频/文档/安装包/压缩包/脚本）
- 自定义分类规则
- 重复文件检测（SHA-256 哈希）
- 批量重命名（支持前缀/后缀/序列/日期）
- 桌面一键规整
- 操作撤回
- ZIP 打包归档
- 浅色/深色模式

## 安装

双击运行 `dist/WindowsFileOrganizer.exe` 即可。

## 打包

```bat
build.bat
```

## MIT License
```

- [ ] **Step 3: Commit**

```bash
git add build.bat README.md
git commit -m "docs: add build script and README"
```

---

### Task 12: 最终检查与打包测试

**Files:**
- Review: 所有源文件

- [ ] **Step 1: 运行 build.bat 验证打包成功**

```bat
build.bat
```

- [ ] **Step 2: 验证 dist 目录生成 exe**

- [ ] **Step 3: 最终 Commit**

```bash
git add -A
git commit -m "v1.0.0: 完成所有功能模块"
```

---

## 计划自检

| 需求 | 对应任务 |
|------|---------|
| 目录选择模块 | Task 3 |
| 自动分类功能 | Task 4 |
| 重复文件检测 | Task 5 |
| 批量重命名 | Task 6 |
| 桌面一键规整 | Task 7 |
| 操作撤回与日志 | Task 8 |
| ZIP打包归档 | Task 9 |
| 浅色/深色模式 | Task 10 |
| 帮助说明弹窗 | Task 10 |
| 一键打包exe脚本 | Task 11 |
| README文档 | Task 11 |

所有需求均已覆盖，无遗漏。
