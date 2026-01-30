import sys
import asyncio
import threading
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFontDatabase, QIcon

from overlay import VoxStatOverlay, resource_path
from watcher import watch_log


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        app.setWindowIcon(
            QIcon(resource_path("assets/icon.ico"))
        )

        QFontDatabase.addApplicationFont(
            resource_path("assets/fonts/mcfont.ttf")
        )
        QFontDatabase.addApplicationFont(
            resource_path("assets/fonts/roboto.ttf")
        )

        overlay = VoxStatOverlay()
        overlay.show()

        loop = asyncio.new_event_loop()
        threading.Thread(
            target=start_loop,
            args=(loop,),
            daemon=True
        ).start()

        asyncio.run_coroutine_threadsafe(
            watch_log(overlay),
            loop
        )

        sys.exit(app.exec())

    except Exception:
        QMessageBox.critical(
            None,
            "VoxStat Overlay",
            "A fatal error occurred.\n\nPlease restart the application."
        )
        sys.exit(5)
