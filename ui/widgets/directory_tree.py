from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from core.file_scanner import get_desktop_path, get_downloads_path
import os


class DirectoryTree(QWidget):
    directory_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        title_label = QLabel("目录")
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(title_label)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.tree)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(3)

        self.btn_select_dir = QPushButton("选择目录")
        self.btn_select_dir.setFixedHeight(28)

        self.btn_desktop = QPushButton("桌面")
        self.btn_desktop.setFixedHeight(28)

        self.btn_downloads = QPushButton("下载")
        self.btn_downloads.setFixedHeight(28)

        btn_layout.addWidget(self.btn_select_dir)
        btn_layout.addWidget(self.btn_desktop)
        btn_layout.addWidget(self.btn_downloads)
        layout.addLayout(btn_layout)

        self.btn_select_dir.clicked.connect(self._on_select_dir)
        self.btn_desktop.clicked.connect(lambda: self._on_favorite_path(get_desktop_path()))
        self.btn_downloads.clicked.connect(lambda: self._on_favorite_path(get_downloads_path()))

        self._populate_tree()

    def _populate_tree(self):
        self.tree.clear()
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "此电脑")

        try:
            for drive in os.listdir("C:/")[:5]:
                QTreeWidgetItem(root, [drive])
        except PermissionError:
            pass

        desktop_item = QTreeWidgetItem(root, ["桌面"])
        downloads_item = QTreeWidgetItem(root, ["下载"])

        self.tree.expand(root)

    def _on_item_double_clicked(self, item, column):
        path = ""
        if item.text(0) == "桌面":
            path = get_desktop_path()
        elif item.text(0) == "下载":
            path = get_downloads_path()
        elif item.parent() and item.parent().text(0) == "此电脑":
            path = f"{item.text(0)}/"

        if path and os.path.isdir(path):
            self.directory_selected.emit(path)

    def _on_select_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            self.directory_selected.emit(path)
            self._add_to_tree(path)

    def _on_favorite_path(self, path):
        if os.path.isdir(path):
            self.directory_selected.emit(path)

    def _add_to_tree(self, path):
        root = self.tree.topLevelItem(0)
        if root:
            QTreeWidgetItem(root, [os.path.basename(path)])
