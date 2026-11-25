"""
File: main.py
Author: Chuncheng Zhang
Date: 2026-11-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Clock demo using pygame.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2026-11-18 ------------------------
# Requirements and constants
import io
import time
import requests
import pygame as pg

from PIL import Image
from loguru import logger

from heavy_load_job import HeavyWorkLoad
from threading import Thread

# %%
WIDTH = 1440
HEIGHT = 900
sizes = [8, 12, 24, 32, 64]
font_name = 'font/MSYH.TTC'
url = 'https://images4.alphacoders.com/485/thumb-1920-48578.jpg'

# %%
pg.init()

CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
FONTs = {sz: pg.font.Font(font_name, sz) for sz in sizes}

HWL = HeavyWorkLoad()


# %% ---- 2026-11-18 ------------------------
# Function and class
def load_background(url, size):
    """下载 url 图片并缩放成 size 的 Surface，失败返回 None。"""
    try:
        resp = requests.get(url, timeout=2)
        resp.raise_for_status()
        img = Image.open(io.BytesIO(resp.content)).convert('RGB')
        img = img.resize(size, Image.LANCZOS)

        # PIL -> pygame Surface
        surf = pg.image.frombytes(
            img.tobytes(), img.size, 'RGB'
        ).convert()
        return surf
    except Exception as err:
        logger.error(f'Failed to load background: {err}')
        return None


BACKGROUND_IMG = load_background(url, (WIDTH, HEIGHT))


# %%
class Control:
    cursor_x = 0
    cursor_y = 0
    key = ''
    text = ''
    t = 0

    def __init__(self):
        self.t = time.time()

    def render_time(self):
        t = time.time() - self.t
        return '%.3f' % (t,)

    def render_txt(self):
        return '(%d, %d) | [%s] | [%s]' % (self.cursor_x, self.cursor_y, self.key, self.text)


ctrl = Control()


# %%
def flip():
    # background
    surf = pg.Surface(SCREEN.get_size())
    surf = surf.convert()
    surf.fill('darkgreen')
    if BACKGROUND_IMG:
        surf.blit(BACKGROUND_IMG, (0, 0))

    # center timing text
    # Clock
    text = FONTs[32].render(f'{time.ctime()}', True, 'white')
    rect = text.get_rect()
    rect.center = (surf.get_width()//2, surf.get_height()//2)
    surf.blit(text, rect)

    # Manual
    text = FONTs[32].render('Press k to start logging thread', True, 'yellow')
    rect = text.get_rect()
    rect.center = (surf.get_width()//2, surf.get_height()//4*3)
    surf.blit(text, rect)

    # bottom text
    # Mouse and keyboard input
    text = FONTs[24].render(ctrl.render_txt(), True, 'white')
    rect = text.get_rect()
    rect.center = (surf.get_width()//2, surf.get_height()-rect.height)
    surf.blit(text, rect)

    # upper left text
    # seconds since start
    text = FONTs[24].render(ctrl.render_time(), True, 'white')
    rect = text.get_rect()
    surf.blit(text, rect)

    # blit
    dt = CLOCK.tick(60) / 1000
    SCREEN.blit(surf, (0, 0))

    pg.display.flip()
    return


def handle_key_k():
    '''Press the key "k" to start the 10 seconds thread.'''
    print('handle_key_k')
    t = Thread(target=HWL.work, )
    t.start()
    return


def handle_quit_intention(evt):
    '''Hand quit intention'''
    if evt in [pg.K_q, pg.K_ESCAPE]:
        pg.quit()


def check_events():
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            pg.quit()

        elif evt.type == pg.MOUSEMOTION:
            ctrl.cursor_x, ctrl.cursor_y = evt.pos

        elif evt.type == pg.TEXTINPUT:
            ctrl.text = evt.text

        elif evt.type in [pg.KEYDOWN, ]:
            ctrl.key = evt.unicode

            if evt.key == pg.K_k:
                handle_key_k()

            handle_quit_intention(evt.key)

        else:
            pass

    return


def main():
    try:
        while True:
            check_events()
            flip()
    except Exception as err:
        import traceback
        traceback.print_exc()
        print(err)
    finally:
        print('main done.')


# %% ---- 2026-11-18 ------------------------
# Play ground
if __name__ == '__main__':
    import sys
    sys.exit(main())


# %% ---- 2026-11-18 ------------------------
# Pending


# %% ---- 2026-11-18 ------------------------
# Pending
