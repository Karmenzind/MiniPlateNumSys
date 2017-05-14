# coding: utf-8
"""
管理员页面
展示所有库存信息
"""
import re
import time
import string
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDialogButtonBox, QApplication,
                             QGridLayout, QLabel, QLineEdit, QMessageBox, QSpinBox,
                             QVBoxLayout, QTabWidget, QPushButton, QToolButton, QHBoxLayout,
                             QToolBox, QLCDNumber, QMessageBox, QTextBrowser, QComboBox, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import (Qt, QSize, QCoreApplication)
from PyQt5.QtGui import QFont, QPalette
from support.dbOper import dbOper

ACQUIRE = '''select `regi_time` as regi_time, `name`, `identity`, `driv_lic`, `briefing`, `plate_num`, `obt_plate_time` as obt_plate_time, `telephone`, `e_mail`, `purchase_bill_id`, `VIN_code`, `adm_area`, `mailing_address`, `mailing_or_not`, `need_temp_or_not` from customers_info;'''


class AdminWin(QDialog):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        titles = [u'obt_plate_time', u'name', u'VIN_code', u'mailing_address', u'e_mail', u'telephone',
                  u'need_temp_or_not', u'briefing', u'plate_num', u'identity', u'regi_time', u'adm_area',
                  u'mailing_or_not', u'driv_lic', u'purchase_bill_id']
        title_values = [u"定号时间", u"姓名", u"车辆识别编号", u"邮寄地址", u"电子邮箱", u"电话", u"需要临时牌照", u"其他信息", u"车牌号", u"身份证", u"注册时间",
                        u"行政区划", u"是否邮寄", u"驾驶证", u"购车发票编号"]
        info_table = QTableWidget()
        info_table.setColumnCount(len(titles))
        info_table.setHorizontalHeaderLabels(title_values)
        query_res = dbOper().query(ACQUIRE)
        for row, item in enumerate(query_res):
            info_table.insertRow(row)
            for col, key in enumerate(titles):
                tmp_item = QTableWidgetItem(unicode(item[key]))
                info_table.setItem(row, col, tmp_item)

        info_table.resizeColumnsToContents()
        layout = QGridLayout()
        layout.addWidget(info_table, 0, 0)
        self.setLayout(layout)
        self.setWindowTitle(u"当前系统注册用户信息")
        self.resize(1000, 618)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    lg = AdminWin()
    lg.show()
    app.exec_()
