import os

import pygame as pg

from conf.settings import images_path


class Bullet(object):

    def __init__(self, plane, bullet_img):
        self.screen = pg.display.get_surface()
        self.window_width, self.window_height = self.screen.get_size()

        self.plane = plane

        self.bullet = pg.image.load(bullet_img)
        # 敌方飞机和自己的飞机，子弹的初始位置不同
        from core.hero import Hero
        if type(self.plane) is Hero:
            # 初始位置
            self.plane_surface = self.plane.get_surface()
            self.bullet_x = self.plane.x + (self.plane_surface.get_width() // 2) - (self.bullet.get_width() // 2)
            self.bullet_y = self.plane.y - 25
        else:
            # 初始位置
            self.plane_surface = self.plane.get_surface()
            self.bullet_x = self.plane.x + (self.plane_surface.get_width() // 2) - (self.bullet.get_width() // 2)
            self.bullet_y = self.plane.y + self.plane_surface.get_height() + 5

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

    def down(self):
        if not self.active or self.bullet_y >= self.window_height + self.bullet.get_height():
            del self
        else:
            self.bullet_y += self.speed

    def get_surface(self):
        return self.bullet


class RedBullet(Bullet):

    def __init__(self, plane):
        # 哪个飞机打的子弹
        self.plane = plane
        # 子弹的图片
        bullet_img = os.path.join(images_path, 'bullet1.png')
        super().__init__(plane, bullet_img)
        # 子弹飞行速度
        self.speed = 15
        # 子弹的攻击力
        self.ad = 10


class BlackBullet(Bullet):

    def __init__(self, plane):
        # 哪个飞机打的子弹
        self.plane = plane
        bullet_img = os.path.join(images_path, 'bullet2.png')
        super().__init__(plane, bullet_img)
        # 子弹飞行速度
        self.speed = 20
        # 子弹的攻击力
        self.ad = 30
