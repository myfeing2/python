# This Python file uses the following encoding: utf-8
import sys, os

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

from PySide6.QtCore import (QItemSelection, QLibraryInfo, QLocale, QTranslator, Slot)

import rc_internetarchive2cue
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon

# sys.path.append("../../")

import convert2cue

basedir = os.path.dirname(__file__)
try: 
    from ctypes import windll # Only exists on Windows.
    myappid = "feiminyu.internetarchive2cue.0.1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.okBtn.clicked.connect(self.convert)
        self.ui.toolBtn.clicked.connect(self.openfiledialog)

    @Slot()
    def convert(self):
        fn = self.ui.lineEdit.text()
        fn = fn.strip()
        if fn != "":
            convert2cue.convert2cue(fn)

    @Slot()
    def openfiledialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "All Files (*);; Python Files (*.json)",
        )
        # print(fname)
        self.ui.lineEdit.setText(fname[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "res/internet-archive1.svg")))

    path = QLibraryInfo.path(QLibraryInfo.TranslationsPath)
    translator = QTranslator(app)
    if translator.load(QLocale.system(), 'qtbase', '_', path):
        # print('loaded qtbase')
        app.installTranslator(translator)
    #translator = QTranslator(app)
    path = ':/translations'
    if translator.load(QLocale.system(), 'translations\\internetarchive2cue', '_', path):
        # print('loaded internetarchive2cue')
        app.installTranslator(translator)

    widget = Widget()
    widget.show()
    sys.exit(app.exec())
