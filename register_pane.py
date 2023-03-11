import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from register_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal




class Register_Pane(QWidget, Ui_Form):
    back_signal = pyqtSignal()
    register_account_password_signal = pyqtSignal(str, str)

    def __init__(self, parent=None, *args, **kwargs):
        super(Register_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("注册")

        self.animation_targets = [self.about_btn, self.clear_btn, self.back_btn]
        self.animation_targets_pos = [target.pos() for target in self.animation_targets]

    # 菜单按钮功能
    def show_hide_menu(self, checked):
        print("显示和隐藏", checked)

        animation_group = QSequentialAnimationGroup(self)
        for idx, target in enumerate(self.animation_targets):

            animation = QPropertyAnimation()
            animation.setTargetObject(target)
            animation.setPropertyName(b"pos")
            if not checked:  # 展开动画
                animation.setStartValue(self.main_menu_btn.pos())
                animation.setEndValue(self.animation_targets_pos[idx])
            else:  # 收回动画
                animation.setEndValue(self.main_menu_btn.pos())
                animation.setStartValue(self.animation_targets_pos[idx])
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.InOutBounce)
            animation_group.addAnimation(animation)

        animation_group.start(QAbstractAnimation.DeleteWhenStopped)

    # 关于按钮功能
    def about(self):
        print("关于")
        QMessageBox.about(self, "联系方式", "微信号:liquidator61")

    # 返回按钮功能
    def back(self):
        self.back_signal.emit()

    # 清除按钮功能
    def clear(self):
        print("清除")
        self.account_edit.clear()
        self.password_edit.clear()
        self.confirm_edit.clear()


    # 检测账户是否已经存在，若不存在正常注册
    def check_register(self):
        user = self.account_edit.text()
        pwd = self.password_edit.text()
        is_exist = user_exist(user)
        if is_exist:
            QMessageBox.about(self, "提示", "账户已存在！")
        else:
            if add_account(user, pwd):
                QMessageBox.about(self, "提示", "注册成功")
            else:
                QMessageBox.about(self, "提示", "注册失败")



    # 检测确认密码是否一致，不一致注册按钮不亮
    def enable_register_btn(self):
        print("判定")
        account_txt = self.account_edit.text()
        password_txt = self.password_edit.text()
        confirm_txt = self.confirm_edit.text()

        if len(account_txt) > 0 and len(password_txt) > 0 and len(confirm_txt) > 0 and password_txt == confirm_txt:
            self.register_btn.setEnabled(True)

        else:
            self.register_btn.setEnabled(False)



# 注册功能--------------------------------------------------------------------------------------
def user_exist(username):
    """
    检测用户名是否存在
    :param username:要检测的用户名
    :return: True：用户名存在；False：用户名不存在
    """
    # 一行一行的去查找，如果用户名存在，return True：False
    try:
        with open("users", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                line_new = line.split("$")
                if line_new[0] == username:
                    return True
            return False
    except IOError:
        return False


def add_account(username, password):
    """
    注册用户
    1、打开文件
    2、用户名$密码
    :param username:用户名
    :param password:密码
    :return:True：注册成功；
    """
    with open("users", "a", encoding="utf-8") as f:
        temp = "\n" + username + "$" + password
        f.write(temp)
        return True
# 注册功能结束----------------------------------------------------------------------------------




if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Register_Pane()
    w.back_signal.connect(lambda: print("返回"))
    w.register_account_password_signal.connect(lambda a, p: print(a, p))
    w.show()

    sys.exit(app.exec())
