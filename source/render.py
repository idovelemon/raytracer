#!/usr/bin/env python3.2


"""
    Declartion:Copyright (c), by i_dovelemon, 2017. All right reserved.
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Render the scene
"""


import multiprocessing

import tracer
import window


__all__ = ["Render",]


class Render(object):
    def __init__(self, window, tracer, img_name="result.bmp"):
        self.window = window
        self.tracer = tracer
        self.img_name = img_name

    def render(self):
        color_buf = []
        for index in range(self.window.getWidth() * self.window.getHeight() * 3):
            color_buf.append(0.0)
        self.tracer.trace(color_buf)
        self.window.update(color_buf)
        self.window.save(self.img_name, color_buf,
                         self.window.getWidth(), self.window.getHeight())
