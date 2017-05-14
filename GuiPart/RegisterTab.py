# coding: utf-8

"""
用户注册
"""
import re
import time
import string
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QApplication,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QSpinBox,
                             QVBoxLayout, QTabWidget, QPushButton, QToolButton, QHBoxLayout,
                             QToolBox, QLCDNumber, QMessageBox, QTextBrowser, QComboBox)
from PyQt5.QtCore import (Qt, QSize, QCoreApplication)
from PyQt5.QtGui import QFont, QPalette
from support.dbOper import dbOper, dct

ADD_CUST = '''
INSERT INTO `platesys`.`customers_info` ( `cust_id`, `user_account`, `user_password`, `regi_time`, `name`, `identity`, `driv_lic`, `briefing`, `plate_num`, `obt_plate_time`, `telephone`, `e_mail`, `purchase_bill_id`, `VIN_code`, `adm_area`, `mailing_address`, `mailing_or_not`, `need_temp_or_not`)
VALUES ( NULL,
         '{user_account}',
         '{user_password}',
         '{regi_time}',
         '{name}',
         '{identity}',
         '{driv_lic}',
         NULL,
         NULL,
         NULL,
         '{telephone}',
         '{e_mail}',
         '{purchase_bill_id}',
         '{VIN_code}',
         '{adm_area}',
         '{mailing_address}',
         '{mailing_or_not}',
         '{need_temp_or_not}' );
'''

protxt = unicode(dct['regi_info']['info'])


