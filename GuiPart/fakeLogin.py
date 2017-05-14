# coding: utf-8
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from coreFrame import mainWin
from support.dbOper import dbOper
from GuiPart.AdminWin import AdminWin
from RegisterTab import RegisterTab

class fakeLogin(QtWidgets.QDialog):
    """
    For registerin' and loggin' in 
    """

    def __init__(self, parent=None):
        super(fakeLogin, self).__init__(parent)
        # self.setWindowTitle()

        self.resize(400, 360)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        username_label = QtWidgets.QLabel(u"账号")
        username_label.setAlignment(QtCore.Qt.AlignRight)
        username_label.setFont(QtGui.QFont("Microsoft YaHei UI", 14))
        self.username_edit = QtWidgets.QLineEdit()
        self.username_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.username_edit.setFont(QtGui.QFont("Microsoft YaHei UI", 14))
        password_label = QtWidgets.QLabel(u"密码")
        password_label.setAlignment(QtCore.Qt.AlignRight)
        password_label.setFont(QtGui.QFont("Microsoft YaHei UI", 14))
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setMinimumSize(QtCore.QSize(0, 30))
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setFont(QtGui.QFont("Microsoft YaHei UI", 14))


        self.confirm = QtWidgets.QPushButton(u"登陆")
        self.register = QtWidgets.QPushButton(u"注册")
        self.cancel = QtWidgets.QPushButton(u"退出")
        self.confirm.setStyleSheet("QPushButton{background-color:#FFFFFF;color:#080808;font-size:17px;}"
                                    "QPushButton:hover{background-color:#F5FFFA;}")
        self.register.setStyleSheet("QPushButton{background-color:#FFFFFF;color:#080808;font-size:17px;}"
                                   "QPushButton:hover{background-color:#F5FFFA;}")
        self.cancel.setStyleSheet("QPushButton{background-color:#FFFFFF;color:#080808;font-size:17px;}"
                                    "QPushButton:hover{background-color:#F5FFFA;}")
        self.confirm.setFont(QtGui.QFont("Microsoft YaHei UI", 10))
        self.register.setFont(QtGui.QFont("Microsoft YaHei UI", 10))
        self.cancel.setFont(QtGui.QFont("Microsoft YaHei UI", 10))

        self.confirm.clicked.connect(self.login_check)
        self.cancel.clicked.connect(QtCore.QCoreApplication.instance().quit)


        layout = QtWidgets.QGridLayout()
        title_lable = QtWidgets.QLabel(u"车牌号自选系统")
        title_lable.setFont(QtGui.QFont("Microsoft YaHei UI", 20, QtGui.QFont.Bold))
        self.setLayout(layout)

        layout.addWidget(title_lable, 0, 0, 1, 1)
        layout.addWidget(username_label, 1, 0, 1, 1)
        layout.addWidget(self.username_edit, 1, 1, 1, 1)
        layout.addWidget(password_label, 2, 0, 1, 1)
        layout.addWidget(self.password_edit, 2, 1, 1, 1)
        layout.addWidget(self.register, 3, 0, 1, 1)
        layout.addWidget(self.confirm, 3, 1, 1, 1)
        layout.addWidget(self.cancel, 4, 0, 1, 2)

        self.setMouseTracking(True)
        self.setStyleSheet("background-color:#FFFFFF;")

        self.loginstate = 0
        self.mw = mainWin()
        self.admw = AdminWin()
        self.regiw = RegisterTab()
        self.register.clicked.connect(self.regiw.show)

        self.already_select = QtWidgets.QMessageBox()

        self.error_login = QtWidgets.QMessageBox()
        self.error_login.setText(u"账号或密码错误")
        self.error_login.setFont(QtGui.QFont("Microsoft YaHei UI", 15))
        self.error_login.setWindowTitle(u":-(")
        self.error_login.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def login_check(self):
        user = self.username_edit.text()
        pwd = self.password_edit.text()
        if user == 'admin':
            if pwd == 'admin':
                self.loginstate = 1
                self.hide()
                self.admw.show()
            else:
                self.error_login.show()
        else:
            tmp_sql = '''select `regi_time`, `name`, `identity`, `driv_lic`, `briefing`, `plate_num`, `obt_plate_time`, `telephone`, `e_mail`, `purchase_bill_id`, `VIN_code`, `adm_area`, `mailing_address`, `mailing_or_not`, `need_temp_or_not` from customers_info where user_account = '{}' and user_password = "{}";'''\
                .format(user, pwd)
            query_res = dbOper().query(tmp_sql)
            if query_res:
                if query_res[0]['obt_plate_time']:
                    tmp_detail = dbOper().query('''select `prefix`, `plate_num` from customers_info where user_account = '{}' and user_password = "{}";'''.format(user, pwd))[0]
                    self.already_select.setText(u"您已经选择预定过车牌\n您的车牌号是\n沪{} {}".format(tmp_detail['prefix'], tmp_detail['plate_num']))
                    self.already_select.setWindowTitle(u':-)')
                    self.already_select.show()
                else:
                    self.loginstate = 1
                    self.hide()
                    self.mw.show()
                    txt = u'你的注册信息如下：\n\n\n'
                    headers = u'''姓名 注册时间 身份证号 驾驶证 车牌号 选牌时间 联系电话 电子邮箱 购车发票 VIN编码 行政区划 邮寄地址 是否邮寄 临时号牌'''.split()
                    fin_headers = headers[:]
                    sql_fin = '''SELECT
                                    `regi_time` AS '注册时间',
                                    `name` as '姓名',
                                    `identity` as '身份证号',
                                    `driv_lic` as '驾驶证',
                                    `briefing` as '其他信息',
                                    `plate_num` as '车牌号',
                                    `obt_plate_time` AS '选牌时间',
                                    `telephone` as '联系电话',
                                    `e_mail` as '电子邮箱',
                                    `purchase_bill_id` as '购车发票',
                                    `VIN_code` as 'VIN编码',
                                    `adm_area` as '行政区划',
                                    `mailing_address` as '邮寄地址',
                                    if(`mailing_or_not` > 0, '是','否') as '是否邮寄',
                                if(`need_temp_or_not` > 0, '是','否') as '临时号牌'
                                FROM
                                    customers_info
                                WHERE
                                    user_account = '{}'
                                AND user_password = "{}";'''.format(user, pwd)
                    query_res_fin = dbOper().query(sql_fin)
                    tmp_dct = {x: y for x, y in query_res_fin[0].iteritems() if y}
                    n = 0
                    for header in headers:
                        if query_res_fin[0][header]:
                            self.mw.display_info.insertRow(n)
                            self.mw.display_info.setItem(n, 0, QtWidgets.QTableWidgetItem(unicode(query_res_fin[0][header])))
                            n += 1
                        else:
                            fin_headers.pop(n-1)
                            continue
                    self.mw.display_info.setVerticalHeaderLabels(fin_headers)
                    self.mw.display_info.setHorizontalHeaderLabels([u''])
                    self.mw.display_info.setColumnWidth(0, 165)
                    # self.mw.display_info.setUpdatesEnabled(0)
                    # self.mw.display_info
            else:
                self.error_login.show()
        self.mw.ui_custom.user_account = user
        self.mw.ui_recom.console.user_account = user
        self.mw.ui_simi.user_account = user

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fake = fakeLogin()
    fake.show()
    app.exec_()