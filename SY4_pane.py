# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox
import matplotlib.pyplot as plt
from SY4_ui import Ui_Form


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class SY_4_Pane(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(SY_4_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验4数据处理")


    def processingData(self):
        try:
            result = (0.1456 * eval(self.lineEdit_4.text()) * eval(self.lineEdit_2.text())) / (eval(self.lineEdit_3.text()) * eval(self.lineEdit_1.text()))
            result = round(result, 5)     # 保留5位小数
            self.lineEdit_5.setText(str(result))

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = SY_4_Pane()

    w.show()

    sys.exit(app.exec())