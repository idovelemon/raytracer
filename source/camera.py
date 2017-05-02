#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved.
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Camera, control how to look at the scene
"""


import math
from vector import *


__all__ = ["Camera",]


class Camera(object):
    def __init__(self, pos, target, dist, fov, aspect):
        self.pos = pos
        self.target = target
        self.dist = dist
        self.fov = fov
        self.aspect = aspect
        self.view_height = 2 * dist * math.tan(fov/2.0)
        self.view_width = self.view_height * aspect

        look_at = target - pos
        look_at.normalize()
        self.view_center = pos + look_at * dist
        
        up = Vector(0.0, 1.0, 0.0)
        self.view_x_axis = Vector.cross(up, look_at)
        self.view_y_axis = Vector.cross(look_at, self.view_x_axis)

    def getPos(self):
        return self.pos

    def getTarget(self):
        return self.target

    def getDist(self):
        return self.dist

    def getFov(self):
        return self.fov

    def getAspect(self):
        return self.aspect

    def getViewWidth(self):
        return self.view_width

    def getViewHeight(self):
        return self.view_height

    def getViewCenter(self):
        return self.view_center

    def getViewXAxis(self):
        return self.view_x_axis

    def getViewYAxis(self):
        return self.view_y_axis


if __name__ == "__main__":
    c = Camera(Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 100.0), 1.0, 90.0, 800.0 / 600.0)
    print(c.getViewWidth())
    print(c.getViewHeight())
    print(c.getViewCenter().x)
    print(c.getViewCenter().y)
    print(c.getViewCenter().z)
    print(c.getViewXAxis().x)
    print(c.getViewXAxis().y)
    print(c.getViewXAxis().z)
    print(c.getViewYAxis().x)
    print(c.getViewYAxis().y)
    print(c.getViewYAxis().z)
