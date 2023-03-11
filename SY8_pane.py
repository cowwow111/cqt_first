# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox
import numpy as np
import matplotlib.pyplot as plt
from SY8_ui import Ui_Form


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class SY_8_Pane(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(SY_8_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验8数据处理")

    def processingData(self):
        try:
            left = [self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5,
                    self.lineEdit_6, self.lineEdit_7, self.lineEdit_8, self.lineEdit_9, self.lineEdit_10]
            right = [self.lineEdit_11, self.lineEdit_12, self.lineEdit_13, self.lineEdit_14, self.lineEdit_15,
                     self.lineEdit_16, self.lineEdit_17, self.lineEdit_18, self.lineEdit_19, self.lineEdit_20]
            x0 = []
            for x in left:
                x0.append(eval(x.text()))
            x0.sort()       # 保证列表中的数由小到大排列，绘图不出错

            y0 = []
            for y in right:
                y0.append(eval(y.text()))
            y0.sort()
            print(x0)
            print(y0)

            z1 = np.polyfit(x0, y0, int(self.spinBox.text()))  # 用 int(self.spinBox.text())=0——8 次多项式拟合
            p1 = np.poly1d(z1)
            print(p1)  # 在屏幕上打印拟合多项式

            # yvals = p1(x0)  # 也可以使用yvals=np.polyval(z1,x)
            plt.plot(x0, y0, marker='o', label='原始数据')
            # plt.plot(x0, yvals, color='r', label='拟合曲线')
            plt.xlabel('相对湿度')
            plt.ylabel('重量差值')
            plt.legend(loc=1)    # 指定legend的位置

            plt.title("样品对湿度的耐受程度")
            plt.show()

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = SY_8_Pane()

    w.show()

    sys.exit(app.exec())