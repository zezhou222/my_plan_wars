import os
import pygame as pg
import time

from core.bullet import BlackBullet
from core.plane import Plane
from conf.settings import (
    images_path,
    enemy3_destroy_music_path,
    enemy3_flying_music_path,
    game_music,
    bullet_music_path)


class EnemyPlaneThree(Plane):

    def __init__(self):
        # boss级别的
        # * 正常图
        self.plane_image_path = os.path.join(images_path, 'enemy3_n1.png')
        self.plane_image_path = os.path.join(images_path, 'enemy3_n2.png')
        # * 被子弹打中1
        # * 被子弹打中2
        # * 被子弹打中3
        # * 被子弹打中4
        # * 被子弹打中5
        self.plane_crash_surface_lis = []
        for i in range(1, 6):
            temp = pg.image.load(os.path.join(images_path, 'enemy3_down%s.png' % i))
            self.plane_crash_surface_lis.append(temp)
        # * 被子弹打中6(化成烟)
        self.plane_crash_image6 = os.path.join(images_path, 'enemy3_down6.png')
        self.plane_crash_image6_surface = pg.image.load(self.plane_crash_image6)
        # * 打子弹的
        self.plane_hit_image = os.path.join(images_path, 'enemy3_hit.png')
        # 子弹射击音乐
        self.shoot_music = pg.mixer.Sound(bullet_music_path)
        self.shoot_music.set_volume(0.3)
        # * 机毁音乐
        self.plane_destroy_music = pg.mixer.Sound(enemy3_destroy_music_path)
        # * 出现的音乐
        # 出场音乐
        self.boss_arise_music = pg.mixer.Sound(enemy3_flying_music_path)
        self.boss_arise_music.set_volume(1)
        # 调用父类初始化
        super().__init__(self.plane_image_path)
        # 初始位置
        plane = self.get_surface()
        x = self.window_width // 2 - (plane.get_width() // 2)
        y = 0 - plane.get_height()
        # 设置初始位置
        self.set_init_position(x, y)
        # 其它属性
        self.sum_life = 3000
        self.life = self.sum_life
        # 打中后的得分
        self.score = self.sum_life * 10
        # 敌方飞机的移动速度
        self.speed = 1
        # 敌机存活状态
        self.active = True
        # boss多会出现
        self.arise_time = 120
        # 敌机出现标志
        self.arise_flag = False
        # 左右移动标志
        self.left_move = True
        self.right_move = False
        # 下降到哪个位置挺住
        self.down_position = 5
        # 射击标志
        self.shoot_flag = False
        # 飞机子弹的对象列表
        self.bullet_obj_lis = []
        # 每轮射击多少枚子弹
        self.bullet_num = 3
        # 每轮第一次射击的开始时间
        self.first_shoot_time = None
        # 每轮发射子弹的间隔时间
        self.shoot_interval_time = 5

    def down(self):
        if self.y <= self.down_position:
            self.y += self.speed

    def left(self):
        if self.left_move:
            if self.x >= self.speed:
                self.x -= self.speed
            else:
                self.left_move = False
                self.right_move = True

    def right(self):
        if self.right_move:
            plane = self.get_surface()
            if self.x <= self.window_width - plane.get_width():
                self.x += self.speed
            else:
                self.right_move = False
                self.left_move = True

    def bullet_fly(self):
        for obj in self.bullet_obj_lis:
            obj.down()

    def shoot(self):
        bullet = BlackBullet(self)
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
        # 表示多少秒后boss 出现
        if not self.arise_flag:
            if time.time() - self.game_start_time > self.arise_time:
                # 出现标志
                self.arise_flag = True
                pg.mixer.music.load(game_music[0])
                pg.mixer.music.set_volume(0.8)
                pg.mixer.music.play(-1)
                # boss出场的音乐
                self.boss_arise_music.play()
            elif time.time() - self.game_start_time > self.arise_time - 3:
                # 主音乐结束
                pg.mixer.music.fadeout(3 * 1000)
            return

        if self.active:
            # 检查血量更换图片
            self.check_blood(self.plane_crash_surface_lis)

            if len(self.bullet_obj_lis) >= self.bullet_num and time.time() - self.first_shoot_time > self.shoot_interval_time:
                # 清空子弹夹
                self.bullet_obj_lis.clear()
                # 初始化时间
                self.first_shoot_time = None

            # * 绘制飞机子弹
            self.bullet_fly()
            if self.shoot_flag:
                self.shoot_flag = False
                self.non_shooting_state(self.plane_image_path)
            if (self.left_move or self.right_move) and len(self.bullet_obj_lis) < self.bullet_num and while_count % 5 == 0:
                self.shoot_flag = True
                self.shooting_state(self.plane_hit_image, self.shoot_music)
                self.shoot()
                # 第一次射击的时间记录
                if self.first_shoot_time is None:
                    self.first_shoot_time = time.time()

            temp = []
            bullet_objs = self.get_bullet_objs()
            for obj in bullet_objs:
                temp.append([obj.get_surface(), (obj.x, obj.y)])
            self.screen.blits(temp)

            plane = self.get_surface()
            # * 绘制敌方飞机
            self.screen.blit(plane, (self.x, self.y))
            if self.life / self.sum_life > 0.2:
                pg.draw.rect(self.screen, (0, 255, 0), [self.x, self.y - 5, int(plane.get_width() * (self.life / self.sum_life)), 5])
            else:
                pg.draw.rect(self.screen, (255, 0, 0), [self.x, self.y - 5, int(plane.get_width() * (self.life / self.sum_life)), 5])
            # 飞机默认往下飞，直到一个位置停住
            self.down()
            # 开始左右移动
            self.left()
            self.right()
        else:
            # * 绘制炸掉的图
            self.screen.blit(self.plane_crash_image6_surface, (self.x, self.y))
            # 停止主音乐
            pg.mixer.music.fadeout(2 * 1000)
            # * 播放音乐
            self.plane_destroy_music.play()

            return True
