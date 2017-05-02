#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved.
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Create a window and draw pixel on it
"""


import math
import time

import pygame
from pygame.locals import *


__all__ = ["Window",]


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def update(self, color_buf):
        pygame.init()
        surface = pygame.display.set_mode((self.width, self.height), 0, 24)
        cur_col = 0
        cur_row = 0        
        while True:
            is_quit = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_quit = True
                    break
            if is_quit is True:
                pygame.quit()
                break

            if cur_row >= self.height:
                pygame.display.update()
                continue
            
            # Display current tracer result
            r = math.floor(color_buf[cur_row * self.width * 3
                                    + cur_col * 3 + 0] * 255)
            g = math.floor(color_buf[cur_row * self.width * 3
                                    + cur_col * 3 + 1] * 255)
            b = math.floor(color_buf[cur_row * self.width * 3
                                    + cur_col * 3 + 2] * 255)
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
            surface.set_at((cur_col,cur_row), (r,g,b))
            cur_col = cur_col + 1
            if cur_col >= self.width:
                cur_col = 0
                cur_row = cur_row + 1
            
            pygame.display.update()

    def save(self, img_name, color_buf, width, height):
        surface = pygame.Surface((width, height))
        for y in range(self.height):
            for x in range(self.width):
                r = math.floor(color_buf[y * self.width * 3 + x * 3 + 0] * 255)
                g = math.floor(color_buf[y * self.width * 3 + x * 3 + 1] * 255)
                b = math.floor(color_buf[y * self.width * 3 + x * 3 + 2] * 255)
                if r > 255:
                    r = 255
                if g > 255:
                    g = 255
                if b > 255:
                    b = 255
                surface.set_at((x,y), (r,g,b))
        pygame.image.save(surface, img_name)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height


if __name__ == "__main__":
    pass
