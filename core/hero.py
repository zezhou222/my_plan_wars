import os
import time

import pygame as pg
from core.plane import Plane
from conf.settings import (
    images_path,
    bullet_music_path,
    me_destroy_music_path
)
from core.bullet import Bullet


class Hero(Plane):

    def __init__(self):
        # 个人分数
        self.score = 0
        # 飞机的移动速度
        self.speed = 10
        # 生命数
        self.life_num = 3
        # 我的飞机
        # * 非射击图
        self.plane_image1_path = os.path.join(images_path, 'me1.png')
        # * 射击图
        self.plane_image2_path = os.path.join(images_path, 'me2.png')
        # * 被撞1次
        self.plane_collide_image1 = os.path.join(images_path, 'me_destroy_1.png')
        # * 被撞2次
        self.plane_collide_image2 = os.path.join(images_path, 'me_destroy_2.png')
        # * 被撞3次
        self.plane_collide_image3 = os.path.join(images_path, 'me_destroy_3.png')
        # * 剩余的生命数不同显示的不同炸毁图片
        self.plane_collide_image_lis = [self.plane_collide_image1, self.plane_collide_image2, self.plane_collide_image3]
        # 父类初始化
        super().__init__(self.plane_image1_path)
        # 飞机的初始位置
        x = self.window_width // 2 - (self.plane.get_width() // 2)
        y = self.window_height - self.plane.get_height()
        self.set_init_position(x, y)
        # 子弹射击音乐
        self.shoot_music = pg.mixer.Sound(bullet_music_path)
        self.shoot_music.set_volume(0.3)
        # 撞机音乐
        self.crash_music = pg.mixer.Sound(me_destroy_music_path)
        self.crash_music.set_volume(0.4)
        # 射击标志
        self.shoot_flag = False
        # 飞机子弹的对象列表
        self.bullet_obj_lis = []
        # 无敌效果的属性
        self.invincible_init()

    def invincible_init(self):
        # 无敌效果标志
        self.invincible_flag = False
        # 无敌效果的持续时间
        self.invincible_time = 2
        # 无敌的开始时间
        self.invincible_start_time = 0

    def up(self):
        if self.speed < self.y <= self.window_height - self.plane.get_height():
            self.plane_y -= self.speed

    def down(self):
        if 4 <= self.y < self.window_height - self.plane.get_height():
            self.plane_y += self.speed

    def left(self):
        if -1 < self.x <= self.window_width - self.plane.get_width() + 1:
            self.plane_x -= self.speed

    def right(self):
        if -1 <= self.x < self.window_width - self.plane.get_width() + 1:
            self.plane_x += self.speed

    def shoot(self, flag=1):
        bullet = Bullet(self, flag)
        self.bullet_obj_lis.append(bullet)

    def bullet_fly(self):
        for obj in self.bullet_obj_lis:
            obj.up()

    def get_bullet_objs(self):
        temp = [obj for obj in self.bullet_obj_lis if obj.active]
        return temp

    def reset(self):
        # 飞机复活的位置
        x = self.window_width // 2 - (self.plane.get_width() // 2)
        y = self.window_height - self.plane.get_height()
        self.set_init_position(x, y)
        # 飞机无敌效果开启
        self.invincible_flag = True
        # 无效效果开始时间
        self.invincible_start_time = time.time()

    def collision_detection(self, enemy_obj_lis):
        # 判断无敌效果
        if self.invincible_flag is True:
            return

        # 敌机身体和自己飞机身体产生碰撞
        plane_width = self.plane.get_width()
        plane_height = self.plane.get_height()
        for enemy in enemy_obj_lis:
            enemy_surface = enemy.get_surface()
            enemy_plane_width = enemy_surface.get_width()
            enemy_plane_height = enemy_surface.get_height()
            # 矩形的碰撞检测
            if enemy.x < self.x + plane_width and enemy.y < self.y + plane_height and enemy.x + enemy_plane_width > self.x and enemy.y + enemy_plane_height > self.y:
                if self.life_num > 0:
                    self.life_num -= 1
                    # 撞机
                    self.crash()
                    # 重置
                    self.reset()
                    return
                else:
                    # 撞机
                    self.crash()
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
                if enemy.x < bullet.bullet_x + bullet_width and enemy.y < bullet.bullet_y + bullet_height and enemy.x + enemy_plane_width > bullet.bullet_x and enemy.y + enemy_plane_height > bullet.bullet_y:
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

    def crash(self):
        self.crash_music.play()
        self.plane = pg.image.load(self.plane_collide_image_lis[3 - self.life_num - 1])

    def draw(self, main_while_count):
        # * 绘制飞机子弹
        self.bullet_fly()
        if self.shoot_flag:
            self.shoot_flag = False
            self.non_shooting_state(self.plane_image1_path)
        if main_while_count % 15 == 0:
            self.shoot_flag = True
            self.shooting_state(self.plane_image2_path, self.shoot_music)
            self.shoot()
        temp = []
        bullet_objs = self.get_bullet_objs()
        for obj in bullet_objs:
            temp.append([obj.get_surface(), (obj.x, obj.y)])
        self.screen.blits(temp)
        # 无敌判断及取消
        if self.invincible_flag is True:
            # 判断超时
            if time.time() - self.invincible_start_time > self.invincible_time:
                self.invincible_init()
        # * 绘制自己的飞机
        self.screen.blit(self.get_surface(), (self.x, self.y))
