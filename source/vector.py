#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Math library for ray tracer
"""


import math


__all__ = ["Vector", "Vector2"]


class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, v):
        return Vector2(self.x - v.x, self.y - v.y)


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def dot(v0, v1):
        return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

    @staticmethod
    def cross(v0, v1):
        return Vector(v0.y * v1.z - v0.z * v1.y,
                      v0.z * v1.x - v0.x * v1.z,
                      v0.x * v1.y - v0.y * v1.x)

    @staticmethod
    def reflect(n, l):
        ln = Vector.dot(n, l)
        ln = 2 * ln
        n = n * ln
        return n - l
    
    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, v):
        return Vector(self.x * v.x, self.y * v.y, self.z * v.z)

    def __mul__(self, num):
        return Vector(self.x * num, self.y * num, self.z * num)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def lengthSqure(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
        
    def normalize(self):
        l = self.length()
        if l == 0.0:
            l = 1.0
        self.x /= l
        self.y /= l
        self.z /= l


if __name__ == "__main__":
    d = Vector(-1, -1, 1)
    d.normalize()
    d = d * (-1)
    a = Vector(1.0, 0.0, 0.0)
    cos = Vector.dot(d,d)
    print(cos)
