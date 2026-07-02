from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, pyqtSignal
from core.file_scanner import FileInfo
from datetime import datetime


class FileList(QWidget):
    file_double_clicked = pyqtSignal(str)
    files_selected = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_files = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        title_label = QLabel("文件列表")
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["文件名", "大小", "类型", "修改时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)

    def populate(self, files):
        self.current_files = files
        self.table.setRowCount(len(files))
        for i, f in enumerate(files):
            name_item = QTableWidgetItem(f.name)
            if f.is_dir:
                name_item.setForeground(Qt.GlobalColor.darkBlue)
                name_item.setIcon(self.style().standardIcon(0))
            self.table.setItem(i, 0, name_item)

            size_item = QTableWidgetItem(f.size_str if f.size > 0 else "")
            self.table.setItem(i, 1, size_item)

            type_item = QTableWidgetItem(f.ext if f.ext else "文件夹")
            self.table.setItem(i, 2, type_item)

            try:
                mtime = datetime.fromtimestamp(float(f.modified)).strftime("%Y-%m-%d %H:%M")
            except (ValueError, TypeError):
                mtime = ""
            time_item = QTableWidgetItem(mtime)
            self.table.setItem(i, 3, time_item)

    def get_selected_files(self):
        selected_rows = self.table.selectionModel().selectedRows()
        return [self.current_files[row.row()] for row in selected_rows if not self.current_files[row.row()].is_dir]

    def _on_item_double_clicked(self, item, column):
        row = item.row()
        if row < len(self.current_files):
            self.file_double_clicked.emit(self.current_files[row].path)

    def _on_selection_changed(self):
        selected = self.get_selected_files()
        self.files_selected.emit([f.path for f in selected])
