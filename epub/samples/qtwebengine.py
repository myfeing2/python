import os
import sys

# 必须在创建 QApplication 之前设置
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

app = QApplication(sys.argv)
view = QWebEngineView()
view.load(QUrl("https://qt.io"))
view.show()
sys.exit(app.exec())
