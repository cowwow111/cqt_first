import pygame
from button import Text,Image
from sprite import *


class Storage:
    def __init__(self):

        self.tank = Container(
                              img_name='xiping.jpg',
                              ratio=0.25,
                              liquid=Liquid({'water': 10000}),
                              solid=Solid(),
                              capacity=10000
                              )
        self.round_bottom_flask_1 = Container(
                                              img_name='ydshaoping.jpg',
                                              ratio=1,
                                              liquid=Liquid({}),
                                              solid=Solid(),
                                              capacity=1000
                                              )


class Experiment:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.item = Storage()

    def draw(self,width,height):
        Image('background.png', ratio=1).draw(self.surface, width / 2, height / 2)
        self.item.tank.draw(self.surface,0.2*width,0.2*height)
        self.item.round_bottom_flask_1.draw(self.surface,0.8*width,0.2*height)