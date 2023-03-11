from PyQt5.QtWidgets import QMessageBox

from login_pane import Login_Pane
from experiment_pane import Experiment_Pane
import sys
from main_win_pane2 import MainWin_Pane
from register_pane import Register_Pane
from SY1_pane import SY_1_Pane
from SY3_pane import SY_3_Pane
from SY4_pane import SY_4_Pane
from SY5_pane import SY_5_Pane
from SY8_pane import SY_8_Pane
from PyQt5.Qt import *
import main1


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_win_pane = MainWin_Pane()
    experiment_pane = Experiment_Pane()
    login_pane = Login_Pane()
    register_pane = Register_Pane()
    sy1_pane = SY_1_Pane()
    sy3_pane = SY_3_Pane()
    sy4_pane = SY_4_Pane()
    sy5_pane = SY_5_Pane()
    sy8_pane = SY_8_Pane()

    main_win_pane.show()


    def show_experiment_pane():
        print("展示实验室安全测试界面")
        login_pane.hide()
        experiment_pane.show()

    # 主界面到登录界面
    def show_login_pane():
        print("展示登录界面")
        login_pane.show()

    # 注册界面回退到登录界面
    def show_login_pane2():
        print("展示登录界面")
        login_pane.show()
        register_pane.hide()

    def show_register_pane():
        print("展示注册界面")
        register_pane.show()
        login_pane.hide()

    def show_simuExp():
        interface = main1.Interface()
        interface.start_interface()


    def show_SY_pane():
        if main_win_pane.comboBox.currentIndex() == 0:
            QMessageBox.about(main_win_pane, "提示", "请先选择实验")
        elif main_win_pane.comboBox.currentIndex() == 1:
            sy1_pane.show()
        elif main_win_pane.comboBox.currentIndex() == 3:
            sy3_pane.show()
        elif main_win_pane.comboBox.currentIndex() == 4:
            sy4_pane.show()
        elif main_win_pane.comboBox.currentIndex() == 5:
            sy5_pane.show()
        elif main_win_pane.comboBox.currentIndex() == 8:
            sy8_pane.show()
        else:
            QMessageBox.about(main_win_pane, "提示", "该实验不用处理数据或功能还未开发")


    # 信号与槽连接
    main_win_pane.show_login_pane_signal.connect(show_login_pane)
    login_pane.show_experiment_pane_signal.connect(show_experiment_pane)
    login_pane.show_register_pane_signal.connect(show_register_pane)
    register_pane.back_signal.connect(show_login_pane2)
    main_win_pane.show_data_process_signal.connect(show_SY_pane)
    main_win_pane.show_simuExp_signal.connect(show_simuExp)

    sys.exit(app.exec())