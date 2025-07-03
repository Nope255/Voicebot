import sys
import asyncio
import logging
import logging.handlers
import platform
from PyQt6.QtWidgets import QApplication
from core import TACTICS


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.TimedRotatingFileHandler('tactics.log', when='midnight', encoding='utf-8', backupCount=7),
        logging.StreamHandler()
    ]
)

if platform.system() == "Emscripten":
    async def main():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        tactics = TACTICS()
        tactics.show()
        await asyncio.sleep(0)
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        tactics = TACTICS()
        tactics.show()
        sys.exit(app.exec())