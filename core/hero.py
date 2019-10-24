import os
import time

import pygame as pg
from core.plane import Plane
from conf.settings import (
    images_path,
    bullet_music_path,
    me_destroy_music_path,
    upgrade_music_path,
)

from core.bullet import (
    RedBullet,
    BlackBullet,
)
from core.supply import BlackBulletSupply, BombSupply
from core.enemyplane_one import EnemyPlaneOne
from core.enemyplane_two import EnemyPlaneTwo
from core.enemyplane_three import EnemyPlaneThree


class Hero(Plane):

    def __init__(self):
        # 生命值(用于抵抗敌机子弹之类的)
        self.sum_life = 100
        self.life = self.sum_life
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
        # * 走向毁灭1
        # * 走向毁灭2
        # * 走向毁灭3
        self.plane_collide_surface_lis = []
        for i in range(1, 4):
            temp = pg.image.load(os.path.join(images_path, 'me_destroy_%s.png' % i))
            self.plane_collide_surface_lis.append(temp)
        # * 虚无
        self.plane_collide_image4 = os.path.join(images_path, 'me_destroy_4.png')
        self.plane_collide_image4_surface = pg.image.load(self.plane_collide_image4)
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
        # 存活标志
        self.active = True
        # 实例的子弹类
        self.bullet = RedBullet
        # 供给列表
        self.supply_lis = []
        # 获取子弹供给后升级子弹的音乐
        self.upgrade_music = pg.mixer.Sound(upgrade_music_path)
        self.upgrade_music.set_volume(0.5)
        # 炸弹补给
        self.bomb_obj = None

    def get_bomb_supply(self):
        self.bomb_obj = BombSupply(self)
        self.supply_lis.append(self.bomb_obj)

    def change_bullet(self):
        if self.bullet is RedBullet:
            self.bullet = BlackBullet
            # 添加供给对象
            obj = BlackBulletSupply(self)
            self.supply_lis.append(obj)
            # 播放升级子弹的音乐
            self.upgrade_music.play()
        else:
            self.bullet = RedBullet

    def invincible_init(self):
        # 无敌效果标志
        self.invincible_flag = False
        # 无敌效果的持续时间
        self.invincible_time = 3
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

    def shoot(self):
        bullet = self.bullet(self)
        self.bullet_obj_lis.append(bullet)

    def bullet_fly(self):
        for obj in self.bullet_obj_lis:
            obj.up()

    def get_bullet_objs(self):
        temp = [obj for obj in self.bullet_obj_lis if obj.active]
        return temp

    def reset(self):
        # 活着的状态标志
        self.active = True
        # 恢复血量
        self.life = self.sum_life
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
                # 小兵挂了
                enemy.active = False
                # 撞机音乐
                self.crash_music.play()
                # 根据不同的敌机，撞击后撞掉不同的血
                if type(enemy) == EnemyPlaneOne:
                    self.life -= 20
                elif type(enemy) == EnemyPlaneTwo:
                    self.life -= 79
                else:
                    # 生命减1
                    self.life_num -= 1

                # 检测自己的血量，标志是否挂了
                if self.life <= 0:
                    # 挂了的标志
                    self.active = False
                    # 生命数减1
                    self.life_num -= 1
                # 检测自己是否没生命数了
                if self.life_num <= 0:
                    return True

                return

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

    def reduce_blood(self, num):
        if self.invincible_flag is False:
            self.life -= num

    def reset_bomb(self):
        self.supply_lis.remove(self.bomb_obj)
        self.bomb_obj = None

    def draw(self, main_while_count):
        if self.active:
            # 供给的过期检测
            for obj in self.supply_lis:
                ret = obj.expired_monitor()
                # 有返回值表示过期了
                if ret:
                    self.supply_lis.remove(ret)
                    if type(obj) is BombSupply:
                        self.bomb_obj = None

            # 根据血量展示不同的图片
            self.check_blood(self.plane_collide_surface_lis)

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
            # * 绘制炸弹供给
            if self.bomb_obj:
                self.bomb_obj.draw()
        else:
            # 播放音乐
            self.crash_music.play()
            # 渲染自己虚无的图
            self.screen.blit(self.plane_collide_image4_surface, (self.x, self.y))
            if self.life_num > 0:
                # 重新初始化
                self.reset()
