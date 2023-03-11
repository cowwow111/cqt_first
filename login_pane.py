import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from login_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal


class Login_Pane(QWidget, Ui_Form):

    show_register_pane_signal = pyqtSignal()
    show_experiment_pane_signal = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Login_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("登录")

    def register_acc(self):
        print("注册账号")
        self.show_register_pane_signal.emit()

    def show_experiment_pane(self):
        user_name = self.lineEdit.text()
        pwd = self.lineEdit_2.text()
        if user_name != '' and pwd != '':
            if login(user_name, pwd):
                print("登录成功")
                self.show_experiment_pane_signal.emit()
            else:
                QMessageBox.about(self, "提示", "账号或密码不正确！")
        else:
            QMessageBox.about(self, "提示", "请输入账号密码")


    def show_register_pane(self):
        print("弹出注册界面")
        self.show_register_pane_signal.emit()


# 登录功能----------------------------------------------------------------------------------------------
def login(username, password):
    """
    用于用户名和密码的验证
    :param username:用户名
    :param password:密码
    :return:True,用户验证成功；False，用户验证失败
    """
    try:
        f = open("users", "r", encoding="utf-8")
        for line in f:
            line = line.strip()  # 清除换行符
            # 无参数时移除两侧空格，换行符
            # 有参数时移除两侧指定的字符
            line_list = line.split("$")
            if line_list[0] == username and line_list[1] == password:
                # print("成功")
                return True
        return False
    except IOError:
        return False
# 登录功能结束---------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)


    w = Login_Pane()

    w.show()


    sys.exit(app.exec())
