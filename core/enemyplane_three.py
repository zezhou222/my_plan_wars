import os
import pygame as pg
import time

from core.plane import Plane
from conf.settings import (
    images_path,
    enemy3_destroy_music_path,
    enemy3_flying_music_path,
    game_music
)


class EnemyPlaneThree(Plane):

    def __init__(self):
        # boss级别的
        # * 正常图
        self.plane_image_path = os.path.join(images_path, 'enemy3_n1.png')
        self.plane_image_path = os.path.join(images_path, 'enemy3_n2.png')
        # * 被子弹打中1
        self.plane_crash_image1 = os.path.join(images_path, 'enemy3_down1.png')
        # * 被子弹打中2
        self.plane_crash_image2 = os.path.join(images_path, 'enemy3_down2.png')
        # * 被子弹打中3
        self.plane_crash_image3 = os.path.join(images_path, 'enemy3_down3.png')
        # * 被子弹打中4
        self.plane_crash_image4 = os.path.join(images_path, 'enemy3_down4.png')
        # * 被子弹打中5
        self.plane_crash_image5 = os.path.join(images_path, 'enemy3_down5.png')
        # * 被子弹打中6(化成烟)
        self.plane_crash_image6 = os.path.join(images_path, 'enemy3_down6.png')
        self.plane_crash_image_lis = [self.plane_crash_image1, self.plane_crash_image2, self.plane_crash_image3, self.plane_crash_image4, self.plane_crash_image5]
        # * 打子弹的
        self.plane_hit_image = os.path.join(images_path, 'enemy3_hit.png')
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
        self.sum_life = 1000
        self.life = self.sum_life
        # 打中后的得分
        self.score = self.sum_life * 10
        # 敌方飞机的移动速度
        self.speed = 1
        # 敌机存活状态
        self.active = True
        # boss多会出现
        self.arise_time = 5
        # 敌机出现标志
        self.arise_flag = False
        # 左右移动标志
        self.left_move = True
        self.right_move = False
        # 下降到哪个位置挺住
        self.down_position = 20

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

    def draw(self, while_count=None):
        # 检查血量更换图片
        self.check_blood(self.plane_crash_image_lis)

        # 表示多少秒后boss 出现
        if not self.arise_flag:
            if time.time() - self.game_start_time > self.arise_time:
                # 出现标志
                self.arise_flag = True
                pg.mixer.music.load(game_music[-3])
                pg.mixer.music.play(-1)
                # boss出场的音乐
                self.boss_arise_music.play()
            elif time.time() - self.game_start_time > self.arise_time - 2:
                # 主音乐结束
                pg.mixer.music.fadeout(2 * 1000)
            return

        if self.active:
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
            temp = pg.image.load(self.plane_crash_image6)
            self.screen.blit(temp, (self.x, self.y))
            # 停止主音乐
            pg.mixer.music.fadeout(5 * 1000)
            # * 播放音乐
            self.plane_destroy_music.play()

            return True
