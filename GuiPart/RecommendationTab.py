# coding: utf-8

import random
import string
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QApplication,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QSpinBox,
                             QVBoxLayout, QTabWidget, QPushButton, QToolButton, QHBoxLayout,
                             QToolBox, QLCDNumber, QMessageBox, QTextBrowser, QScrollArea)
from PyQt5.QtCore import (Qt, QSize, QCoreApplication,)
from PyQt5.QtGui import QFont
import time
from support.plateNumAlg import create_content, QUERY_IF_EXISTS, enlarge_table, select_over
from support.dbOper import dbOper

SELECT_NOT_OCCUPIED = '''SELECT * FROM `plate_nums` where occupied = 0  limit {qty};'''

class subForm(QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        res_font = QFont()
        res_font.setPointSize(30)
        res_font.setBold(True)
        res_font.setItalic(False)
        res_font.setWeight(20)

        self.begin_button = QPushButton(u"开始自动生成")
        self.begin_button.setFont(res_font)

        button_box = QHBoxLayout()
        button_box.addWidget(self.begin_button)
        main_layout = QVBoxLayout()

        self.res_box = QGridLayout()
        main_layout.addLayout(button_box)
        main_layout.addLayout(self.res_box)

        self.begin_button.clicked.connect(self.create_res)

        self.setLayout(main_layout)

        self.before_select_message = QMessageBox()
        self.before_select_message.setText(u"请谨慎选择\n选中将无法修改")
        self.before_select_message.setFont(QFont("Microsoft YaHei UI", 12))
        self.before_select_message.setWindowTitle(u"！")
        self.before_select_message.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.result_plate = ''
        self.user_account = ''

        self.congratulation = QMessageBox()
        self.congratulation.setWindowTitle(u'恭喜!')
        self.congratulation.buttonClicked.connect(QCoreApplication.instance().quit)
        self.congratulation.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.congratulation.setFont(QFont("Microsoft YaHei UI", 12))


    def create_res(self):
        base = string.ascii_uppercase + string.digits
        res = should_have_qty(45)

        for idx, item in enumerate(res):
            button = QPushButton()
            self.res_box.addWidget(button, idx/3, idx%3)
            self.res_box.setAlignment(Qt.AlignHCenter)
            tmp_plate = u'沪' + item['prefix'] + '/ ' + item['plate_num']
            button.setText(tmp_plate)
            res_font = QFont()
            res_font.setPointSize(30)
            res_font.setBold(True)
            res_font.setItalic(False)
            res_font.setWeight(20)
            button.setFont(res_font)
            button.kv = item
            button.clicked.connect(self.after_select)
        self.begin_button.setDisabled(1)

    def after_select(self):
        self.result_plate = self.sender().kv
        are_you_sure = QMessageBox.question(self, u"", u"你确定吗？", QMessageBox.Yes | QMessageBox.No)
        if are_you_sure == QMessageBox.Yes:
            self.congratulation.setText(
                u"您已经选号成功！\n您的车牌号为: 沪%s %s" % (self.result_plate['prefix'], self.result_plate['plate_num']))
            self.congratulation.show()
            select_over(user_account=self.user_account, **self.result_plate)

class Form(QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.console = subForm(self)
        # self.console.setMinimumSize(1500, 600)

        scroll = QScrollArea()
        scroll.setWidget(self.console)
        scroll.setAutoFillBackground(True)
        scroll.setWidgetResizable(True)
        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        self.setLayout(vbox)

class SimilarQueryTab(QDialog):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)


        res_font = QFont()
        res_font.setPointSize(30)
        res_font.setBold(True)
        res_font.setItalic(False)
        res_font.setWeight(20)

        self.begin_button = QPushButton(u"点击进行近似查询")
        self.begin_button.setFont(res_font)
        self.begin_button.clicked.connect(self.create_res)

        button_box = QHBoxLayout()

        self.simi_base = ['' for i in xrange(5)]
        for i in xrange(5):
            simi_edit = QLineEdit()
            simi_edit.setFixedHeight(50)
            button_box.addWidget(simi_edit)
            simi_edit.idx = i
            simi_edit.textChanged.connect(self.simi_base_change)

        button_box.addWidget(self.begin_button)
        main_layout = QGridLayout()

        self.res_box = QGridLayout()
        main_layout.addLayout(button_box, 0, 0)
        main_layout.addLayout(self.res_box, 1, 0)

        self.setLayout(main_layout)

        self.before_select_message = QMessageBox()
        self.before_select_message.setText(u"请谨慎选择\n选中将无法修改")
        self.before_select_message.setFont(QFont("Microsoft YaHei UI", 12))
        self.before_select_message.setWindowTitle(u"！")
        self.before_select_message.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.result_plate = ''
        self.user_account = ''

        self.congratulation = QMessageBox()
        self.congratulation.setWindowTitle(u'恭喜!')
        self.congratulation.buttonClicked.connect(QCoreApplication.instance().quit)
        self.congratulation.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.congratulation.setFont(QFont("Microsoft YaHei UI", 12))

        self.error_plate_format = QMessageBox()
        self.error_plate_format.setWindowFlags(Qt.WindowStaysOnTopHint)

    def simi_base_change(self):
        okay = 1
        simi_edit = self.sender()
        if len(simi_edit.text()) > 1:
            simi_edit.setText(simi_edit.text()[0])
        if simi_edit.text() in string.lowercase:
            simi_edit.setText(simi_edit.text().upper())
        tmp = self.simi_base[:]
        tmp[simi_edit.idx] = simi_edit.text()
        if simi_edit.idx in (0, 4):
            if tmp[simi_edit.idx] and (tmp[simi_edit.idx] not in string.digits):
                self.error_plate_format.setText(u"只能为数字")
                simi_edit.setText(u'')
                self.error_plate_format.show()
                okay = 0
        if simi_edit.idx in (1, 2, 3):
            if tmp[simi_edit.idx] and (tmp[simi_edit.idx] not in string.digits+string.uppercase):
                self.error_plate_format.setText(u"只能为数字或字母")
                simi_edit.setText(u'')
                self.error_plate_format.show()
                okay = 0
        if tmp.count(u'0') == 4:
            simi_edit.setText(u'')
            self.error_plate_format.setText(u"数字不能全为0")
            self.error_plate_format.show()
            okay = 0
        qty_of_letter = 0
        for i in tmp:
            if i and (i in string.uppercase):
                qty_of_letter += 1
        if (qty_of_letter == 0 and u'' not in tmp[1:4]) or (qty_of_letter > 1):
            simi_edit.setText(u'')
            self.error_plate_format.setText(u"字母有且只能有一个")
            self.error_plate_format.show()
            okay = 0
        if okay:
            self.simi_base = tmp[:]

    def create_res(self):
        tmp = self.simi_base[:]
        for idx, k in enumerate(tmp):
            if k == '':
                tmp[idx] = u'.'
        tmp_sql = "SELECT * FROM `plate_nums` where occupied = 0  and plate_num regexp '{regexp}' limit 15".format(regexp=''.join(tmp))
        res = dbOper().query(tmp_sql)

        if not res:
            self.error_plate_format.setText(u"抱歉，查询无结果\n请尝试输入其他条件")
            self.error_plate_format.show()
        else:
            for idx, item in enumerate(res):
                button = QPushButton()
                self.res_box.addWidget(button, idx/3, idx%3)
                self.res_box.setAlignment(Qt.AlignHCenter)
                tmp_plate = u'沪' + item['prefix'] + '/ ' + item['plate_num']
                button.setText(tmp_plate)
                res_font = QFont()
                res_font.setPointSize(30)
                res_font.setBold(True)
                res_font.setItalic(False)
                res_font.setWeight(20)
                button.setFont(res_font)
                button.kv = item
                button.clicked.connect(self.after_select)
            self.begin_button.setDisabled(1)

    def after_select(self):
        self.result_plate = self.sender().kv
        are_you_sure = QMessageBox.question(self, u" ", u"你确定吗？", QMessageBox.Yes | QMessageBox.No)
        if are_you_sure == QMessageBox.Yes:
            self.congratulation.setText(
                u"您已经选号成功！\n您的车牌号为: 沪%s %s" % (self.result_plate['prefix'], self.result_plate['plate_num']))
            self.congratulation.show()
            select_over(user_account=self.user_account, **self.result_plate)

def should_have_qty(qty=6):
    res = dbOper().query(SELECT_NOT_OCCUPIED.format(qty=qty))
    if len(res) < 6:
        enlarge_table(6 - len(res))
        return should_have_qty()
    return res