import os
from PyQt5.QAxContainer import QAxWidget
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton, QDesktopWidget
from main_win2_ui import Ui_Form
import experiment_list
import sys
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal, Qt



class MainWin_Pane(QWidget, Ui_Form):

    show_login_pane_signal = pyqtSignal()
    show_data_process_signal = pyqtSignal()
    show_simuExp_signal = pyqtSignal()


    def __init__(self, parent=None, *args, **kwargs):
        super(MainWin_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.axWidget = QAxWidget(self)
        self.verticalLayout_2.addWidget(self.axWidget)
        self.setWindowTitle("制药实验小帮手")

        self.move_to_center()  # 窗口居中显示
        self.add_ex()   # 添加实验并显示
        self.comboBox.currentTextChanged.connect(self.choose_ex)

    def add_ex(self):   # ex = experiment
        self.comboBox.addItem("请选择实验(如果页面过大或过小，可通过‘ctrl + 鼠标滚轮’调整大小)")  # 添加默认item
        for ex in experiment_list.ex_ls:
            self.comboBox.addItem(ex)


    def choose_ex(self):   # ex = experiment
        if self.comboBox.currentIndex() == 0:   # 默认选项时显示空白页
            pass
        else:
            return self.onOpenFile("./resource/专业实验/experiment{}.docx".format(self.comboBox.currentIndex()))


    def onOpenFile(self, path):
        relative_path = path  # 该文件相对路径
        path = os.path.abspath(relative_path)  # 获取该文件的绝对路径
        return self.openOffice(path, 'Word.Application')


    def openOffice(self, path, app):
        self.axWidget.clear()
        if not self.axWidget.setControl(app):
            return QMessageBox.critical(self, '错误', '没有安装  %s' % app)
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)
        self.axWidget.show()
        print(path)


    # def openPdf(self, path):
    #     self.axWidget.clear()
    #     if not self.axWidget.setControl('Adobe PDF Reader'):
    #         return QMessageBox.critical(self, '错误', '没有安装 Adobe PDF Reader')
    #     # self.axWidget.setControl("{233C1507-6A77-46A4-9443-F871F945D258}")
    #     self.axWidget.dynamicCall(
    #         'SetVisible (bool Visible)', 'false')  # 不显示窗体
    #     self.axWidget.setProperty('DisplayAlerts', False)
    #     self.axWidget.setControl(path)
    #     self.axWidget.show()

    # 移除AxWidget插件
    def closeEvent(self, event):
        self.axWidget.close()
        self.axWidget.clear()
        self.layout().removeWidget(self.axWidget)
        del self.axWidget
        super(MainWin_Pane, self).closeEvent(event)


    def move_to_center(self):
        center_pointer = QDesktopWidget().availableGeometry().center()
        x = center_pointer.x()
        y = center_pointer.y()
        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(x - width / 2, y - height / 2)


    def show_login_pane(self):
        self.show_login_pane_signal.emit()


    def show_data_process(self):
        self.show_data_process_signal.emit()

    def about_us(self):
        QMessageBox.about(self, "提示", "本程序由2022SRP制药组制作")

    def show_simuExp(self):
        self.show_simuExp_signal.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)


    w = MainWin_Pane()

    w.show()


    sys.exit(app.exec())


