import os


project_path = os.getcwd()

log_path = os.path.join(project_path, 'log')

static_path = os.path.join(project_path, 'static')

music_path = os.path.join(static_path, 'music')

game_music = [
    os.path.join(music_path, '白金迪斯科.mp3'),
    os.path.join(music_path, '成都.mp3'),
    os.path.join(music_path, 'game_music.ogg'),
    os.path.join(music_path, 'hundouluo.wav')
]

font_path = os.path.join(static_path, 'font')

screentshot_path = os.path.join(static_path, 'screenshot')

images_path = os.path.join(static_path, 'images')

bullet_music_path = os.path.join(music_path, 'bullet.wav')

me_destroy_music_path = os.path.join(music_path, 'me_down.wav')

enemy1_destroy_music_path = os.path.join(music_path, 'enemy1_down.wav')

enemy2_destroy_music_path = os.path.join(music_path, 'enemy2_down.wav')

enemy3_destroy_music_path = os.path.join(music_path, 'enemy3_down.wav')

enemy3_flying_music_path = os.path.join(music_path, 'enemy3_flying.wav')

supply_music_path = os.path.join(music_path, 'supply.wav')

get_bullet_music_path = os.path.join(music_path, 'get_bullet.wav')

get_bomb_music_path = os.path.join(music_path, 'get_bomb.wav')

use_bomb_music_path = os.path.join(music_path, 'use_bomb.wav')

upgrade_music_path = os.path.join(music_path, 'upgrade.wav')

