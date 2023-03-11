# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox
import numpy as np
import math
import matplotlib.pyplot as plt
from SY3_ui import Ui_Form
from scipy import optimize

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class SY_3_Pane(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(SY_3_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验3数据处理")
        self.stackedWidget.setCurrentIndex(0)  # 设置默认页面为第一页

    def set_index0(self):
        self.stackedWidget.setCurrentIndex(0)

    def set_index1(self):
        self.stackedWidget.setCurrentIndex(1)

    # 第一页数据处理
    def pg1_data(self):
        try:
            fi = (eval(self.lineEdit_2.text()) * eval(self.lineEdit_3.text())) / (eval(self.lineEdit_1.text() * eval(self.lineEdit_4.text())))
            result = (eval(self.lineEdit_5.text()) * eval(self.lineEdit_1.text()) * fi * 100) / (eval(self.lineEdit_3.text()) * eval(self.lineEdit_6.text()))
            self.lineEdit_7.setText(str(result))

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")

    # 第二页第一项数据处理
    def pg2_data1(self):
        try:
            def f_1(x, A, B):
                return A * x + B

            plt.figure()
            # 拟合点
            x0 = []  # 将用户输入的数据传给x0和y0
            y0 = []
            page2_left = [self.lineEdit2_1, self.lineEdit2_2, self.lineEdit2_3, self.lineEdit2_4, self.lineEdit2_5]  # 左侧数据
            page2_right = [self.lineEdit2_7, self.lineEdit2_8, self.lineEdit2_9, self.lineEdit2_10, self.lineEdit2_11] # 右侧数据
            for x in page2_left:
                x0.append(float(x.text()))
            for y in page2_right:
                y0.append(float(y.text()))

            # 绘制散点
            # plt.scatter(x0[:], y0[:], 3, "red")
            plt.scatter(x0[:], y0[:], color='red', marker='o')

            # 直线拟合与绘制
            A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]

            global a, b  # 声明a, b为全局变量，供pg2_data2()函数使用
            a, b = A1, B1  # 将拟合的A与B传给全局变量
            x1 = np.arange(0, 0.6, 0.1)  # 0和0.0005对应x0的两个端点，0.00001为步长
            y1 = A1 * x1 + B1
            plt.plot(x1, y1, color="blue")

            # 拟合结果：y=Ax+B, R^2 = xxx
            R2 = self.computeCorrelation(x0, y0)
            plt.title('拟合结果：y=%.3fx + %.3f, R^2=%.8f' % (A1, B1, R2))
            plt.xlabel('氯霉素浓度 mg/L')
            plt.ylabel('峰高')
            plt.show()

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")


    # 第二页第二项数据处理
    def pg2_data2(self):
        try:
            c1 = round((eval(self.lineEdit2_6.text()) - b) / a, 5)  # 保留浓度结果5位小数
            self.lineEdit2_12.setText(str(c1))   # 样品浓度

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")

    # 计算R2值
    def computeCorrelation(self, X, Y):
        xBar = np.mean(X)
        yBar = np.mean(Y)
        SSR = 0
        varX = 0
        varY = 0
        for i in range(0, len(X)):
            diffXXBar = X[i] - xBar
            diffYYBar = Y[i] - yBar
            SSR += (diffXXBar * diffYYBar)
            varX += diffXXBar ** 2
            varY += diffYYBar ** 2

        SST = math.sqrt(varX * varY)
        return abs(SSR / SST)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = SY_3_Pane()

    w.show()

    sys.exit(app.exec())