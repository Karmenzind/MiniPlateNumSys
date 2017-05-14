# coding: utf-8

import re
import string
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QApplication,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QSpinBox,
                             QVBoxLayout, QTabWidget, QPushButton, QToolButton, QHBoxLayout,
                             QToolBox, QLCDNumber, QMessageBox, QTextBrowser, QComboBox)
from PyQt5.QtCore import (Qt, QSize, QCoreApplication)
from PyQt5.QtGui import QFont, QPalette
from support.dbOper import dbOper
from support.plateNumAlg import select_over


res_pattern = re.compile(r'\d([0-9\s][A-Z\s][0-9\s]|[A-Z\s][0-9\s][0-9\s]|[0-9\s][0-9\s][A-Z\s])[\s\d]')

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.keyboard_layout = QVBoxLayout()
        self.create_keyboard()

        res_p = QPalette()
        res_p.setColor(QPalette.Window, Qt.lightGray)  # 设置背景颜色

        # res_label = QLabel(u'沪')
        plt_levels = [u'沪'+x for x in string.ascii_uppercase]
        self.plate_level = QComboBox()
        self.plate_level.addItems(plt_levels)
        self.plate_level.setMinimumSize(0, 100)
        # self.plate_level.set

        self.res = QLabel()
        # self.res.setStyleSheet()
        self.res.setAutoFillBackground(True)
        self.res.setPalette(res_p)

        res_font = QFont("Microsoft YaHei UI Light")
        res_font.setPointSize(50)
        res_font.setBold(True)
        res_font.setItalic(False)
        res_font.setWeight(30)
        # res_label.setFont(res_font)
        # res_label.setAlignment(Qt.AlignRight)
        self.res.setFont(res_font)
        self.plate_level.setFont(res_font)
        self.res.setAlignment(Qt.AlignHCenter)

        self.del_button = QPushButton(u'删除')
        self.firm_button = QPushButton(u'确认')

        self.del_button.setFont(QFont("Microsoft YaHei UI", 20))
        self.firm_button.setFont(QFont("Microsoft YaHei UI", 20))
        self.del_button.setMinimumSize(QSize(0, 40))
        self.firm_button.setMinimumSize(QSize(0, 40))

        self.del_button.clicked.connect(self.del_action)
        self.firm_button.clicked.connect(self.submit_action)
        handle_buttons = QHBoxLayout()
        handle_buttons.addWidget(self.del_button)
        handle_buttons.addWidget(self.firm_button)

        main_layout = QGridLayout()
        main_layout.addLayout(self.keyboard_layout, 0, 0, 1, 4)
        main_layout.addWidget(self.plate_level, 1, 0, 1, 1)
        main_layout.addWidget(self.res, 1, 1, 1, 3)
        main_layout.addLayout(handle_buttons, 2, 2, 1, 2)

        self.error_plate_format = QMessageBox()
        self.error_plate_format.setText(u"1、最多5位\n2、首尾必须为数字\n3、有且只能有一个字母\n4、数字不能全为零")
        self.error_plate_format.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.result_plate = ''
        self.user_account = ''

        self.setLayout(main_layout)

    def create_keyboard(self):
        self.button_1 = QPushButton('1')
        self.button_2 = QPushButton('2')
        self.button_3 = QPushButton('3')
        self.button_4 = QPushButton('4')
        self.button_5 = QPushButton('5')
        self.button_6 = QPushButton('6')
        self.button_7 = QPushButton('7')
        self.button_8 = QPushButton('8')
        self.button_9 = QPushButton('9')
        self.button_0 = QPushButton('0')

        self.button_Q = QPushButton('Q')
        self.button_W = QPushButton('W')
        self.button_E = QPushButton('E')
        self.button_R = QPushButton('R')
        self.button_T = QPushButton('T')
        self.button_Y = QPushButton('Y')
        self.button_U = QPushButton('U')
        self.button_I = QPushButton('I')
        self.button_O = QPushButton('O')
        self.button_P = QPushButton('P')

        self.button_A = QPushButton('A')
        self.button_S = QPushButton('S')
        self.button_D = QPushButton('D')
        self.button_F = QPushButton('F')
        self.button_G = QPushButton('G')
        self.button_H = QPushButton('H')
        self.button_J = QPushButton('J')
        self.button_K = QPushButton('K')
        self.button_L = QPushButton('L')

        self.button_Z = QPushButton('Z')
        self.button_X = QPushButton('X')
        self.button_C = QPushButton('C')
        self.button_V = QPushButton('V')
        self.button_B = QPushButton('B')
        self.button_N = QPushButton('N')
        self.button_M = QPushButton('M')

        for idx, line in enumerate((
                [self.button_1, self.button_2, self.button_3, self.button_4, self.button_5, self.button_6,
                 self.button_7, self.button_8, self.button_9, self.button_0],
                [self.button_Q, self.button_W, self.button_E, self.button_R, self.button_T, self.button_Y,
                 self.button_U, self.button_I, self.button_O, self.button_P],
                [self.button_A, self.button_S, self.button_D, self.button_F, self.button_G, self.button_H,
                 self.button_J, self.button_K, self.button_L],
                [self.button_Z, self.button_X, self.button_C, self.button_V, self.button_B, self.button_N,
                 self.button_M])):
            tmp_box = QHBoxLayout()
            tmp_box.setSpacing(1)
            tmp_box.setContentsMargins(11, 11, 11, 11)
            for button in line:
                # 按钮特征
                button.setMinimumSize(QSize(0, 40))
                button.setMaximumSize(QSize(198, 16777215))
                tmp_box.addWidget(button)
                # 按钮字体
                button_font = QFont("Microsoft YaHei UI")
                button_font.setPointSize(25)
                button_font.setWeight(20)

                button.setFont(button_font)

                # button.setStyleSheet("QPushButton{background-color:#F4F4F4;color:#080808;}"
                #                         "QPushButton:hover{background-color:#F5FFFA;}")

                # Button action
                button.clicked.connect(self.click_key)
            self.keyboard_layout.addLayout(tmp_box)
            tmp_box.setAlignment(Qt.AlignHCenter)

    def click_key(self):

        button = self.sender()
        if button is None or not isinstance(button, QPushButton):
            return
        tmp_txt = self.res.text() + button.text()
        # print tmp_txt.__repr__()
        # print ': <5'.format(tmp_txt).__repr__()
        if len(tmp_txt) <= 5 and res_pattern.match('{: <5}'.format(tmp_txt)) and tmp_txt.find('0') < 4:
            self.res.setText(tmp_txt)
        else:
            self.error_plate_format.show()


    def del_action(self):
        self.res.setText(self.res.text()[:-1])

    def submit_action(self):

        reply_confirm = QMessageBox.question(self, u"请确认", u"选定 {}？选定后不可更改".format(self.res.text()),
                                             QMessageBox.Yes | QMessageBox.No)
        if reply_confirm == QMessageBox.Yes:
            self.confirm_action()

    def confirm_action(self):
        reply_message = QTextBrowser()
        self.result_plate = dict(prefix=self.plate_level.currentText()[-1], plate_num=self.res.text())
        occupy_query = dbOper().query('''SELECT occupied FROM `plate_nums` where prefix='{prefix}' and plate_num='{plate_num}';'''.format(**self.result_plate))
        if occupy_query:
            if occupy_query[0]['occupied'].__str__() == '1':
                QMessageBox.question(self, u"输入无效", u"抱歉，您所输入的牌号\n{}\n已经被占用，请重新选择".format(self.res.text()),
                                     QMessageBox.Yes)
            else:
                reply = QMessageBox.question(self, u"选择成功", u"恭喜，您所输入的牌号\n{}\n可以使用，请点击确认".format(self.res.text()),
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    select_over(user_account=self.user_account, **self.result_plate)
        else:
            dbOper().update('''insert into plate_nums set prefix='{prefix}', plate_num='{plate_num}';'''.format(**self.result_plate))
            reply = QMessageBox.question(self, u"选择成功", u"恭喜，您所输入的牌号\n{}\n可以使用，请点击确认".format(self.res.text()),
                                 QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                select_over(user_account=self.user_account, **self.result_plate)
                QCoreApplication.instance().quit()