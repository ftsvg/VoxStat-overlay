from PyQt6.QtCore import QObject, pyqtSignal

class OverlaySignals(QObject):
    update_players = pyqtSignal(list)