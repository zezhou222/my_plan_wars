import os
import random
import time

import pygame as pg

from conf.settings import (
    images_path,
    get_bullet_music_path,
    get_bomb_music_path,
    use_bomb_music_path)


class BlackBulletSupply(object):

    def __init__(self, plane=None):
        if plane:
            self.plane = plane
            # 供给得到的时间(在碰撞后更改)
            self.supply_get_time = time.time()
            # 供给的持续时间
            self.supply_keep_time = 10
        else:
            self.screen = pg.display.get_surface()
            supply_image = os.path.join(images_path, 'bullet_supply.png')
            self.supply_surface = pg.image.load(supply_image)
            # 供给的初始位置
            self.supply_x = random.randint(0, self.screen.get_width() - self.supply_surface.get_width())
            self.supply_y = 0 - self.supply_surface.get_height()
            # 供给的移动速度
            self.supply_speed = 1
            # 得到供给的音乐
            self.music = pg.mixer.Sound(get_bullet_music_path)
            self.music.set_volume(0.4)

    def expired_monitor(self):
        if time.time() - self.supply_get_time > self.supply_keep_time:
            self.plane.change_bullet()
            return self

    def supply_collision_detection(self, plane_objs):
        for obj in plane_objs:
            plane_surface = obj.get_surface()
            plane_width = plane_surface.get_width()
            plane_height = plane_surface.get_height()
            supply_width = self.supply_surface.get_width()
            supply_height = self.supply_surface.get_height()
            if self.supply_x < obj.x + plane_width and self.supply_y < obj.y + plane_height and self.supply_x + supply_width > obj.x and self.supply_y + supply_height > obj.y:
                # 让飞机升级子弹
                obj.change_bullet()
                # 播放获取子弹的音乐
                self.music.play()
                return self

    def supply_move(self):
        self.supply_y += self.supply_speed

    def draw(self):
        # * 渲染图
        self.screen.blit(self.supply_surface, (self.supply_x, self.supply_y))
        # * 移动
        self.supply_move()


class BombSupply(object):

    def __init__(self, plane=None):
        self.plane = plane
        self.screen = pg.display.get_surface()
        if plane:
            # 炸弹补给使用后的音乐
            self.use_bomb_music = pg.mixer.Sound(use_bomb_music_path)
            self.use_bomb_music.set_volume(0.5)
            # 炸弹框图片
            supply_image = os.path.join(images_path, 'bomb.png')
            self.supply_surface = pg.image.load(supply_image)
            # 初始位置
            x, y = pg.mouse.get_pos()
            self.supply_x = x - self.supply_surface.get_width() // 2
            self.supply_y = y - self.supply_surface.get_height() // 2
            # 供给得到的时间(在碰撞后更改)
            self.supply_get_time = time.time()
            # 供给的持续时间
            self.supply_keep_time = 10
            # 伤害
            self.ad = 1000
        else:
            supply_image = os.path.join(images_path, 'bomb_supply.png')
            self.supply_surface = pg.image.load(supply_image)
            # 供给的初始位置
            self.supply_x = random.randint(0, self.screen.get_width() - self.supply_surface.get_width())
            self.supply_y = 0 - self.supply_surface.get_height()
            # 供给的移动速度
            self.supply_speed = 1
            # 得到供给的音乐
            self.music = pg.mixer.Sound(get_bomb_music_path)
            self.music.set_volume(0.4)

    def expired_monitor(self):
        if time.time() - self.supply_get_time > self.supply_keep_time:
            self.plane.change_bullet()
            return self

    def supply_collision_detection(self, plane_objs):
        for obj in plane_objs:
            plane_surface = obj.get_surface()
            plane_width = plane_surface.get_width()
            plane_height = plane_surface.get_height()
            supply_width = self.supply_surface.get_width()
            supply_height = self.supply_surface.get_height()
            if self.supply_x < obj.x + plane_width and self.supply_y < obj.y + plane_height and self.supply_x + supply_width > obj.x and self.supply_y + supply_height > obj.y:
                # 获取炸弹补给
                obj.get_bomb_supply()
                # 播放获取炸弹的音乐
                self.music.play()
                return self

    def supply_move(self):
        self.supply_y += self.supply_speed

    def use(self, enemy_plane_objs):
        # 播放音乐
        self.use_bomb_music.play()
        # 屏幕内的敌方飞机都减血
        for enemy in enemy_plane_objs:
            if enemy.y > 0:
                enemy.life -= self.ad
                if enemy.life <= 0:
                    # 加分
                    self.plane.score += enemy.score
                    # 消灭
                    enemy.active = False
        # 重置飞机的bomb
        self.plane.reset_bomb()

    def draw(self):
        if self.plane:
            # 跟随鼠标位置
            x, y = pg.mouse.get_pos()
            self.supply_x = x - self.supply_surface.get_width() // 2
            self.supply_y = y - self.supply_surface.get_height() // 2
            # * 渲染图
            self.screen.blit(self.supply_surface, (self.supply_x, self.supply_y))
        else:
            # * 渲染图
            self.screen.blit(self.supply_surface, (self.supply_x, self.supply_y))
            # * 移动
            self.supply_move()
