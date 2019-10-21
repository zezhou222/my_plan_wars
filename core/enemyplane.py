import pygame as pg
import random
import os

from conf.settings import (
    images_path,
    enemy1_down_music_path,
    enemy2_down_music_path,
    enemy3_down_music_path
)


class EnemyPlane(object):

    def __init__(self, enemy_level=1):
        self.screen = pg.display.get_surface()
        self.window_width, self.window_height = self.screen.get_size()

        self.enemy_level = enemy_level
        # 敌方飞机
        # 1是普通小飞机, 2是厉害点的
        if enemy_level == 1:
            plane_image_path = os.path.join(images_path, 'enemy1.png')
            plane_down_image_path = os.path.join(images_path, 'enemy1_down3.png')
            self.enemy_down = pg.image.load(plane_down_image_path)
            self.enemy = pg.image.load(plane_image_path)
            self.sum_life = 10
            self.life = 10
            self.score = 100
        elif enemy_level == 2:
            plane_image_path = os.path.join(images_path, 'enemy2.png')
            plane_down_image_path = os.path.join(images_path, 'enemy2_down3.png')
            self.enemy_down = pg.image.load(plane_down_image_path)
            self.enemy = pg.image.load(plane_image_path)
            self.sum_life = 50
            self.life = 50
            self.score = 500
        elif enemy_level == 3:
            plane_image_path = os.path.join(images_path, 'enemy3_n1.png')
            plane_down_image_path = os.path.join(images_path, 'enemy3_down3.png')
            self.enemy_down = pg.image.load(plane_down_image_path)
            self.enemy = pg.image.load(plane_image_path)
            self.sum_life = 500
            self.life = 500
            self.score = 5000
            self.down_position = 20

        if enemy_level <= 2:
            # 初始位置
            self.enemy_x = random.randint(0, self.window_width - self.enemy.get_width())
            self.enemy_y = random.randint(0, self.window_height - self.enemy.get_height())
            self.enemy_y -= self.window_height

            # 敌方飞机的移动速度
            self.speed = 2
        elif enemy_level == 3:
            # 初始位置
            self.enemy_x = self.window_width // 2 - (self.enemy.get_width() // 2)
            self.enemy_y = 0 - self.enemy.get_height()

            # 敌方飞机的移动速度
            self.speed = 1

            # 左右移动标志
            self.left_move = True
            self.right_move = False

        # 敌机是否显示
        self.active = True

    @property
    def x(self):
        return self.enemy_x

    @property
    def y(self):
        return self.enemy_y

    def down(self):
        if self.enemy_level <= 2:
            if self.enemy_y <= self.window_height:
                self.enemy_y += self.speed
            else:
                # 重新初始位置
                self.enemy_x = random.randint(0, self.window_width - self.enemy.get_width())
                self.enemy_y = random.randint(0, self.window_height - self.enemy.get_height())
                self.enemy_y -= self.window_height
        elif self.enemy_level == 3:
            if self.enemy_y <= self.down_position:
                self.enemy_y += self.speed

    def left(self):
        if self.left_move:
            if self.enemy_x >= self.speed:
                self.enemy_x -= self.speed
            else:
                self.left_move = False
                self.right_move = True

    def right(self):
        if self.right_move:
            if self.enemy_x <= self.window_width - self.enemy.get_width():
                self.enemy_x += self.speed
            else:
                self.right_move = False
                self.left_move = True

    def get_surface(self):
        return self.enemy

    def draw(self, while_count=None):
        if self.active:
            if self.enemy_level <= 2:
                # * 绘制敌方飞机
                self.screen.blit(self.enemy, (self.x, self.y))
                # * 画血条
                if self.enemy_level == 2:
                    pg.draw.rect(self.screen, (255, 0, 0), [self.enemy_x, self.enemy_y-5, int(self.enemy.get_width() * (self.life / self.sum_life)), 5])
                # 飞机默认往下飞
                self.down()
            elif self.enemy_level == 3:
                # * 绘制敌方飞机
                self.screen.blit(self.enemy, (self.x, self.y))
                pg.draw.rect(self.screen, (255, 0, 0), [self.enemy_x, self.enemy_y - 5, int(self.enemy.get_width() * (self.life / self.sum_life)), 5])
                # 飞机默认往下飞，直到一个位置停住
                self.down()
                # 开始左右移动
                self.left()
                self.right()

        else:
            if self.enemy_level <= 2:
                # * 绘制炸掉的图
                self.screen.blit(self.enemy_down, (self.x, self.y))
                # = 爆炸音效
                if self.enemy_level == 1:
                    pg.mixer.Sound(enemy1_down_music_path).play()
                elif self.enemy_level == 2:
                    pg.mixer.Sound(enemy2_down_music_path).play()

                # * 初始化飞机
                self.__init__(self.enemy_level)
            elif self.enemy_level == 3:
                # * 绘制炸掉的图
                self.screen.blit(self.enemy_down, (self.x, self.y))
                # * 爆炸音效
                pg.mixer.Sound(enemy3_down_music_path).play()

                return True
