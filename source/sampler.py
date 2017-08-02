#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemeon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Used to sample square
"""


import math
import random
from abc import ABCMeta, abstractmethod

from color import *
from vector import *
from window import *


__all__ = ["Sampler", "RandomSampler", "JitteredSampler", "NRookSampler", "MultiJitteredSampler"]


class Sampler(metaclass=ABCMeta):
    RANDOM  = 0
    JITTERED = 1
    NROOK = 2
    MULTIJITTERED = 3
    HAMMERSLEY = 4
    
    def __init__(self, sampler_type):
        self.type = sampler_type
        self.samplers = []

    @abstractmethod
    def genSamplersInUnitSqure(self, num):
        pass

    def mapToHemiSphere(self, e):
        for i in range(len(self.samplers)):
            self.samplers[i].x = 2 * math.pi * self.samplers[i].x
            t = pow(1 - self.samplers[i].y, 1 / (e + 1))
            self.samplers[i].y = math.acos(t)
            
    def getSamplers(self):
        return self.samplers


class RandomSampler(Sampler):
    def __init__(self):
        super().__init__(Sampler.RANDOM)

    def genSamplersInUnitSqure(self, num):
        self.samplers = []
        for i in range(num):
            x = random.random()
            y = random.random()
            self.samplers.append(Vector2(x,y))


class JitteredSampler(Sampler):
    def __init__(self):
        super().__init__(Sampler.JITTERED)

    def isSqure(self, t):
        q = math.floor(t)
        if t - q < 0.0001:
            return True
        return False
    
    def genSamplersInUnitSqure(self, num):
        self.samplers = []
        t = math.sqrt(num)
        if self.isSqure(t):
            step = 1.0 / t
            for i in range(int(t)):
                for j in range(int(t)):
                    x = j * step + random.random() * step
                    y = i * step + random.random() * step
                    self.samplers.append(Vector2(x, y))
        else:
            raise ValueError


class NRookSampler(Sampler):
    def __init__(self):
        super().__init__(Sampler.NROOK)

    def genSamplersInUnitSqure(self, num):
        self.samplers = []
        step = 1.0 / num
        col_list = []
        for i in range(num):
                col_list.append(i)
        for i in range(num):
            r = random.randint(0, len(col_list) - 1)
            col = col_list[r]
            x = col * step + random.random() * step
            y = i * step + random.random() * step
            col_list.remove(col)
            self.samplers.append(Vector2(x, y))


class MultiJitteredSampler(Sampler):
    def __init__(self):
        super().__init__(Sampler.MULTIJITTERED)

    def isSqure(self, t):
        q = math.floor(t)
        if t - q < 0.0001:
            return True
        return False        

    def genSamplersInUnitSqure(self, num):
        self.samplers = []
        t = math.sqrt(num)
        if self.isSqure(t) is False:
            raise ValueError
            return

        step = 1.0 / num
        
        col_lists = []
        row_lists = []
        for i in range(int(t)):
            col_lists.append([])
            row_lists.append([])
            for j in range(int(t)):
                col_lists[i].append(j)
                row_lists[i].append(j)

        for i in range(int(t)):
            for j in range(int(t)):
                col = col_lists[j][random.randint(0, len(col_lists[j]) - 1)]
                row = row_lists[i][random.randint(0, len(row_lists[i]) - 1)]
                x = j * t + col
                y = i * t + row
                x = x * step + random.random() * step
                y = y * step + random.random() * step
                self.samplers.append(Vector2(x, y))
                col_lists[j].remove(col)
                row_lists[i].remove(row)

class HammersleySampler(Sampler):
    def __init__(self):
        super().__init__(Sampler.MULTIJITTERED)

    def radicalInverseBase2(self, v):
        x = 0.0
        f = 0.5
        v = int(v)
        while v != 0:
            x += f * (v & 1)
            v = math.floor(v / 2)
            f *= 0.5
        return x
        
    def genSamplersInUnitSqure(self, num):
        self.samplers = []
        for i in range(num):
            x = i * 1.0 / num
            y = self.radicalInverseBase2(i)
            self.samplers.append(Vector2(x, y))

if __name__ == "__main__":
    def test_random():        
        w = Window(400, 400)
        s = RandomSampler()
        s.genSamplersInUnitSqure(256)
        samplers = s.getSamplers()
        for sampler in samplers:
            x = sampler.x * 400
            y = sampler.y * 400
            w.pixel(x, y, Color(0, 0, 0))
        w.update

    def test_jittered():
        w = Window(400, 400)
        s = JitteredSampler()
        s.genSamplersInUnitSqure(256)
        samplers = s.getSamplers()
        for sampler in samplers:
            x = sampler.x * 400
            y = sampler.y * 400
            w.pixel(x, y, Color(0, 0, 0))
        w.update

    def test_nrook():
        w = Window(400, 400)
        s = NRookSampler()
        s.genSamplersInUnitSqure(256)
        samplers = s.getSamplers()
        for sampler in samplers:
            x = sampler.x * 400
            y = sampler.y * 400
            w.pixel(x, y, Color(0, 0, 0))
        w.update

    def test_multijittered():
        w = Window(400, 400)
        s = MultiJitteredSampler()
        s.genSamplersInUnitSqure(256)
        samplers = s.getSamplers()
        for sampler in samplers:
            x = sampler.x * 400
            y = sampler.y * 400
            w.pixel(x, y, Color(0, 0, 0))
        w.update

    def test_hammersley():
        w = Window(400, 400)
        s = HammersleySampler()
        s.genSamplersInUnitSqure(256)
        samplers = s.getSamplers()
        color_buf = []
        for i in range(400):
            for j in range(400):
                color_buf.append(0.0) #r
                color_buf.append(0.0) #g
                color_buf.append(0.0) #b
        for sampler in samplers:
            x = sampler.x * 400
            y = sampler.y * 400
            color_buf[int(y) * 400 * 3 + int(x) * 3 + 0] = 1.0
            color_buf[int(y) * 400 * 3 + int(x) * 3 + 1] = 0.0
            color_buf[int(y) * 400 * 3 + int(x) * 3 + 2] = 0.0
        w.save("hammersley256.png", color_buf, 400, 400)
        
    #test_random()
    #test_jittered()
    #test_nrook()
    #test_multijittered()
    test_hammersley()
        

