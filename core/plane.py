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

    # 根据不同血量更换敌机surface对象
    def check_blood(self, plane_crash_image_lis):
        list_length = len(plane_crash_image_lis)
        avg_blood = self.sum_life / (list_length+1)
        # 敌机血量很健康，不更换图片(默认是普通形式的)
        if self.life >= avg_blood * list_length:
            return
        # 血量在正常下，进行血量区间判断更换
        for index in range(list_length, 0, -1):
            if avg_blood * (index-1) <= self.life < avg_blood * index:
                self.plane = plane_crash_image_lis[list_length - index]
                return
