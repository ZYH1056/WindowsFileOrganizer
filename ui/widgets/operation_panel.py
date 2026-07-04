from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal


class OperationPanel(QWidget):
    auto_classify = pyqtSignal()
    find_duplicates = pyqtSignal()
    batch_rename = pyqtSignal()
    organize_desktop = pyqtSignal()
    pack_zip = pyqtSignal()
    undo = pyqtSignal()
    toggle_theme = pyqtSignal()
    show_help = pyqtSignal()
    custom_rules = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_mode = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)

        title_label = QLabel("操作")
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(title_label)

        self.btn_auto_classify = QPushButton("自动分类")
        self.btn_auto_classify.setFixedHeight(32)
        self.btn_auto_classify.setStyleSheet("font-size: 13px;")

        self.btn_find_duplicates = QPushButton("查找重复文件")
        self.btn_find_duplicates.setFixedHeight(32)

        self.btn_batch_rename = QPushButton("批量重命名")
        self.btn_batch_rename.setFixedHeight(32)

        self.btn_organize_desktop = QPushButton("一键规整桌面")
        self.btn_organize_desktop.setFixedHeight(36)
        self.btn_organize_desktop.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.btn_pack_zip = QPushButton("打包 ZIP")
        self.btn_pack_zip.setFixedHeight(32)

        layout.addWidget(self.btn_auto_classify)
        layout.addWidget(self.btn_find_duplicates)
        layout.addWidget(self.btn_batch_rename)
        layout.addWidget(self.btn_organize_desktop)
        layout.addWidget(self.btn_pack_zip)

        layout.addStretch()

        self.btn_custom_rules = QPushButton("自定义规则")
        self.btn_custom_rules.setFixedHeight(28)

        self.btn_undo = QPushButton("撤回")
        self.btn_undo.setFixedHeight(28)
        self.btn_undo.setEnabled(False)

        self.btn_theme = QPushButton("深色模式")
        self.btn_theme.setFixedHeight(28)

        self.btn_help = QPushButton("使用说明")
        self.btn_help.setFixedHeight(28)

        layout.addWidget(self.btn_custom_rules)
        layout.addWidget(self.btn_undo)
        layout.addWidget(self.btn_theme)
        layout.addWidget(self.btn_help)

        self.btn_auto_classify.clicked.connect(self.auto_classify.emit)
        self.btn_find_duplicates.clicked.connect(self.find_duplicates.emit)
        self.btn_batch_rename.clicked.connect(self.batch_rename.emit)
        self.btn_organize_desktop.clicked.connect(self.organize_desktop.emit)
        self.btn_pack_zip.clicked.connect(self.pack_zip.emit)
        self.btn_custom_rules.clicked.connect(self.custom_rules.emit)
        self.btn_undo.clicked.connect(self.undo.emit)
        self.btn_theme.clicked.connect(self._on_toggle_theme)
        self.btn_help.clicked.connect(self.show_help.emit)

    def update_undo_state(self, has_undo):
        self.btn_undo.setEnabled(has_undo)

    def _on_toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.btn_theme.setText("浅色模式" if self.is_dark_mode else "深色模式")
        self.toggle_theme.emit()
