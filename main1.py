import sys

import pygame

import main_win_pane2
import settings as st
from button import *
from menu import Menu
from stage import exp1, exp2


class Interface:
    def __init__(self):
        pygame.init()
        self.basic_background()
        self.width, self.height = self.size
        self.clock = pygame.time.Clock()
        self.exp_list = [exp1, exp2]

    def basic_background(self):
        """
        <基本背景><basic_background>\n
        返回值为背景尺寸和背景表面
        """
        # 设置logo和界面标题
        pygame.display.set_icon(st.game_icon)
        pygame.display.set_caption(st.game_caption)

        # 设置开始界面
        self.size = width, height = 1920 * st.show_ratio, 1080 * st.show_ratio
        self.screen = pygame.display.set_mode((int(width), int(height)))

    def start_interface(self):
        menu = Menu(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.left_button.handle_event():
                        menu.exp_down()
                    if menu.right_button.handle_event():
                        menu.exp_up()
                    if menu.start_button.handle_event():
                        self.exp_interface(menu.experiment_index)
            menu.run(self.width, self.height)
            pygame.display.update()

    def exp_interface(self, exp_index):
        target_exp = self.exp_list[exp_index]
        exp = target_exp.Experiment()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    exp.hold()
                    exp.timeManage()
                elif event.type == pygame.MOUSEBUTTONUP:
                    exp.unhold()

            exp.run(self.width, self.height)
            pygame.display.update()


if __name__ == '__main__':
    interface = Interface()
    interface.start_interface()
