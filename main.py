# coding: utf-8

import sys
from PyQt5.QtWidgets import QApplication

from GuiPart.fakeLogin import fakeLogin
from GuiPart.coreFrame import mainWin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    lg = fakeLogin()
    lg.show()
    app.exec_()

