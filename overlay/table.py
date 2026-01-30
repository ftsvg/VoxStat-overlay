from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .mc_colors import mc_to_html


def format_stat(value: int) -> str:
    return f"{value:,}"


STAT_COLORS = {
    "wins": "#55FF55",
    "weightedwins": "#5555FF",
    "kills": "#FF55FF",
    "finals": "#FF5555",
    "beds": "#FFFF55",
}


class PlayerTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 6)

        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setHorizontalHeaderLabels([
            "Player",
            "Wins",
            "Weighted Wins",
            "Kills",
            "Finals",
            "Beds",
        ])

        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.model().setHeaderData(
            0,
            Qt.Orientation.Horizontal,
            Qt.AlignmentFlag.AlignLeft,
            Qt.ItemDataRole.TextAlignmentRole,
        )

        self.setColumnWidth(0, 340)
        for col in range(1, 6):
            self.setColumnWidth(col, 110)

        self.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
            }

            QTableWidget::viewport {
                background-color: transparent;
            }

            QTableWidget::item {
                background-color: transparent;
            }

            QHeaderView::section {
                background-color: transparent;
                color: #FFFFFF;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #2A2A2A;
                font-weight: 700;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 6px;
            }

            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.25);
                border-radius: 3px;
            }
        """)

        self.mc_font = QFont("Minecraft", 10)

    def clear_players(self):
        self.setRowCount(0)

    def add_player(self, display_name: str, stats):
        row = self.rowCount()
        self.insertRow(row)
        self.setRowHeight(row, 34)

        name_label = QLabel()
        name_label.setTextFormat(Qt.TextFormat.RichText)
        name_label.setText(mc_to_html(display_name))
        name_label.setFont(self.mc_font)
        name_label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )
        self.setCellWidget(row, 0, name_label)

        if stats is None:
            for col in range(1, 6):
                item = QTableWidgetItem("-")
                item.setFont(self.mc_font)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(Qt.GlobalColor.gray)
                self.setItem(row, col, item)
            return

        values = [
            ("wins", stats.wins),
            ("weightedwins", stats.weightedwins),
            ("kills", stats.kills),
            ("finals", stats.finals),
            ("beds", stats.beds),
        ]

        for col, (key, value) in enumerate(values, start=1):
            item = QTableWidgetItem(format_stat(value))
            item.setFont(self.mc_font)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QtGui.QColor(STAT_COLORS[key]))
            self.setItem(row, col, item)
