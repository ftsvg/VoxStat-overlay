import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from .cfg import config

PRIMARY_COLOR = "#5555FF"


class SettingsPage(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.setStyleSheet("background-color: transparent;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("Settings")
        title.setStyleSheet(f"""
            color: {PRIMARY_COLOR};
            font-size: 18px;
            font-weight: 700;
        """)

        log_label = QLabel("Logs file")
        log_label.setStyleSheet("color: #FFFFFF; font-weight: 700;")

        self.path_label = QLabel(config.log_path or "No log file selected")
        self.path_label.setStyleSheet("color: #AAAAAA;")

        btn_primary = """
            QPushButton {
                background-color: #5555FF;
                color: white;
                padding: 12px;
                min-height: 24px;
                border-radius: 8px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #6666FF;
            }
        """

        pick_btn = QPushButton("Select logs file")
        pick_btn.setStyleSheet(btn_primary)
        pick_btn.clicked.connect(self.pick_log)

        api_label = QLabel("API key")
        api_label.setStyleSheet("color: #FFFFFF; font-weight: 700;")

        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter your API key")
        self.api_input.setText(config.api_key or "")
        self.api_input.setStyleSheet("""
            QLineEdit {
                background-color: #1A1A1A;
                color: white;
                padding: 12px;
                min-height: 24px;
                border-radius: 8px;
                border: 1px solid #2A2A2A;
                font-weight: 600;
            }
        """)

        save_btn = QPushButton("Save settings")
        save_btn.setStyleSheet(btn_primary)
        save_btn.clicked.connect(self.save_settings)

        layout.addWidget(title)
        layout.addWidget(log_label)
        layout.addWidget(self.path_label)
        layout.addWidget(pick_btn)
        layout.addWidget(api_label)
        layout.addWidget(self.api_input)
        layout.addSpacing(18)
        layout.addWidget(save_btn)
        layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

    def pick_log(self):
        appdata = os.environ.get("APPDATA", "")
        mc_logs = os.path.join(appdata, ".minecraft", "logs")
        start_dir = mc_logs if os.path.isdir(mc_logs) else appdata

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Minecraft latest.log",
            start_dir,
            "Log files (*.log)"
        )
        if path:
            config.log_path = path
            self.path_label.setText(path)

    def save_settings(self):
        key = self.api_input.text().strip()
        config.api_key = key if key else None
        config.save()

        if config.api_key:
            self.overlay.clear_error_toast()

        self.overlay.open_overlay()
        self.overlay.show_toast("Settings saved")
