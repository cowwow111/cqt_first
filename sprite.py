import pygame

from button import *
import math


class Exptools(ButtonImage):
    def __init__(self, img_name, ratio):
        super().__init__(img_name, ratio)
        self.surface = pygame.display.get_surface()
        self.moving_code = 0
        self.collided_code = 0
        self.package_code = 0

    def draw(self, surface: pygame.Surface, center_x, center_y):
        pos = pygame.mouse.get_pos()
        if self.package_code == 0:
            if self.moving_code == 0:
                super().draw(surface, center_x, center_y)
            if self.moving_code == 1:
                super().draw(surface, pos[0], pos[1])
                self.position = pos
        elif self.package_code == 1:
            if self.moving_code == 0:
                super().draw(surface, self.position[0], self.position[1])
            if self.moving_code == 1:
                super().draw(surface, pos[0], pos[1])
                self.position = pos


class Heater(ButtonImage):
    def __init__(self, img_name, ratio, temp=25):
        super().__init__(img_name, ratio)
        self.surface = pygame.display.get_surface()
        self.temp = temp

    def package(self, package_list: list):
        index = self.rect.collidelist(package_list)
        if index == -1:
            self.package_code = 0
        else:
            package_obj = package_list[index]
            package_obj.package_code = 1
            package_obj.temp = self.temp

    def tempControl(self):
        keys = pygame.key.get_pressed()
        if self.handle_event():
            if keys[pygame.K_z]:
                self.temp -= 1
            if keys[pygame.K_c]:
                self.temp += 1

    def information(self):
        text_num = Text(text=str(self.temp)+'℃',
                        text_color=Color().BLACK,
                        font_type='STXINGKA.TTF',
                        font_size=30)
        text_num.draw(self.surface, self.rect.center[0], self.rect.center[1])


class Liquid:
    def __init__(self, component: dict = None, ph: float = 7.0):
        """
        component: {组分名：数量}
        ph: 水溶液ph值
        """
        if component is None:
            component = {}
        self.component = component
        self.ph = ph
        self.amount = 0
        self.update_amount()

    def update_amount(self):
        amount = 0
        for i in self.component.values():
            amount += i
        self.amount = amount


class Solid:
    def __init__(self, component: dict = None):
        """
        component: {组分名：数量}
        """
        if component is None:
            component = {}
        self.component = component
        self.amount = 0
        self.update_amount()

    def update_amount(self):
        amount = 0
        for i in self.component.values():
            amount += i
        self.amount = amount


class Container(Exptools):
    def __init__(self, img_name, ratio, liquid: Liquid, solid: Solid, capacity=500, temp=25):
        super().__init__(img_name, ratio)
        self.reaction_start = None
        self.capacity = capacity
        self.liquid = liquid
        self.solid = solid
        self.temp = temp
        self.space = 0
        self.update(None)

    def update(self, time):
        self.liquid.update_amount()
        self.space = self.capacity - self.liquid.amount
        self.reaction_start = time

    def react(self, output: list, time):
        """
        改变属性为output:第一项为液相，第二项为固相
        """
        self.liquid = Liquid(output[0])
        self.solid = Solid(output[1])
        self.update(time)

    def output(self, output_list: list, time):
        index = self.rect.collidelist(output_list)
        if index == -1:
            self.collided_code = 0
        if self.moving_code == 1 and index != (-1) and self.collided_code == 0:
            collide_obj = output_list[index]
            if collide_obj.space >= 100 and self.liquid.amount >= 100:
                amount = 100
                for key in self.liquid.component.keys():
                    delta_liq = self.liquid.component[key] / self.liquid.amount * amount
                    self.liquid.component[key] -= delta_liq
                    if key in collide_obj.liquid.component:
                        collide_obj.liquid.component[key] += delta_liq
                    else:
                        collide_obj.liquid.component[key] = delta_liq
                self.update(time)
                collide_obj.update(time)
                self.collided_code = 1

            elif collide_obj.space >= 100 and self.liquid.amount > 0:
                amount = self.liquid.amount
                for key in self.liquid.component.keys():
                    delta_liq = self.liquid.component[key] / self.liquid.amount * amount
                    self.liquid.component[key] -= delta_liq
                    if key in collide_obj.liquid.component:
                        collide_obj.liquid.component[key] += delta_liq
                    else:
                        collide_obj.liquid.component[key] = delta_liq
                self.update(time)
                collide_obj.update(time)
                self.collided_code = 1

            elif collide_obj.space < 100 and self.liquid.amount >= collide_obj.space:
                amount = collide_obj.space
                for key in self.liquid.component.keys():
                    delta_liq = self.liquid.component[key] / self.liquid.amount * amount
                    self.liquid.component[key] -= delta_liq
                    if key in collide_obj.liquid.component:
                        collide_obj.liquid.component[key] += delta_liq
                    else:
                        collide_obj.liquid.component[key] = delta_liq
                self.update(time)
                collide_obj.update(time)
                self.collided_code = 1

            elif self.liquid.amount == 0 and self.solid is not {}:
                for key in self.solid.component.keys():
                    delta_sol = self.solid.component[key]
                    self.solid.component[key] -= delta_sol
                    if key in collide_obj.solid.component:
                        collide_obj.solid.component[key] += delta_sol
                    else:
                        collide_obj.solid.component[key] = delta_sol

    def information(self, name: str):
        text_num = Text(text=str(self.liquid.amount),
                        text_color=Color().BLACK,
                        font_type='STXINGKA.TTF',
                        font_size=30)
        text_name = Text(text=name,
                         text_color=Color().BLACK,
                         font_type='STXINGKA.TTF',
                         font_size=30
                         )
        text_name.draw(self.surface, self.rect.center[0], self.rect.center[1] - 35)
        text_num.draw(self.surface, self.rect.center[0], self.rect.center[1])


class Timer(Text):
    def __init__(self, time: float, text_color, font_type, font_size):
        self.time = time
        self.init_time = self.time
        self.time_to_text()
        super().__init__(self.text, text_color, font_type, font_size)

    def time_to_text(self):
        hour = math.floor(self.time)
        minute = int((self.time - hour) * 60)

        if minute < 10:
            minute_text = '0' + str(minute)
        else:
            minute_text = str(minute)

        if hour < 10:
            hour_text = '0' + str(hour)
        else:
            hour_text = str(hour)
        self.text = hour_text + ':' + minute_text

    def update(self):
        self.time_to_text()

    def reset(self):
        self.time = self.init_time
        self.update()

    def confirm(self):
        self.init_time = self.time
        print(self.init_time)


class AddTime(ButtonText):
    def __init__(self, delta_time, text_color, font_type, font_size):
        self.text = '+' + str(delta_time * 60) + 'min'
        super().__init__(self.text, text_color, font_type, font_size)
        self.delta_time = delta_time
