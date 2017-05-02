#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Ray tracer, it will trace scene and display the result
"""


from camera import *
from color import *
from light import *
from material import *
from sampler import *
from scene import *
from shade import *
from vector import *
from window import *

    
class Tracer(object):
    def __init__(self, scene, camera, width, height, shader, depth, sampler, sampler_num):
        self.scene = scene
        self.camera = camera
        self.width = width
        self.height = height
        self.shader = shader
        self.depth = depth
        self.sampler = sampler
        self.sampler_num = sampler_num
        self.trace_ok = False

    def getDepth(self):
        return self.depth

    def isTraceOk(self):
        return self.trace_ok
    
    def trace(self, color_buf):
        print("Tracer Process: Start")
        for y in range(self.height):
            for x in range(self.width):
                color = Color(0.0,0.0, 0.0)
                self.sampler.genSamplersInUnitSqure(self.sampler_num)
                for sampler in self.sampler.getSamplers():
                    trace_x = x - 0.5 + sampler.x
                    trace_y = y - 0.5 + sampler.y
                    ray = self.__genRay(trace_x, trace_y)
                    shadeInfo = self.hit_object(ray)
                    color = color + self.calcColor(ray, shadeInfo)
                color = color * (1.0 / self.sampler_num)
                color_buf[y * self.width * 3 + x * 3 + 0] = color.r
                color_buf[y * self.width * 3 + x * 3 + 1] = color.g
                color_buf[y * self.width * 3 + x * 3 + 2] = color.b
            ratio = 100.0 * y / self.height
            print("Tracer Process: %f" % (ratio,))
        print("Tracer Process: End")

    def __genRay(self, x, y):
        ratio_x = 1.0 * x / self.width - 0.5
        ratio_y = 0.5 - 1.0 * y / self.height
        scene_x = ratio_x * self.camera.getViewWidth()
        scene_y = ratio_y * self.camera.getViewHeight()
        target = self.camera.getViewCenter() + self.camera.getViewXAxis() * scene_x + self.camera.getViewYAxis() * scene_y
        direction = target - self.camera.getPos()
        direction.normalize()
        return Ray(self.camera.getPos(), direction)

    def hit_object(self, ray, ep = 0.0):
        shadeInfo = None
        shapes = self.scene.getAllShapes()
        min_length = 10000000.0
        for shape in shapes:
            isIntersected, point, t = shape.isIntersection(ray)
            if t < ep:
                continue # Avoid self intersection
            if isIntersected is True:
                cur_len = (point - ray.o).length()
                if cur_len < min_length:
                    min_length = cur_len
                    shadeInfo = self.__collect_shade_info(shape, point, ray)
        return shadeInfo

    def calcColor(self, ray, shadeInfo):
        color = Color(0.0, 0.0, 0.0)
        if shadeInfo is None:
            return color
        
        color = self.shader.shade(shadeInfo)
        return color

    def __collect_shade_info(self, shape, point, ray):
        shadeInfo = ShadeInfo()
        shadeInfo.normal = shape.genNormal(point)
        shadeInfo.material = shape.getMaterial()
        shadeInfo.scene = self.scene
        shadeInfo.point = point
        shadeInfo.camera = self.camera
        shadeInfo.ep = shape.getEp()
        shadeInfo.tracer = self
        shadeInfo.ray = ray
        return shadeInfo


if __name__ == "__main__":
    pass
