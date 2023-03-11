# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox
import numpy as np
import math
import matplotlib.pyplot as plt
from SY1_ui import Ui_Form
from scipy import optimize

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class SY_1_Pane(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(SY_1_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验1数据处理")
        self.stackedWidget.setCurrentIndex(0)  # 设置默认页面为第一页

        # 将填空类 lineEdit进行分类
        self.page1_left = [self.lineEdit1_1, self.lineEdit1_2, self.lineEdit1_3, self.lineEdit1_4, self.lineEdit1_5]
        self.page1_right = [self.lineEdit1_7, self.lineEdit1_8, self.lineEdit1_9, self.lineEdit1_10, self.lineEdit1_11]

        self.page2_left = [self.lineEdit2_1, self.lineEdit2_2, self.lineEdit2_3, self.lineEdit2_4, self.lineEdit2_5, self.lineEdit2_6]
        self.page2_right = [self.lineEdit2_7, self.lineEdit2_8, self.lineEdit2_9, self.lineEdit2_10, self.lineEdit2_11, self.lineEdit2_12]

        self.page3_left = [self.lineEdit3_1, self.lineEdit3_2, self.lineEdit3_3, self.lineEdit3_4, self.lineEdit3_5, self.lineEdit3_6]
        self.page3_right = [self.lineEdit3_7, self.lineEdit3_8, self.lineEdit3_9, self.lineEdit3_10, self.lineEdit3_11, self.lineEdit3_12]


    # ===============================================数据处理模块=========================================================

    # 第一页数据处理
    def pg1_data(self):
        try:
            # 左侧
            y_ls = []
            s1 = 0
            for y in self.page1_left:
                if y.text() != '':
                    y_ls.append(float(y.text()))
                    s1 += float(y.text())
                else:
                    s1 += 0
                a1 = round(float(s1 / len(y_ls)), 3)  # 保留3位小数
                self.lineEdit1_6.setText(str(a1))
            # 右侧函数
            for text in self.page1_right:    # 清除右侧文本
                text.clear()

            x_ls = []
            s2 = 0
            for i in range(0, 5):
                if self.page1_left[i].text() != '':
                    x_ls.append((float(self.page1_left[i].text()) - 0.0025) / 0.0275)
                else:
                    x_ls.append(0)  # 用0代替空输入，加入x_ls列表中
            for x, data in zip(self.page1_right, x_ls):
                if data != 0:
                    x.setText(str(round(data, 3)))
                    s2 += data
                else:
                    s2 += 0
            a2 = round(s2 / len(y_ls), 3)
            self.lineEdit1_12.setText(str(a2))

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")

    # 第二页数据处理
    def pg2_data(self):
        try:
            def f_1(x, A, B):
                return A * x + B

            plt.figure()
            # 拟合点
            x0 = []  # 将用户输入的数据传给x0和y0
            y0 = []
            for x in self.page2_left:
                x0.append(float(x.text()))
            for y in self.page2_right:
                y0.append(float(y.text()))

            # 绘制散点
            # plt.scatter(x0[:], y0[:], 3, "red")
            plt.scatter(x0[:], y0[:], color='red', marker='o')

            # 直线拟合与绘制
            A1, B1 = optimize.curve_fit(f_1, x0, y0)[0]
            x1 = np.arange(0, 0.0005, 0.00001)  # 0和0.0005对应x0的两个端点，0.00001为步长
            y1 = A1 * x1 + B1
            plt.plot(x1, y1, color="blue")

            # 拟合结果：y=Ax+B, R^2 = xxx
            R2 = self.computeCorrelation(x0, y0)
            plt.title('拟合结果：y=%.3fx + %.3f, R^2=%.8f' % (A1, B1, R2))
            plt.xlabel('DPA mol/L')
            plt.ylabel('吸光度')
            plt.show()

        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示", "请检查你的输入")

    # 第三页数据处理
    def pg3_data(self):
        try:
            x0 = []
            for x in self.page3_left:
                x0.append(int(x.text()))
            y0 = []
            for y in self.page3_right:
                y0.append(int(y.text()))

            z1 = np.polyfit(x0, y0, int(self.spinBox.text()))  # 用 int(self.spinBox.text())=0——8 次多项式拟合
            p1 = np.poly1d(z1)
            print(p1)  # 在屏幕上打印拟合多项式

            yvals = p1(x0)  # 也可以使用yvals=np.polyval(z1,x)
            plt.plot(x0, y0, marker='o', label='原始数据')
            plt.plot(x0, yvals, color='r', label='拟合曲线')
            plt.xlabel('照射时间')
            plt.ylabel('吸光度变化值')
            plt.legend(loc=1)    # 指定legend的位置

            plt.title("拟合结果")
            plt.show()

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

    # =============================================数据处理模块结束========================================================


    # 绑定换页按键与槽
    def set_index0(self):
        self.label_index.setText("-------------------------------------------样品含量测定-------------------------------------------")
        self.stackedWidget.setCurrentIndex(0)

    def set_index1(self):
        self.label_index.setText("----------------------------------------单线态氧标准曲线的绘制----------------------------------------")
        self.stackedWidget.setCurrentIndex(1)

    def set_index2(self):
        self.label_index.setText("----------------------------------------样品单线态氧含量的测定----------------------------------------")
        self.stackedWidget.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = SY_1_Pane()

    w.show()

    sys.exit(app.exec())