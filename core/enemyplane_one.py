import random
import os
import pygame as pg

from core.plane import Plane
from conf.settings import (
    images_path,
    enemy1_destroy_music_path,
)


class EnemyPlaneOne(Plane):

    def __init__(self):
        # 普通飞机
        # * 正常图
        self.plane_image_path = os.path.join(images_path, 'enemy1.png')
        # * 被子弹打中1
        self.plane_crash_image1 = os.path.join(images_path, 'enemy1_down1.png')
        # * 被子弹打中2
        self.plane_crash_image2 = os.path.join(images_path, 'enemy1_down2.png')
        # * 被子弹打中3
        self.plane_crash_image3 = os.path.join(images_path, 'enemy1_down3.png')
        # * 被子弹打中4(化成烟)
        self.plane_crash_image4 = os.path.join(images_path, 'enemy1_down4.png')
        # * 机毁音乐
        self.plane_destroy_music = pg.mixer.Sound(enemy1_destroy_music_path)
        self.plane_destroy_music.set_volume(0.3)
        # 调用父类初始化
        super().__init__(self.plane_image_path)
        # 初始位置
        plane = self.get_surface()
        x = random.randint(0, self.window_width - plane.get_width())
        y = random.randint(0, self.window_height - plane.get_height())
        y -= self.window_height
        # 设置初始位置
        self.set_init_position(x, y)
        # 其它属性
        self.sum_life = 10
        self.life = self.sum_life
        # 打中后的得分
        self.score = self.sum_life * 10
        # 敌方飞机的移动速度
        self.speed = 2
        # 敌机是否显示
        self.active = True

    def down(self):
        if self.y <= self.window_height:
            self.y += self.speed
        else:
            plane = self.get_surface()
            # 重新初始位置
            x = random.randint(0, self.window_width - plane.get_width())
            y = random.randint(0, self.window_height - plane.get_height())
            y -= self.window_height
            self.set_init_position(x, y)

    def draw(self, while_count=None):
        if self.active:
            # * 绘制敌方飞机
            self.screen.blit(self.get_surface(), (self.x, self.y))
            # 飞机默认往下飞
            self.down()
        else:
            # * 绘制炸掉的图
            temp = pg.image.load(self.plane_crash_image4)
            self.screen.blit(temp, (self.x, self.y))
            # * 播放音乐
            self.plane_destroy_music.play()

            self.__init__()
