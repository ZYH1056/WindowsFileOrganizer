from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget,
                             QListWidgetItem, QComboBox)
from PyQt6.QtCore import Qt
from core.classifier import Classifier
import json


class CustomRuleDialog(QDialog):
    def __init__(self, classifier: Classifier, parent=None):
        super().__init__(parent)
        self.classifier = classifier
        self.setWindowTitle("自定义分类规则")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        category_layout = QHBoxLayout()
        category_layout.setSpacing(10)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(self.classifier.get_categories())

        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("输入后缀，如 .txt")

        self.btn_add_ext = QPushButton("添加后缀")
        self.btn_add_ext.setFixedSize(80, 28)

        category_layout.addWidget(QLabel("分类:"))
        category_layout.addWidget(self.cat_combo)
        category_layout.addWidget(QLabel("后缀:"))
        category_layout.addWidget(self.ext_input)
        category_layout.addWidget(self.btn_add_ext)
        layout.addLayout(category_layout)

        self.ext_list = QListWidget()
        self._populate_ext_list()
        layout.addWidget(self.ext_list)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_remove = QPushButton("移除选中")
        self.btn_remove.setFixedSize(100, 30)

        self.btn_save = QPushButton("保存")
        self.btn_save.setFixedSize(80, 30)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setFixedSize(80, 30)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_add_ext.clicked.connect(self._on_add_ext)
        self.btn_remove.clicked.connect(self._on_remove_ext)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_cancel.clicked.connect(self.reject)
        self.cat_combo.currentTextChanged.connect(self._populate_ext_list)

    def _populate_ext_list(self):
        self.ext_list.clear()
        cat = self.cat_combo.currentText()
        if cat == "其他":
            return
        exts = self.classifier.rules.get(cat, [])
        for ext in exts:
            self.ext_list.addItem(QListWidgetItem(ext))

    def _on_add_ext(self):
        ext = self.ext_input.text().strip()
        if not ext.startswith("."):
            ext = "." + ext
        cat = self.cat_combo.currentText()
        if cat == "其他":
            return
        if ext and ext not in self.classifier.rules.get(cat, []):
            self.classifier.rules[cat].append(ext)
            self._populate_ext_list()
            self.ext_input.clear()

    def _on_remove_ext(self):
        selected = self.ext_list.selectedItems()
        if not selected:
            return
        cat = self.cat_combo.currentText()
        for item in selected:
            ext = item.text()
            if ext in self.classifier.rules.get(cat, []):
                self.classifier.rules[cat].remove(ext)
        self._populate_ext_list()

    def _on_save(self):
        self.classifier.update_rules(self.classifier.rules)
        self.accept()
