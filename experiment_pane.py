import random
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from experiment_ui import Ui_widget
import quiz_list

class Experiment_Pane(QWidget, Ui_widget):
    def __init__(self, parent=None, *args, **kwargs):
        super(Experiment_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("实验室安全练习题")

        self.optionlist = [self.radioButton_A, self.radioButton_B, self.radioButton_C, self.radioButton_D]   # 将选项放进一个列表里
        self.quiz_num = []  # 创建抽取的题目号的空列表 0~99
        self.quiz_box = []   # 创建用于存储抽取的题目的空列表
        self.Extract_Quiz()
        self.count = 0  # 记录题目数量
        self.Set_Text()



        self.submit_answer_btn.setText("提交答案")
        self.last_quiz_btn.setText("上一题")
        self.next_quiz_btn.setText("下一题")

        # 按钮信号
        self.option = None      # 初始化选项为空
        self.radioButton_A.toggled.connect(self.opA)
        self.radioButton_B.toggled.connect(self.opB)
        self.radioButton_C.toggled.connect(self.opC)
        self.radioButton_D.toggled.connect(self.opD)
        self.submit_answer_btn.clicked.connect(self.Submit_Answer)
        self.next_quiz_btn.clicked.connect(self.Next_Quiz)
        self.last_quiz_btn.clicked.connect(self.Last_Quiz)



    def opA(self):
        self.option = 1  # 选A
    def opB(self):
        self.option = 2  # 选B
    def opC(self):
        self.option = 3  # 选C
    def opD(self):
        self.option = 4  # 选D

    # 提交答案判定
    def Submit_Answer(self):
        try:
            if self.option is not None:
                if self.option == quiz_list.answer[self.quiz_num[self.count]]:
                    QMessageBox.about(self, "提示", '回答正确')
                else:
                    QMessageBox.about(self, "提示", "回答错误，正确答案为第{}个".format(quiz_list.answer[self.quiz_num[self.count]]))
            else:
                QMessageBox.about(self, "提示", "请选择一个选项")

            for i in self.optionlist:      # 重置radiobutton选中状态
                i.setCheckable(False)
                i.setCheckable(True)
            self.option = None

        except Exception as e:
            print(e)

    def Extract_Quiz(self):        # 从题库中随机抽取10道题目
        for q in range(10):
            self.quiz_num.append(random.randint(0, len(quiz_list.answer) - 1))   #  len(quiz_list.answer) 长度为比索引值多1
        for num in self.quiz_num:   # num为str类
            self.quiz_box.append(quiz_list.str_test[int(num)])   # 将题目号对应的题目放入 quiz_box
        # print(self.quiz_box)

    def Set_Text(self):           # 显示抽取的题目
        self.quiz_text.setText(str("{}、".format(self.count + 1)) + self.quiz_box[self.count][0])
        self.radioButton_A.setText(self.quiz_box[self.count][1])
        self.radioButton_B.setText(self.quiz_box[self.count][2])
        self.radioButton_C.setText(self.quiz_box[self.count][3])
        self.radioButton_D.setText(self.quiz_box[self.count][4])

    def Next_Quiz(self):         # 切换至下一题
        if self.count < 9:       # 存储在quiz_box 中的题目数索引值为0~9
            self.count += 1
            self.Set_Text()
        else:
            QMessageBox.about(self, "提示", "每次限做10道题哦~~")

    def Last_Quiz(self):
        if self.count > 0:
            self.count -= 1
            self.Set_Text()
        else:
            QMessageBox.about(self, "提示", "已经是第一道题了!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Experiment_Pane()

    w.show()


    sys.exit(app.exec())
