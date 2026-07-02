from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from core.batch_rename import preview_rename, apply_rename


class RenameDialog(QDialog):
    def __init__(self, files: list, parent=None):
        super().__init__(parent)
        self.files = files
        self.setWindowTitle("批量重命名")
        self.setMinimumSize(600, 450)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.renamed_results = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        rule_layout = QHBoxLayout()
        rule_layout.setSpacing(10)

        rule_label = QLabel("重命名规则:")
        rule_label.setFixedWidth(80)

        self.rule_combo = QComboBox()
        self.rule_combo.addItems(["前缀", "后缀", "数字序列", "日期"])
        self.rule_combo.currentTextChanged.connect(self._on_rule_changed)

        self.param_label = QLabel("参数:")
        self.param_label.setFixedWidth(40)

        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("输入前缀/后缀内容")

        self.btn_preview = QPushButton("预览")
        self.btn_preview.setFixedSize(80, 28)
        self.btn_preview.clicked.connect(self._on_preview)

        rule_layout.addWidget(rule_label)
        rule_layout.addWidget(self.rule_combo)
        rule_layout.addWidget(self.param_label)
        rule_layout.addWidget(self.param_input)
        rule_layout.addWidget(self.btn_preview)
        layout.addLayout(rule_layout)

        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(2)
        self.preview_table.setHorizontalHeaderLabels(["原文件名", "新文件名"])
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.preview_table)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_apply = QPushButton("应用")
        self.btn_apply.setFixedSize(80, 30)
        self.btn_apply.clicked.connect(self._on_apply)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setFixedSize(80, 30)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_apply)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_apply.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def _on_rule_changed(self, text):
        if text == "数字序列":
            self.param_input.setPlaceholderText("起始数字，默认为 1")
            self.param_input.setText("1")
        elif text == "日期":
            self.param_input.setPlaceholderText("日期格式，如 YYYYMMDD")
            self.param_input.setText("YYYYMMDD")
        else:
            self.param_input.setPlaceholderText("输入前缀/后缀内容")
            self.param_input.clear()

    def _on_preview(self):
        rule_map = {"前缀": "prefix", "后缀": "suffix", "数字序列": "sequence", "日期": "date"}
        rule = rule_map.get(self.rule_combo.currentText(), "prefix")
        param = self.param_input.text()

        kwargs = {}
        if rule == "prefix":
            kwargs["prefix"] = param
        elif rule == "suffix":
            kwargs["suffix"] = param
        elif rule == "sequence":
            try:
                kwargs["start"] = int(param) if param else 1
            except ValueError:
                kwargs["start"] = 1
        elif rule == "date":
            kwargs["date_fmt"] = param.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")

        results = preview_rename(self.files, rule, **kwargs)

        self.preview_table.setRowCount(len(results))
        for i, (_, original, new_name) in enumerate(results):
            self.preview_table.setItem(i, 0, QTableWidgetItem(original))
            item = QTableWidgetItem(new_name)
            item.setForeground(Qt.GlobalColor.blue)
            self.preview_table.setItem(i, 1, item)

    def _on_apply(self):
        rule_map = {"前缀": "prefix", "后缀": "suffix", "数字序列": "sequence", "日期": "date"}
        rule = rule_map.get(self.rule_combo.currentText(), "prefix")
        param = self.param_input.text()

        kwargs = {}
        if rule == "prefix":
            kwargs["prefix"] = param
        elif rule == "suffix":
            kwargs["suffix"] = param
        elif rule == "sequence":
            try:
                kwargs["start"] = int(param) if param else 1
            except ValueError:
                kwargs["start"] = 1
        elif rule == "date":
            kwargs["date_fmt"] = param.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")

        self.renamed_results = apply_rename(self.files, rule, **kwargs)
        self.accept()
