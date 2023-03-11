import pygame
from button import Image
from sprite import *


class Storage:
    def __init__(self):
        self.tank = Container(
            img_name='xiping.jpg',
            ratio=0.2,
            liquid=Liquid({'water': 10000}),
            solid=Solid(),
            capacity=10000
        )
        self.round_bottom_flask_1 = Container(
            img_name='ydshaoping.jpg',
            ratio=0.4,
            liquid=Liquid({}),
            solid=Solid(),
            capacity=1000
        )
        self.reagent_bottle_1 = Container(
            img_name='shijip.jpg',
            ratio=0.2,
            liquid=Liquid({'acetone': 10000}),
            solid=Solid(),
            capacity=10000
        )
        self.heater1 = Heater(
            img_name='shuiyu.jpg',
            ratio=0.3
        )
        self.timer = Timer(
            8.0,
            Color().BLACK,
            'STXINGKA.TTF',
            60
        )
        self.add_time1 = AddTime(
            1 / 6,
            Color().BLACK,
            'STXINGKA.TTF',
            30
        )
        self.add_time2 = AddTime(
            1 / 3,
            Color().BLACK,
            'STXINGKA.TTF',
            30
        )
        self.add_time3 = AddTime(
            1 / 2,
            Color().BLACK,
            'STXINGKA.TTF',
            30
        )
        self.add_time4 = AddTime(
            1.0,
            Color().BLACK,
            'STXINGKA.TTF',
            30
        )
        self.reset_button = ButtonText(
            'reset',
            Color().BLACK,
            'STXINGKA.TTF',
            40
        )
        self.confirm_button = ButtonText(
            'confirm',
            Color().BLACK,
            'STXINGKA.TTF',
            40
        )
        self.heater_group = [self.heater1]
        self.add_time_group = [self.add_time1, self.add_time2, self.add_time3, self.add_time4]
        self.group1 = [self.tank, self.round_bottom_flask_1, self.reagent_bottle_1]


class Experiment:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.item = Storage()
        self.time = self.item.timer.time

    def draw(self, width, height):
        Image('background.png', ratio=1).draw(self.surface, width / 2, height / 2)
        self.item.heater1.draw(self.surface, 0.5 * width, 0.7 * height)
        self.item.heater1.information()
        self.item.tank.draw(self.surface, 0.2 * width, 0.7 * height)
        self.item.tank.information('水')
        self.item.round_bottom_flask_1.draw(self.surface, 0.8 * width, 0.7 * height)
        self.item.round_bottom_flask_1.information(' ')
        self.item.reagent_bottle_1.draw(self.surface, 0.2 * width, 0.5 * height)
        self.item.reagent_bottle_1.information('丙酮')
        self.item.timer.draw(self.surface, 0.5 * width, 0.05 * height)
        self.item.reset_button.draw(self.surface, 0.2 * width, 0.05 * height)
        self.item.add_time1.draw(self.surface, 0.3 * width, 0.05 * height)
        self.item.add_time2.draw(self.surface, 0.4 * width, 0.05 * height)
        self.item.add_time3.draw(self.surface, 0.6 * width, 0.05 * height)
        self.item.add_time4.draw(self.surface, 0.7 * width, 0.05 * height)
        self.item.confirm_button.draw(self.surface, 0.8 * width, 0.05 * height)

    def hold(self):
        holding = 0
        for i in self.item.group1:
            if i.handle_event() and holding == 0:
                i.moving_code = 1
                i.package_code = 0

    def unhold(self):
        for i in self.item.heater_group:
            i.package([self.item.round_bottom_flask_1])
        for i in self.item.group1:
            if i.moving_code == 1:
                i.moving_code = 0

    def timeManage(self):
        for i in self.item.add_time_group:
            if i.handle_event():
                self.item.timer.time += i.delta_time
                self.item.timer.update()
        if self.item.reset_button.handle_event():
            self.item.timer.reset()
        if self.item.confirm_button.handle_event():
            self.item.timer.confirm()
            self.time = self.item.timer.time
            self.rule()

    def rule(self):
        rbf = self.item.round_bottom_flask_1
        if rbf.liquid.component.get('water') == 100 and rbf.liquid.component.get(
                'acetone') == 200 and self.time - rbf.reaction_start >= 2.0 and (73 > rbf.temp > 67):
            rbf.react([{'A': 200}, {}], self.time)

    def run(self, width, height):
        for i in self.item.heater_group:
            i.tempControl()
        time = self.item.timer.time
        self.item.tank.output([self.item.round_bottom_flask_1], time)
        self.item.reagent_bottle_1.output([self.item.round_bottom_flask_1], time)
        self.draw(width, height)