class RegisterTab(QDialog):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        account_label = QLabel(u"账号")
        self.account_edit = QLineEdit(u"可包含大小写字母、数字和下划线")
        self.account_edit.tag = 'user_account'
        pwd_label = QLabel(u"密码")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.tag = 'user_password'
        name_label = QLabel(u"姓名")
        self.name_edit = QLineEdit(u"须与身份证信息一致")
        self.name_edit.tag = 'name'
        idcard_label = QLabel(u"身份证")
        self.idcard_edit = QLineEdit()
        self.idcard_edit.tag = 'identity'
        drivlic_label = QLabel(u"驾驶证")
        self.drivlic_edit = QLineEdit()
        self.drivlic_edit.tag = 'driv_lic'
        area_label = QLabel(u"行政区划")
        self.area_edit = QComboBox()
        self.area_edit.tag = 'adm_area'
        self.area_edit.addItems([u"黄浦区",
                                 u"浦东新区",
                                 u"徐汇区",
                                 u"长宁区",
                                 u"静安区",
                                 u"普陀区",
                                 u"虹口区",
                                 u"杨浦区",
                                 u"闵行区",
                                 u"宝山区",
                                 u"嘉定区",
                                 u"金山区",
                                 u"松江区",
                                 u"青浦区",
                                 u"奉贤区",
                                 u"崇明区"])
        vin_label = QLabel(u"车辆识别代号")
        self.vin_edit = QLineEdit()
        self.vin_edit.tag = 'VIN_code'
        bill_label = QLabel(u"购车发票编号")
        self.bill_edit = QLineEdit()
        self.bill_edit.tag = 'purchase_bill_id'
        tele_label = QLabel(u"手机/电话")
        self.tele_edit = QLineEdit()
        self.tele_edit.tag = 'telephone'
        email_label = QLabel(u"E-mail")
        self.email_edit = QLineEdit()
        self.email_edit.tag = 'e_mail'
        self.needtemp_check = QCheckBox(u"是否需要临时号牌")
        self.needtemp_check.tag = 'need_temp_or_not'
        self.ismail_check = QCheckBox(u"是否需要快递（不选择则自取）")
        self.ismail_check.tag = 'mailing_or_not'
        addr_label = QLabel(u"邮寄地址")
        self.addr_edit = QLineEdit()
        self.addr_edit.tag = 'mailing_address'

        self.protoread = QCheckBox(u"请确保您已经认真阅读了《XXXXXX协议》")

        self.submit = QPushButton(u"提交")
        self.submit.setDisabled(1)
        cancel = QPushButton(u"取消")
        # self.submit.clicked.connect(self.login_check)
        proto_text = QTextBrowser()
        proto_text.setText(protxt)

        layout = QGridLayout()
        # layout.addWidget(QLabel(u"新用户注册"), 0, 1, 1, 1)
        layout.addWidget(account_label, 1, 0, 1, 1)
        layout.addWidget(self.account_edit, 1, 1, 1, 1)
        layout.addWidget(pwd_label, 2, 0, 1, 1)
        layout.addWidget(self.pwd_edit, 2, 1, 1, 1)
        layout.addWidget(name_label, 3, 0, 1, 1)
        layout.addWidget(self.name_edit, 3, 1, 1, 1)
        layout.addWidget(idcard_label, 4, 0, 1, 1)
        layout.addWidget(self.idcard_edit, 4, 1, 1, 1)
        layout.addWidget(drivlic_label, 5, 0, 1, 1)
        layout.addWidget(self.drivlic_edit, 5, 1, 1, 1)
        layout.addWidget(area_label, 6, 0, 1, 1)
        layout.addWidget(self.area_edit, 6, 1, 1, 1)
        layout.addWidget(vin_label, 7, 0, 1, 1)
        layout.addWidget(self.vin_edit, 7, 1, 1, 1)
        layout.addWidget(bill_label, 8, 0, 1, 1)
        layout.addWidget(self.bill_edit, 8, 1, 1, 1)
        layout.addWidget(tele_label, 9, 0, 1, 1)
        layout.addWidget(self.tele_edit, 9, 1, 1, 1)
        layout.addWidget(email_label, 10, 0, 1, 1)
        layout.addWidget(self.email_edit, 10, 1, 1, 1)
        layout.addWidget(self.needtemp_check, 11, 0, 1, 2)
        layout.addWidget(self.ismail_check, 12, 0, 1, 2)
        layout.addWidget(addr_label, 13, 0, 1, 1)
        layout.addWidget(self.addr_edit, 13, 1, 1, 1)
        layout.addWidget(self.protoread, 14, 0, 1, 2)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit)
        button_layout.addWidget(cancel)
        layout.addLayout(button_layout, 15, 0, 1, 2)
        layout.addWidget(proto_text, 1, 2, 15, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 6)

        self.resize(800, 480)

        self.setLayout(layout)

        self.addr_edit.setDisabled(1)
        self.ismail_check.clicked.connect(self.addr_state)
        self.protoread.clicked.connect(self.submit_state)
        self.submit.clicked.connect(self.regi_check)
        cancel.clicked.connect(QCoreApplication.instance().quit)

        self.regi_res = QMessageBox()
        self.regi_res.setFont(QFont("Microsoft YaHei UI", 12))
        self.regi_res.setWindowTitle(u":-(")
        self.regi_res.setWindowFlags(Qt.WindowStaysOnTopHint)

    def submit_state(self):
        if self.protoread.isChecked():
            self.submit.setDisabled(0)
        else:
            self.submit.setDisabled(1)

    def addr_state(self):
        if self.ismail_check.isChecked():
            self.addr_edit.setDisabled(0)
        else:
            self.addr_edit.setDisabled(1)

    def regi_check(self):
        res = {}
        for item in [self.account_edit, self.pwd_edit, self.name_edit, self.idcard_edit, self.drivlic_edit,
                     self.area_edit, self.vin_edit, self.bill_edit, self.tele_edit, self.email_edit,
                     self.needtemp_check, self.ismail_check, self.addr_edit]:
            if isinstance(item, QLineEdit):
                if item.isEnabled():
                    if not item.text():
                        self.regi_res.setText(u"每一项均为必填！")
                        break
                    res[item.tag] = item.text().encode('utf-8')
            elif isinstance(item, QCheckBox):
                res[item.tag] = int(item.isChecked())
            elif isinstance(item, QComboBox):
                res[item.tag] = item.currentText().encode('utf-8')
        else:
            try:
                tmp_account = self.account_edit.text()
                assert re.match(r"^[\w\d_]+$", tmp_account) and tmp_account != 'admin', u"账号格式错误，请重新输入"
                if not self.ismail_check.isChecked():
                    res['mailing_address'] = ''
                res['regi_time'] = time.time().__str__()
                # tmp_password = self.pwd_edit.text()
                # assert re.match(r"[\w\d_]*", tmp_password), u"密码格式错误"
            except Exception, e:
                self.regi_res.setText(e.message)
            else:
                exist_query = dbOper().query(
                    '''select * from customers_info where user_account='{user_account}' or identity='{identity}';'''
                    .format(**res))
                if not exist_query:
                    tmp_sql = ADD_CUST.format(**res)
                    dbOper().update(tmp_sql)
                    self.regi_res.setWindowTitle(u":-)")
                    self.regi_res.setText(u"恭喜，注册成功!\n现在可以使用账号 {} 登陆系统".format(tmp_account))
                    self.hide()
                else:
                    self.regi_res.setText(u"用户名/身份证号\n已存在！")
        self.regi_res.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    fake = RegisterTab()
    fake.show()
    app.exec_()
