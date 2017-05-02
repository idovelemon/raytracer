#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved.
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: RGB color
"""


import math


__all__ = ["Color",]


class Color(object):
    def __init__(self, r,g ,b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, c):
        result = Color(0.0, 0.0, 0.0)
        result.r = self.r + c.r
        result.g = self.g + c.g
        result.b = self.b + c.b
        return result
    
    def __mul__(self, f):
        result = Color(0.0, 0.0, 0.0)
        if isinstance(f, float):
            result.r = self.r * f
            result.g = self.g * f
            result.b = self.b * f
        elif isinstance(f, Color):
            result.r = self.r * f.r
            result.g = self.g * f.g
            result.b = self.b * f.b
        else:
            raise TypeError
        return result

    def getColorStr(self):
        s = "#"
        value = math.floor(self.r * 255)
        t = format(value, "02x")
        s = s + t
        
        value = math.floor(self.g * 255)
        t = format(value, "02x")
        s = s + t

        value = math.floor(self.b * 255)
        t = format(value, "02x")
        s = s + t
        
        return s


if __name__ == "__main__":
    c = Color(0.5, 0.0, 0.0)
    print(c.getColorStr())
