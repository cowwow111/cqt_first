# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox
import numpy as np
import math
import matplotlib.pyplot as plt
from SY5_ui import Ui_Form
from scipy import optimize

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class SY_5_Pane(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(SY_5_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验5数据处理")


    def processingData1(self):
        try:
            def f_1(x, A, B):
                return A * x + B

            plt.figure()
            # 拟合点
            x0 = []  # 将用户输入的数据传给x0和y0
            y0 = []
            left = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5]  # 左侧数据
            right = [self.lineEdit_6, self.lineEdit_7, self.lineEdit_8, self.lineEdit_9, self.lineEdit_10]  # 右侧数据
            for x in left:
                x0.append(float(x.text()))
            for y in right:
                y0.append(float(y.text()))

            # 绘制散点
            # plt.scatter(x0[:], y0[:], 3, "red")
            plt.scatter(x0[:], y0[:], color='red', marker='o')

            # 直线拟合与绘制
            A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]

            global a, b   # 声明a, b为全局变量，传给processingData2()使用
            a, b = A1, B1
            x1 = np.arange(0, 0.024, 0.004)  # 0和0.0005对应x0的两个端点，0.00001为步长
            y1 = A1 * x1 + B1
            plt.plot(x1, y1, color="blue")

            # 拟合结果：y=Ax+B, R^2 = xxx
            R2 = self.computeCorrelation(x0, y0)
            plt.title('拟合结果：y=%.3fx + %.3f, R^2=%.8f' % (A1, B1, R2))
            plt.xlabel('胆红素浓度 mg/ml')
            plt.ylabel('吸光度')
            plt.show()

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")

    def processingData2(self):
        try:
            c1 = (eval(self.lineEdit_12.text()) - b) / a
            result = round(c1 * 25000 / 3, 3)      # 样品胆红素百分含量 = 10c1/1000 * 50/3 * 50/10 * 1/0.01 * 100%, 结果保留3位小数
            self.lineEdit_13.setText(str(result))

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

    w = SY_5_Pane()

    w.show()

    sys.exit(app.exec())