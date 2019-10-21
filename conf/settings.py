import os


project_path = os.getcwd()

log_path = os.path.join(project_path, 'log')

static_path = os.path.join(project_path, 'static')

music_path = os.path.join(static_path, 'music')

game_music = [
    os.path.join(music_path, '晴天.mp3'),
    os.path.join(music_path, '成都.mp3'),
    os.path.join(music_path, 'hundouluo.wav')
]

font_path = os.path.join(static_path, 'font')

screentshot_path = os.path.join(static_path, 'screenshot')

images_path = os.path.join(static_path, 'images')

bullet_music_path = os.path.join(music_path, 'bullet.wav')

me_down_music_path = os.path.join(music_path, 'me_down.wav')

enemy1_down_music_path = os.path.join(music_path, 'enemy1_down.wav')

enemy2_down_music_path = os.path.join(music_path, 'enemy2_down.wav')

enemy3_down_music_path = os.path.join(music_path, 'enemy3_down.wav')

enemy3_flying_music_path = os.path.join(music_path, 'enemy3_flying.wav')
