import pygame as pg


class Plane(object):

    def __init__(self, plane_image_path):
        self.screen = pg.display.get_surface()
        self.window_width, self.window_height = self.screen.get_size()
        # 飞机的正常图
        self.plane = pg.image.load(plane_image_path)
        # 飞机的初始位置
        self.plane_x = None
        self.plane_y = None

    def non_shooting_state(self, plane_image_path):
        self.plane = pg.image.load(plane_image_path)

    def shooting_state(self, plane_image_path, shoot_music):
        self.plane = pg.image.load(plane_image_path)
        shoot_music.play()

    def set_init_position(self, x, y):
        self.plane_x = x
        self.plane_y = y

    @property
    def x(self):
        return self.plane_x

    @property
    def y(self):
        return self.plane_y

    @x.setter
    def x(self, value):
        self.plane_x = value

    @y.setter
    def y(self, value):
        self.plane_y = value

    def get_surface(self):
        return self.plane
