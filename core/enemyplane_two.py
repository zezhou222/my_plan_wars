import random
import os
import pygame as pg

from core.bullet import RedBullet
from core.plane import Plane
from conf.settings import (
    images_path,
    enemy2_destroy_music_path,
    bullet_music_path
)


class EnemyPlaneTwo(Plane):

    def __init__(self):
        # 中等级别
        # * 正常图
        self.plane_image_path = os.path.join(images_path, 'enemy2.png')
        # * 被子弹打中1
        # * 被子弹打中2
        # * 被子弹打中3
        self.plane_crash_surface_lis = []
        for i in range(1, 4):
            temp = pg.image.load(os.path.join(images_path, 'enemy2_down%s.png' % i))
            self.plane_crash_surface_lis.append(temp)
        # * 被子弹打中4(化成烟)
        self.plane_crash_image4 = os.path.join(images_path, 'enemy2_down4.png')
        self.plane_crash_image4_surface = pg.image.load(self.plane_crash_image4)
        # * 打子弹的图
        self.plane_hit_image = os.path.join(images_path, 'enemy2_hit.png')
        # * 机毁音乐
        self.plane_destroy_music = pg.mixer.Sound(enemy2_destroy_music_path)
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
        self.sum_life = 60
        self.life = self.sum_life
        # 打中后的得分
        self.score = self.sum_life * 10
        # 敌方飞机的移动速度
        self.speed = 2
        # 敌机是否显示
        self.active = True
        # 飞机子弹的对象列表
        self.bullet_obj_lis = []
        # 子弹射击音乐
        self.shoot_music = pg.mixer.Sound(bullet_music_path)
        self.shoot_music.set_volume(0.3)
        # 射击标志
        self.shoot_flag = False

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
            # 清空子弹列表
            self.bullet_obj_lis.clear()

    def bullet_fly(self):
        for obj in self.bullet_obj_lis:
            obj.down()

    def arrive_shoot_position(self):
        if self.y >= self.get_surface().get_height() // 2:
            return True

    def shoot(self):
        if self.arrive_shoot_position():
            bullet = RedBullet(self)
            self.bullet_obj_lis.append(bullet)

    def get_bullet_objs(self):
        temp = [obj for obj in self.bullet_obj_lis if obj.active]
        return temp

    def bullet_collision_detection(self, hero_obj_lis):
        bullet_objs = self.get_bullet_objs()
        for bullet in bullet_objs:
            bullet_surface = bullet.get_surface()
            bullet_width = bullet_surface.get_width()
            bullet_height = bullet_surface.get_height()
            for hero in hero_obj_lis:
                hero_surface = hero.get_surface()
                hero_plane_width = hero_surface.get_width()
                hero_plane_height = hero_surface.get_height()
                # 矩形碰撞监测
                if hero.x < bullet.bullet_x + bullet_width and hero.y < bullet.bullet_y + bullet_height and hero.x + hero_plane_width > bullet.bullet_x and hero.y + hero_plane_height > bullet.bullet_y:
                    # 自己飞机减血
                    hero.reduce_blood(bullet.ad)
                    if hero.life <= 0:
                        hero.active = False
                        if hero.life_num > 0:
                            # 生命减1
                            hero.life_num -= 1
                        else:
                            return True
                    # 子弹消失
                    bullet.active = False
                    break

    def draw(self, while_count=None):
        if self.active:
            # 检查血量更换图片
            self.check_blood(self.plane_crash_surface_lis)

            # * 绘制飞机子弹
            self.bullet_fly()
            if self.shoot_flag:
                self.shoot_flag = False
                self.non_shooting_state(self.plane_image_path)
            if self.arrive_shoot_position() and len(self.bullet_obj_lis) < 3 and while_count % 10 == 0:
                self.shoot_flag = True
                self.shooting_state(self.plane_hit_image, self.shoot_music)
                self.shoot()
            temp = []
            bullet_objs = self.get_bullet_objs()
            for obj in bullet_objs:
                temp.append([obj.get_surface(), (obj.x, obj.y)])
            self.screen.blits(temp)
            # * 绘制敌方飞机
            self.screen.blit(self.get_surface(), (self.x, self.y))
            # * 画血条
            plane = self.get_surface()
            if self.life / self.sum_life > 0.2:
                pg.draw.rect(self.screen, (0, 255, 0), [self.x, self.y - 5, int(plane.get_width() * (self.life / self.sum_life)), 5])
            else:
                pg.draw.rect(self.screen, (255, 0, 0), [self.x, self.y - 5, int(plane.get_width() * (self.life / self.sum_life)), 5])
            # 飞机默认往下飞
            self.down()
        else:
            # * 绘制炸掉的图
            self.screen.blit(self.plane_crash_image4_surface, (self.x, self.y))
            # * 播放音乐
            self.plane_destroy_music.play()

            self.__init__()
