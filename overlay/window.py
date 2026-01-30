from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

from .table import PlayerTable
from .settings import SettingsPage
from .signals import OverlaySignals
from .resources import resource_path
from .cfg import config


PRIMARY_COLOR = "#5555FF"
SUCCESS_COLOR = "#55FF55"
ERROR_COLOR = "#FF5555"
BG_RGBA = "rgba(17, 17, 17, 220)"
RADIUS = 8


class VoxStatOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.signals = OverlaySignals()
        self.signals.update_players.connect(self._update_players)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(900, 420)

        self._drag_pos = None
        self._error_visible = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        container = QWidget()
        container.setStyleSheet(f"""
            background-color: {BG_RGBA};
            border-radius: {RADIUS}px;
        """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.header = QWidget()
        self.header.setFixedHeight(54)
        self.header.setStyleSheet("background-color: transparent;")

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(14, 0, 14, 0)

        logo = QLabel()
        logo.setPixmap(
            QPixmap(resource_path("assets/images/logo.png")).scaled(
                30, 30,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        title = QLabel("VoxStat Overlay")
        title.setStyleSheet(f"""
            color: {PRIMARY_COLOR};
            font-size: 18px;
            font-weight: 700;
        """)

        header_layout.addWidget(logo)
        header_layout.addSpacing(10)
        header_layout.addWidget(title)
        header_layout.addStretch()

        btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #AAAAAA;
                font-size: 14px;
                padding: 6px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
                color: #FFFFFF;
            }
        """

        close_btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #AAAAAA;
                font-size: 14px;
                padding: 6px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 85, 85, 0.15);
                color: #FF5555;
            }
        """

        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setStyleSheet(btn_style)
        self.settings_btn.clicked.connect(self.open_settings)

        self.min_btn = QPushButton("—")
        self.min_btn.setStyleSheet(btn_style)
        self.min_btn.clicked.connect(self.showMinimized)

        self.close_btn = QPushButton("✕")
        self.close_btn.setStyleSheet(close_btn_style)
        self.close_btn.clicked.connect(self.close)

        header_layout.addWidget(self.settings_btn)
        header_layout.addWidget(self.min_btn)
        header_layout.addWidget(self.close_btn)

        container_layout.addWidget(self.header)

        body = QWidget()
        body.setStyleSheet("background-color: transparent;")

        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(12, 12, 12, 12)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;")

        self.table = PlayerTable()
        self.settings = SettingsPage(self)

        self.stack.addWidget(self.table)
        self.stack.addWidget(self.settings)

        body_layout.addWidget(self.stack)
        container_layout.addWidget(body)
        root.addWidget(container)

        self.toast = QLabel("", self)
        self.toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toast.setStyleSheet("""
            background-color: rgba(85, 255, 85, 0.18);
            color: #55FF55;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 700;
            min-width: 260px;
        """)
        self.toast.hide()

        QTimer.singleShot(0, self._check_api_key)

    def _check_api_key(self):
        if not config.api_key:
            self.open_settings()
            self.show_toast("Please set your API key", error=True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_toast()

    def _position_toast(self):
        w = self.toast.sizeHint().width()
        self.toast.move((self.width() - w) // 2, 16)

    def show_toast(self, text, error=False):
        self._error_visible = error

        if error:
            self.toast.setStyleSheet("""
                background-color: rgba(255, 85, 85, 0.18);
                color: #FF5555;
                padding: 10px 18px;
                border-radius: 10px;
                font-weight: 700;
                min-width: 260px;
            """)
        else:
            self.toast.setStyleSheet("""
                background-color: rgba(85, 255, 85, 0.18);
                color: #55FF55;
                padding: 10px 18px;
                border-radius: 10px;
                font-weight: 700;
                min-width: 260px;
            """)

        self.toast.setText(text)
        self._position_toast()
        self.toast.raise_()
        self.toast.show()

        if not error:
            QTimer.singleShot(2000, self.toast.hide)

    def clear_error_toast(self):
        if self._error_visible:
            self._error_visible = False
            self.toast.hide()

    def open_settings(self):
        self.stack.setCurrentIndex(1)

    def open_overlay(self):
        self.stack.setCurrentIndex(0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    def _update_players(self, players):
        self.table.clear_players()
        for display_name, stats in players:
            self.table.add_player(display_name, stats)
