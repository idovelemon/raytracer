#!/usr/bin/env


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved.
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Light to illuminate scene
"""

import math

from color import *


class AmbientLight(object):
    def __init__(self, k, c):
        self.k = k
        self.c = c

    def getLightCoefficient(self):
        return self.k

    def getLightColor(self):
        return self.c * self.k


class ParallelLight(object):
    def __init__(self, k, c, d):
        self.k = k
        self.c = c
        self.d = d

    def getLightColor(self):
        return self.c * self.k

    def getLightDir(self):
        return self.d


class AreaLight(object):
    def __init__(self, shape, sampler, sampler_num):
        self.shape = shape
        self.sampler = sampler
        self.sampler_num = sampler_num

    def getPDF(self):
        return 1.0 / self.shape.getArea()
        
    def getShape(self):
        return self.shape

    def getSamplers(self):
        self.sampler.genSamplersInUnitSqure(self.sampler_num)
        samplers = self.sampler.getSamplers()
        sampler_point_in_area = []
        for sampler in samplers:
            sampler_point_in_area.append(self.shape.genSamplerPoint(sampler))
        return sampler_point_in_area

class EnvLight(object):
    def __init__(self, kenv, cenv, sampler, sampler_num):
        self.kenv = kenv
        self.cenv = cenv
        self.sampler = sampler
        self.sampler_num = sampler_num

    def getPDF(self, cos):
        return cos / math.pi

    def getSamplers(self):
        self.sampler.genSamplersInUnitSqure(self.sampler_num)
        self.sampler.mapToHemiSphere()
        return self.sampler.getSamplers()

    def getLightColor(self):
        return self.cenv * self.kenv


if __name__ == "__main__":
    ambient = AmbientLight(0.1, Color(1.0, 1.0, 1.0))
    print(ambient.c.getColorStr())
