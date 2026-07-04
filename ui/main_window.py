from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QStatusBar, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QFileDialog,
                             QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from core import (scan_directory, Classifier, find_duplicates, delete_files,
                  organize_desktop, UndoManager, pack_files_to_zip, pack_by_category)
from ui.widgets.directory_tree import DirectoryTree
from ui.widgets.file_list import FileList
from ui.widgets.operation_panel import OperationPanel
from ui.widgets.dialogs import (ConfirmDialog, RenameDialog, HelpDialog,
                                CustomRuleDialog)
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows 文件整理工具")
        self.setMinimumSize(900, 600)
        self.current_path = ""
        self.classifier = Classifier()
        self.undo_manager = UndoManager()
        self.selected_files = []
        self.is_dark_mode = False
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.dir_tree = DirectoryTree()
        main_layout.addWidget(self.dir_tree, 2)

        self.file_list = FileList()
        main_layout.addWidget(self.file_list, 5)

        self.operation_panel = OperationPanel()
        main_layout.addWidget(self.operation_panel, 3)

        self.status_bar = QStatusBar()
        self.log_label = QLabel("就绪")
        self.status_bar.addWidget(self.log_label)
        self.setStatusBar(self.status_bar)

        self.dir_tree.directory_selected.connect(self._on_directory_selected)
        self.file_list.files_selected.connect(self._on_files_selected)

        self.operation_panel.auto_classify.connect(self._on_auto_classify)
        self.operation_panel.find_duplicates.connect(self._on_find_duplicates)
        self.operation_panel.batch_rename.connect(self._on_batch_rename)
        self.operation_panel.organize_desktop.connect(self._on_organize_desktop)
        self.operation_panel.pack_zip.connect(self._on_pack_zip)
        self.operation_panel.undo.connect(self._on_undo)
        self.operation_panel.toggle_theme.connect(self._on_toggle_theme)
        self.operation_panel.show_help.connect(self._on_show_help)
        self.operation_panel.custom_rules.connect(self._on_custom_rules)

    def _on_directory_selected(self, path):
        self.current_path = path
        files = scan_directory(path)
        self.file_list.populate(files)
        self.log_label.setText(f"已扫描 {len(files)} 个项目 - {path}")

    def _on_files_selected(self, files):
        self.selected_files = files

    def _on_auto_classify(self):
        if not self.current_path:
            self.log_label.setText("请先选择目录")
            return

        dialog = ConfirmDialog("自动分类",
                              f"将当前目录中的文件按规则分类到子文件夹？\n\n目录: {self.current_path}",
                              self)
        if dialog.exec():
            files = scan_directory(self.current_path)
            moves = self.classifier.classify_files(files, self.current_path)
            self.undo_manager.record_move(moves)
            self.operation_panel.update_undo_state(True)
            self._on_directory_selected(self.current_path)
            self.log_label.setText(f"已分类 {len(moves)} 个文件")

    def _on_find_duplicates(self):
        if not self.current_path:
            self.log_label.setText("请先选择目录")
            return

        self.log_label.setText("正在扫描重复文件...")
        files = scan_directory(self.current_path)
        paths = [f.path for f in files if not f.is_dir]
        groups = find_duplicates(paths)

        if not groups:
            self.log_label.setText("未找到重复文件")
            return

        result_dialog = QMessageBox(self)
        result_dialog.setWindowTitle("重复文件检测结果")
        result_dialog.setText(f"发现 {len(groups)} 组重复文件")

        text = ""
        for i, group in enumerate(groups, 1):
            text += f"\n组 {i} ({group.size_str}):\n"
            for f in group.files:
                text += f"  {f}\n"

        result_dialog.setDetailedText(text)
        result_dialog.exec()

        delete_dialog = ConfirmDialog("删除重复文件",
                                     f"是否删除重复文件（保留每组第一个）？\n共 {len(groups)} 组",
                                     self)
        if delete_dialog.exec():
            to_delete = []
            for group in groups:
                to_delete.extend(group.files[1:])

            self.undo_manager.record_delete(to_delete)
            delete_files(to_delete)
            self.operation_panel.update_undo_state(True)
            self._on_directory_selected(self.current_path)
            self.log_label.setText(f"已删除 {len(to_delete)} 个重复文件")

    def _on_batch_rename(self):
        files = self.selected_files if self.selected_files else [f.path for f in scan_directory(self.current_path) if not f.is_dir]
        if not files:
            self.log_label.setText("没有可重命名的文件")
            return

        dialog = RenameDialog(files, self)
        if dialog.exec():
            if dialog.renamed_results:
                self.undo_manager.record_rename(dialog.renamed_results)
                self.operation_panel.update_undo_state(True)
                self._on_directory_selected(self.current_path)
                self.log_label.setText(f"已重命名 {len(dialog.renamed_results)} 个文件")

    def _on_organize_desktop(self):
        dialog = ConfirmDialog("一键规整桌面",
                              "将桌面所有文件移入「桌面归档」文件夹？\n快捷方式将被忽略。",
                              self)
        if dialog.exec():
            result = organize_desktop()
            self.log_label.setText(f"已移动 {len(result['moved'])} 个文件，跳过 {len(result['skipped'])} 个")

    def _on_pack_zip(self):
        files = self.selected_files if self.selected_files else [f.path for f in scan_directory(self.current_path) if not f.is_dir]
        if not files:
            self.log_label.setText("没有可打包的文件")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "保存 ZIP", "", "ZIP Files (*.zip)")
        if save_path:
            if pack_files_to_zip(files, save_path):
                self.log_label.setText(f"已打包到 {save_path}")
            else:
                self.log_label.setText("打包失败")

    def _on_undo(self):
        if self.undo_manager.undo():
            self.log_label.setText("已撤回上一次操作")
            if self.current_path:
                self._on_directory_selected(self.current_path)
        else:
            self.log_label.setText("没有可撤回的操作")
        self.operation_panel.update_undo_state(self.undo_manager.has_undo())

    def _on_toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #1e1e1e; color: #d4d4d4; }
                QPushButton { background-color: #3c3c3c; color: #d4d4d4; border: 1px solid #555; padding: 4px; }
                QPushButton:hover { background-color: #4c4c4c; }
                QTableWidget { background-color: #252526; color: #d4d4d4; gridline-color: #3c3c3c; }
                QHeaderView::section { background-color: #3c3c3c; color: #d4d4d4; }
                QTreeWidget { background-color: #252526; color: #d4d4d4; }
                QLineEdit { background-color: #3c3c3c; color: #d4d4d4; border: 1px solid #555; }
                QComboBox { background-color: #3c3c3c; color: #d4d4d4; border: 1px solid #555; }
                QListWidget { background-color: #252526; color: #d4d4d4; }
                QStatusBar { background-color: #252526; color: #d4d4d4; }
                QTextEdit { background-color: #252526; color: #d4d4d4; }
            """)
        else:
            self.setStyleSheet("")

    def _on_show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def _on_custom_rules(self):
        dialog = CustomRuleDialog(self.classifier, self)
        dialog.exec()
        self.log_label.setText("分类规则已更新")
