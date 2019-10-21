import pygame as pg
import os

from conf.settings import (
    images_path,
    bullet_music_path,
    me_down_music_path
)
from core.bullet import Bullet


class MyPlane(object):

    def __init__(self):
        self.screen = pg.display.get_surface()
        self.window_width, self.window_height = self.screen.get_size()

        # 个人分数
        self.score = 0

        # 我的飞机
        self.plane_image1_path = os.path.join(images_path, 'me1.png')
        self.plane_image2_path = os.path.join(images_path, 'me2.png')
        self.non_shooting_state()

        # 飞机的初始位置
        self.my_x = self.window_width // 2 - (self.plane.get_width() // 2)
        self.my_y = self.window_height - self.plane.get_height()

        # 飞机的移动速度
        self.speed = 10

        # 飞机子弹的对象列表
        self.bullet_obj_lis = []

        # 子弹射击音乐
        self.shoot_music = pg.mixer.Sound(bullet_music_path)
        self.shoot_music.set_volume(0.4)

        # 撞机音乐
        self.me_down = pg.mixer.Sound(me_down_music_path)
        self.me_down.set_volume(0.4)

        # 射击标志
        self.shoot_flag = False

    def non_shooting_state(self):
        self.plane = pg.image.load(self.plane_image1_path)
        # self.plane.fill((0,0,0))

    def shooting_state(self):
        self.plane = pg.image.load(self.plane_image2_path)
        # self.plane.fill((0, 0, 0))
        self.shoot_music.play()

    @property
    def x(self):
        return self.my_x

    @property
    def y(self):
        return self.my_y

    def get_surface(self):
        return self.plane

    def up(self):
        # print(self.my_y, self.window_height - self.plane.get_height())
        if self.speed < self.my_y <= self.window_height - self.plane.get_height():
            self.my_y -= self.speed

    def down(self):
        # print(self.my_y, self.window_height - self.plane.get_height())
        if 4 <= self.my_y < self.window_height - self.plane.get_height():
            self.my_y += self.speed

    def left(self):
        # print(self.my_x, self.window_width - self.plane.get_width())
        if -1 < self.my_x <= self.window_width - self.plane.get_width() + 1:
            self.my_x -= self.speed

    def right(self):
        # print(self.my_x, self.window_width - self.plane.get_width())
        if -1 <= self.my_x < self.window_width - self.plane.get_width() + 1:
            self.my_x += self.speed

    def shoot(self, flag=1):
        bullet = Bullet(self, flag)
        self.bullet_obj_lis.append(bullet)

    def bullet_fly(self):
        for obj in self.bullet_obj_lis:
            obj.up()

    def get_bullet_objs(self):
        temp = [obj for obj in self.bullet_obj_lis if obj.active]
        return temp

    def collision_detection(self, enemy_obj_lis):
        # 敌机身体和自己飞机身体产生碰撞
        plane_width = self.plane.get_width()
        plane_height = self.plane.get_height()
        for enemy in enemy_obj_lis:
            enemy_surface = enemy.get_surface()
            enemy_plane_width = enemy_surface.get_width()
            enemy_plane_height = enemy_surface.get_height()
            # 矩形的碰撞检测
            if enemy.enemy_x < self.my_x + plane_width and enemy.enemy_y < self.my_y + plane_height and enemy.enemy_x + enemy_plane_width > self.my_x and enemy.enemy_y + enemy_plane_height > self.my_y:
                # 撞机音效播放
                self.me_down.play()
                return True

    def bullet_collision_detection(self, enemy_obj_lis):
        bullet_objs = self.get_bullet_objs()
        for bullet in bullet_objs:
            bullet_surface = bullet.get_surface()
            bullet_width = bullet_surface.get_width()
            bullet_height = bullet_surface.get_height()
            for enemy in enemy_obj_lis:
                enemy_surface = enemy.get_surface()
                enemy_plane_width = enemy_surface.get_width()
                enemy_plane_height = enemy_surface.get_height()
                # 矩形的碰撞检测
                if enemy.enemy_x < bullet.bullet_x + bullet_width and enemy.enemy_y < bullet.bullet_y + bullet_height and enemy.enemy_x + enemy_plane_width > bullet.bullet_x and enemy.enemy_y + enemy_plane_height > bullet.bullet_y:
                    # 敌人减血
                    enemy.life -= bullet.ad
                    if enemy.life <= 0:
                        # 改变敌机的激活状态
                        enemy.active = False
                        # 加分
                        self.score += enemy.score
                    # 子弹消失
                    bullet.active = False
                    break

    def draw(self, main_while_count):
        # * 绘制飞机子弹
        self.bullet_fly()
        if self.shoot_flag:
            self.shoot_flag = False
            self.non_shooting_state()
        if main_while_count % 15 == 0:
            self.shoot_flag = True
            self.shooting_state()
            self.shoot()
        temp = []
        bullet_objs = self.get_bullet_objs()
        for obj in bullet_objs:
            temp.append([obj.get_surface(), (obj.x, obj.y)])
        self.screen.blits(temp)
        # * 绘制自己的飞机
        self.screen.blit(self.plane, (self.x, self.y))
