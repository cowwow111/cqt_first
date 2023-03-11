import pygame
import settings as st
from button import ButtonImage, Text, Color, ButtonText,Image


class Menu:
    def __init__(self, screen):
        self.display_surface = pygame.display.get_surface()
        self.experiment_index = 0
        self.component()

    def component(self):
        self.title_label = Text('制药工程实验模拟',
                                text_color=Color().BLACK,
                                font_type='STXINGKA.TTF',
                                font_size=50)
        self.left_button = ButtonImage('la.png', ratio=0.1)
        self.right_button = ButtonImage('ra.png', ratio=0.1)
        self.label0 = Text('请选择实验',
                           text_color=Color().BLACK,
                           font_type='STXINGKA.TTF',
                           font_size=20)
        self.start_button = ButtonText('开始模拟',
                                       text_color=Color().WHITE,
                                       font_type='STXINGKA.TTF',
                                       font_size=40)

    def draw(self, width, height):
        Image('background.png', ratio=1).draw(self.display_surface, width / 2, height / 2)
        self.title_label.draw(self.display_surface, 0.5 * width, 0.15 * height)
        self.experiment_label = Text(text=st.experimentLabelList[self.experiment_index],
                                     text_color=Color().BLACK,
                                     font_type='STXINGKA.TTF',
                                     font_size=32)
        self.left_button.draw(self.display_surface, 0.2 * width, 1 / 3 * height)
        self.right_button.draw(self.display_surface, 0.8 * width, 1 / 3 * height)
        self.experiment_label.draw(self.display_surface, 0.5 * width, 1 / 3 * height)
        self.label0.draw(self.display_surface, 0.5 * width, 0.5 * height)
        self.start_button.draw(self.display_surface, 0.5 * width, 2 / 3 * height)

    def run(self, width, height):
        self.draw(width, height)

    def exp_up(self):
        if self.experiment_index < (len(st.experimentLabelList) - 1):
            self.experiment_index += 1

    def exp_down(self):
        if self.experiment_index > 0:
            self.experiment_index -= 1

    def test(self):
        print(1)
