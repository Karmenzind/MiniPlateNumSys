# coding: utf-8

tmp = '''hello'''
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QSpinBox,
                             QVBoxLayout, QTabWidget, QTextBrowser, QPushButton, QTableWidget)
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5 import QtGui
from CustomazingTab import Form as _custom
from RecommendationTab import Form as _recom
from RecommendationTab import SimilarQueryTab as _simi

class mainWin(QDialog):

    def __init__(self, parent=None, ):
        super(mainWin, self).__init__(parent)

        self.display_info = QTableWidget()
        self.display_info.setColumnCount(1)

        self.ui_custom = _custom()
        self.ui_recom = _recom()
        self.ui_simi = _simi()

        tab_title_font = QtGui.QFont("Microsoft YaHei UI", 13)
        tab_title_font.setBold(0)

        tabs = QTabWidget()
        tabs.setFont(tab_title_font)
        tabs.addTab(self.ui_custom, u"自编自选")
        tabs.addTab(self.ui_recom, u"系统推荐")
        tabs.addTab(self.ui_simi, u"近似查询")
        exitbutton = QPushButton()
        exitbutton.setMinimumSize(40, 40)
        exitbutton.setMaximumSize(40, 40)
        exitbutton.setIcon(QtGui.QIcon('./GuiPart/pic/exit.jpg'))
        exitbutton.clicked.connect(QCoreApplication.instance().quit)
        layout = QGridLayout()
        layout.addWidget(exitbutton, 0, 0)
        layout.addWidget(self.display_info, 1, 0)
        layout.addWidget(tabs, 0, 1, 2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        self.resize(1200, 310)
        self.setLayout(layout)
        self.setWindowTitle(u"车牌号自选&推荐")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

