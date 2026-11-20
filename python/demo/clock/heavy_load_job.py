"""
File: heavy_load_job.py
Author: Chuncheng Zhang
Date: 2026-11-18
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Simulate the heavy load job.

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2026-11-18 ------------------------
# Requirements and constants
import time
from loguru import logger

logger.add('log/heavy_load_job.log', rotation='1day')


# %% ---- 2026-11-18 ------------------------
# Function and class
class HeavyWorkLoad:
    length = 10
    step = 1
    running = False

    def work(self):
        '''Prevent from repeating startup'''
        if self.running:
            logger.error('Cannot repeat start.')
            return

        self.running = True

        tic = time.time()
        t = tic
        line = 'Start.'
        logger.info(line)

        while t < tic+self.length:
            line = f'{time.ctime()}'
            logger.debug(line)
            time.sleep(self.step)
            t = time.time()

        line = 'Safety stop.'
        logger.info(line)

        self.running = False
        return


# %% ---- 2026-11-18 ------------------------
# Play ground
if __name__ == '__main__':
    hwl = HeavyWorkLoad()
    hwl.work()


# %% ---- 2026-11-18 ------------------------
# Pending


# %% ---- 2026-11-18 ------------------------
# Pending
