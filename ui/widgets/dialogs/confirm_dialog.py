from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt


class ConfirmDialog(QDialog):
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(360, 160)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_ok = QPushButton("确认")
        self.btn_ok.setFixedSize(80, 30)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setFixedSize(80, 30)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
