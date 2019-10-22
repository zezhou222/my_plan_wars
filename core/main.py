import os
import time

import pygame as pg
from conf.settings import (
    game_music,
    font_path,
    screentshot_path,
    images_path,
    enemy3_flying_music_path
)
from lib.global_func import (
    get_random_filename
)
from core.enemyplane_one import EnemyPlaneOne
from core.enemyplane_two import EnemyPlaneTwo
from core.enemyplane_three import EnemyPlaneThree
from core.hero import Hero


class MyGame(object):

    def __init__(self):
        pg.init()
        pg.display.init()
        pg.mixer.init()

        # 游戏窗口标题
        pg.display.set_caption('飞机大战')
        # 游戏窗口初始化设置
        self.window_width = 480
        self.window_height = 700
        self.screen = pg.display.set_mode((self.window_width, self.window_height))

        # 游戏帧数对象及初始帧数
        self.clock_obj = pg.time.Clock()
        self.frame_num = 60

        # 游戏音乐
        pg.mixer.music.load(game_music[-1])
        # pg.mixer.music.play(loops=-1)

        # 字体对象
        song_font_path = os.path.join(font_path, 'simsun.ttc')
        self.font = pg.font.Font(song_font_path, 50)
        self.middle_font = pg.font.Font(song_font_path, 30)
        self.small_font = pg.font.Font(song_font_path, 13)

        # 游戏背景图
        back_image_path = os.path.join(images_path, 'background.png')
        self.background = pg.image.load(back_image_path)

        # 开始游戏加载的资源
        self.game_start_init()
        # 游戏运行的资源
        self.game_running_init()
        # 游戏结束的
        self.game_over_init()
        # 通过的
        self.pass_func_init()

        # 退出标志
        self.exit_flag = False
        # 鼠标是否显示的标志
        self.mouse_visible = True
        # 运行标志
        self.running_flag = False
        # 结束标志
        self.over_flag = False
        # 通关标志
        self.pass_flag = False

    def game_start_init(self):
        temp = os.path.join(images_path, 'gamestart.png')
        self.gamestart_img = pg.image.load(temp)

    # 仅游戏开始时候运行一次
    def game_start(self):
        # 内容
        # (1) 游戏标题
        text = self.font.render("飞机大战", 1, (255, 0, 0))
        text_x = self.window_width // 2 - (text.get_width() // 2)
        text_y = 180
        self.screen.blit(text, (text_x, text_y))
        # (2) 游戏开始的按钮图片
        gamestart_x = self.window_width // 2 - (self.gamestart_img.get_width() // 2)
        gamestart_y = self.window_height // 2
        self.screen.blit(self.gamestart_img, (gamestart_x, gamestart_y))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True
        # 鼠标左键的点击事件监测
        if pg.mouse.get_pressed()[0]:
            now_x, now_y = pg.mouse.get_pos()
            # 监测开始游戏的
            if gamestart_x <= now_x <= gamestart_x + self.gamestart_img.get_width() and gamestart_y <= now_y <= gamestart_y + self.gamestart_img.get_height():
                self.running_flag = True
                # 放游戏音乐
                pg.mixer.music.play(loops=-1)
                return

    def paused(self):
        # * 绘制帮助文本内容
        text = self.small_font.render("注：再次按空格继续游戏。", 1, (0, 0, 0))
        text_x = self.window_width // 2 - (text.get_width() // 2)
        text_y = self.window_height // 2
        self.screen.blit(text, (text_x, text_y))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    if self.game_pause is True:
                        # 恢复音乐
                        pg.mixer.music.unpause()
                        # 重置标志位
                        self.game_pause = False

    def pass_through(self):
        pg.time.delay(200)

        # 绘制内容
        # * 所有的敌机炸毁
        if self.enemy_plane_obj_lis:
            obj = self.enemy_plane_obj_lis.pop(0)
            if obj.active is True and type(obj) is not EnemyPlaneThree:
                obj.active = False
                obj.draw()
        # * 绘制其它还未炸毁的飞机
        for obj in self.enemy_plane_obj_lis:
            if obj.active is True:
                self.screen.blit(obj.get_surface(), (obj.x, obj.y))
        # * 绘制自己的飞机
        for obj in self.plane_obj_lis:
            self.screen.blit(obj.get_surface(), (obj.x, obj.y))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True

        # 5秒后结束
        if time.time() - self.pass_start_time > 5:
            # 设置全局标志位
            self.running_flag = False
            self.pass_flag = True

    def game_running_init(self):
        # 自己飞机对象
        self.plane = Hero()
        self.plane_obj_lis = [self.plane]
        # 敌机飞机对象
        self.enemy_plane_obj_lis = []
        self.enemy_one_level = 10
        self.enemy_two_level = 1
        # 初始化敌人对象
        for i in range(self.enemy_one_level):
            obj = EnemyPlaneOne()
            self.enemy_plane_obj_lis.append(obj)
        for i in range(self.enemy_two_level):
            obj = EnemyPlaneTwo()
            self.enemy_plane_obj_lis.append(obj)
        # 大boss
        self.enemy_three_level_obj = EnemyPlaneThree()
        self.enemy_three_level_obj.game_start_time = time.time()
        self.enemy_plane_obj_lis.append(self.enemy_three_level_obj)
        # 计数器(用于延迟子弹发射)
        self.count = 0
        # 游戏暂停标志
        self.game_pause = False
        # 过关标志
        self.pass_through_flag = False
        self.pass_start_time = 0
        # 生命数的图片
        life_imge = os.path.join(images_path, 'life.png')
        self.life = pg.image.load(life_imge)

    def game_running(self):
        # 判断游戏暂停，进入暂停的事件循环
        if self.game_pause is True:
            self.paused()
            return

        # 判断过关
        if self.pass_through_flag is True:
            self.pass_through()
            return

        # 碰撞检测
        # * 检测主角和敌机身体的碰撞
        ret = self.plane.collision_detection(self.enemy_plane_obj_lis)
        if ret is True:
            self.running_flag = False
            self.over_flag = True
            # * 关闭主音乐
            pg.mixer.music.stop()
        # * 检测主角飞的子弹和敌机身体的碰撞
        self.plane.bullet_collision_detection(self.enemy_plane_obj_lis)

        # 内容
        # * 绘制敌方飞机
        for obj in self.enemy_plane_obj_lis:
            ret = obj.draw(self.count)
            # 过关判断，大boss挂了
            if ret is True:
                # 让其进入通关的事件循环中
                self.pass_through_flag = True
                # 通过的时间
                self.pass_start_time = time.time()
                return
        # * 绘制自己飞机方面的(子弹，自己的飞机等)
        for obj in self.plane_obj_lis:
            obj.draw(self.count)
        # * 绘制生命条数
        for index in range(self.plane.life_num, 0, -1):
            x = self.window_width - (self.life.get_width() * index)
            y = self.window_height - self.life.get_height()
            self.screen.blit(self.life, (x, y))
        # * 输出游戏fps
        game_fps = str(int(self.clock_obj.get_fps())) + " fps"
        text = self.small_font.render(game_fps, 1, (0, 0, 0))
        text_x = self.window_width - text.get_width()
        text_y = 0
        self.screen.blit(text, (text_x, text_y))
        # * 绘制分数
        text = self.middle_font.render("Score:%s" % self.plane.score, 1, (0, 0, 0))
        self.screen.blit(text, (0, 0))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True
            elif event.type == pg.KEYUP:
                # + 提高fps，- 降低fps ，每次幅度10(范围60-80)
                if event.key == pg.K_KP_PLUS and 60 <= self.frame_num < 80:
                    self.frame_num += 10
                elif event.key == pg.K_KP_MINUS and 60 < self.frame_num <= 80:
                    self.frame_num -= 10
                elif event.key == pg.K_p:
                    file_name = get_random_filename() + '.jpg'
                    file_path = os.path.join(screentshot_path, file_name)
                    pg.image.save(self.screen, file_path)
                elif event.key == pg.K_SPACE:
                    if self.game_pause is False:
                        # 暂停音乐
                        pg.mixer.music.pause()
                        # 暂停标志
                        self.game_pause = True

        # 主角的上下左右的长按事件
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_UP]:
            self.plane.up()
        elif key_pressed[pg.K_DOWN]:
            self.plane.down()
        elif key_pressed[pg.K_LEFT]:
            self.plane.left()
        elif key_pressed[pg.K_RIGHT]:
            self.plane.right()

        # 循环的计数器
        self.count += 1
        if self.count >= 100:
            self.count = 0

    def game_over_init(self):
        temp = os.path.join(images_path, 'again.png')
        self.again_img = pg.image.load(temp)

    def game_over(self):
        # 渲染
        # * game over
        text = self.font.render("Game Over", 1, (0, 0, 0))
        text_x = self.window_width // 2 - (text.get_width() // 2)
        text_y = 180
        self.screen.blit(text, (text_x, text_y))
        # * 重新开始
        again_x = self.window_width // 2 - (self.gamestart_img.get_width() // 2)
        again_y = self.window_height // 2
        self.screen.blit(self.again_img, (again_x, again_y))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True
        # 鼠标左键的点击事件监测
        if pg.mouse.get_pressed()[0]:
            now_x, now_y = pg.mouse.get_pos()
            # 监测开始游戏的
            if again_x <= now_x <= again_x + self.again_img.get_width() and again_y <= now_y <= again_y + self.again_img.get_height():
                self.again_game()
                return

    def pass_func_init(self):
        # 临时计数变量
        self.temp_count = self.plane.score

    def pass_func(self):
        # 渲染
        if self.temp_count >= self.plane.score:
            # * 成绩
            text = self.middle_font.render("总分数:%s" % self.plane.score, 1, (0, 0, 0))
            text_x = self.window_width // 2 - (text.get_width() // 2)
            text_y = 180
            self.screen.blit(text, (text_x, text_y))
            # * so good!
            text2 = self.middle_font.render("so good!", 1, (0, 0, 0))
            text_x = self.window_width // 2 - (text2.get_width() // 2)
            text_y = 180 + text.get_height() + 50
            self.screen.blit(text2, (text_x, text_y))
            # * 重新开始
            again_x = self.window_width // 2 - (self.gamestart_img.get_width() // 2)
            again_y = self.window_height // 2
            self.screen.blit(self.again_img, (again_x, again_y))
        else:
            # * 成绩
            text = self.middle_font.render("总分数:%s" % self.temp_count, 1, (0, 0, 0))
            text_x = self.window_width // 2 - (text.get_width() // 2)
            text_y = 180
            self.screen.blit(text, (text_x, text_y))

        # 事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit_flag = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_p:
                    file_name = get_random_filename() + '.jpg'
                    file_path = os.path.join(screentshot_path, file_name)
                    pg.image.save(self.screen, file_path)

        # 鼠标左键的点击事件监测
        if self.temp_count == self.plane.score and pg.mouse.get_pressed()[0]:
            now_x, now_y = pg.mouse.get_pos()
            # 监测开始游戏的
            if again_x <= now_x <= again_x + self.again_img.get_width() and again_y <= now_y <= again_y + self.again_img.get_height():
                self.again_game()
                return

        if self.temp_count < self.plane.score:
            if self.plane.score - self.temp_count < 100:
                self.temp_count += 1
            else:
                self.temp_count += 100

    def again_game(self):
        self.over_flag = False
        self.running_flag = True
        # 初始化游戏运行的资源
        self.game_running_init()
        self.pass_func_init()
        # 放游戏音乐
        pg.mixer.music.load(game_music[-1])
        pg.mixer.music.play(loops=-1)

    def run(self):
        while not self.exit_flag:
            # 帧数设置
            self.clock_obj.tick(self.frame_num)
            # 设置光标可见
            pg.mouse.set_visible(self.mouse_visible)
            # 背景图
            self.screen.blit(self.background, (0, 0))

            if self.running_flag:
                self.game_running()
            elif self.over_flag:
                self.game_over()
            elif self.pass_flag:
                self.pass_func()
            else:
                self.game_start()

            # 刷新屏幕
            pg.display.update()

        pg.quit()


def run():
    MyGame().run()
