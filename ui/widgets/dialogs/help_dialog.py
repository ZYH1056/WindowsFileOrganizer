from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                             QScrollArea, QTextEdit, QHBoxLayout)
from PyQt6.QtCore import Qt


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("使用说明")
        self.setMinimumSize(550, 450)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QTextEdit()
        content.setReadOnly(True)
        content.setHtml("""
        <style>
            body { font-family: 'Microsoft YaHei', sans-serif; font-size: 14px; line-height: 1.6; }
            h2 { color: #2c3e50; margin-bottom: 15px; }
            h3 { color: #34495e; margin-top: 20px; margin-bottom: 10px; }
            p { margin: 8px 0; color: #555; }
            ul { margin: 8px 0; padding-left: 20px; }
            li { margin: 5px 0; }
            .highlight { color: #3498db; font-weight: bold; }
        </style>
        <h2>Windows 文件整理工具</h2>
        <p>由 <span class="highlight">搞机协会</span> 开发，专为 Windows 用户打造的本地文件管理利器。</p>

        <h3>目录选择</h3>
        <p>点击左侧「选择目录」按钮，选择要整理的文件夹。支持桌面、下载目录、U盘等任意本地路径。</p>

        <h3>自动分类</h3>
        <p>根据文件后缀自动分拣到对应分类文件夹（图片、视频、文档、安装包、压缩包、脚本）。</p>

        <h3>查找重复文件</h3>
        <p>通过 SHA-256 哈希比对精准查找重复文件，支持批量删除冗余副本。</p>

        <h3>批量重命名</h3>
        <p>支持添加前缀、后缀、数字序列、日期等多种重命名规则，实时预览修改效果。</p>

        <h3>一键规整桌面</h3>
        <p>一键将桌面所有文件移入「桌面归档」文件夹，自动忽略快捷方式。</p>

        <h3>操作撤回</h3>
        <p>可撤回最近一次文件移动、删除或重命名操作，防止误操作。</p>

        <h3>ZIP 打包归档</h3>
        <p>选中文件批量打包为 ZIP，可按分类单独压缩保存。</p>

        <h3>深色模式</h3>
        <p>点击右侧「深色模式」按钮切换界面主题。</p>

        <h3>注意事项</h3>
        <ul>
            <li>所有操作均在本地执行，不上传任何数据</li>
            <li>高危操作（删除、批量移动）会弹出二次确认</li>
            <li>操作日志保存在程序同目录的 operation_log.txt</li>
        </ul>
        """)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn = QPushButton("知道了")
        btn.setFixedSize(80, 30)
        btn.clicked.connect(self.accept)
        btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
