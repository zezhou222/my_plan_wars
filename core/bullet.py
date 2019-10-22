import pygame as pg
import os

from conf.settings import images_path


class Bullet(object):

    def __init__(self, plane, flag):
        self.screen = pg.display.get_surface()
        self.window_width, self.window_height = self.screen.get_size()

        self.plane = plane

        if flag:
            bullet_img = os.path.join(images_path, 'bullet1.png')
            self.bullet = pg.image.load(bullet_img)
            self.ad = 10

        # 初始位置
        self.plane_surface = self.plane.get_surface()
        self.bullet_x = self.plane.x + (self.plane_surface.get_width() // 2) - (self.bullet.get_width() // 2)
        self.bullet_y = self.plane.y - 25

        # 子弹飞行速度
        self.speed = 15

        # 子弹超过一屏幕，攻击失效标志,或攻击到敌机目标，不显示
        self.active = True

    @property
    def x(self):
        return self.bullet_x

    @property
    def y(self):
        return self.bullet_y

    def up(self):
        if not self.active or self.bullet_y <= 0 - self.bullet.get_height():
            del self
        else:
            self.bullet_y -= self.speed

    def get_surface(self):
        return self.bullet
