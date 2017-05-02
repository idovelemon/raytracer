#!/usr/bin/env python3.2


"""
    Demostrate render basic scene
"""


import multiprocessing
import random
import time

from camera import *
from color import *
from light import *
from material import *
from render import *
from sampler import *
from scene import *
from shade import *
from tracer import *
from vector import *
from window import *


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400


def render_many_balls():
    s = Scene()

    # Ambient Light
    ambient = AmbientLight(0.7, Color(1.0, 1.0, 1.0))
    s.setAmbientLight(ambient)

    # Squre area light
    mat = Material.createEmission(10.0, Color(1.0, 1.0, 1.0))
    shape = Squre(Vector(0.0, 30.0, 0.0), 40.0, Vector(0.0, -1.0, 0.0), mat)
    shape.setEp(0.00001)
    s.addShape(shape)
    area_light = AreaLight(shape, MultiJitteredSampler(), 64)
    s.addAreaLight(area_light)

    # Balls
    mat = Material.createMirror(0.1, 0.5, Color(1.0, 0.0, 0.0), 0.3, Color(1.0, 1.0, 1.0))
    shape = Sphere(Vector(-8.1, 0.0, 8.1), 8.0, mat)
    shape.setEp(0.00001)
    s.addShape(shape)
    mat = Material.createMirror(0.1, 0.5, Color(0.0, 1.0, 0.0), 0.3, Color(1.0, 1.0, 1.0))
    shape = Sphere(Vector(8.1, 0.0, 8.1), 8.0, mat)
    shape.setEp(0.00001)
    s.addShape(shape)
    mat = Material.createMirror(0.1, 0.5, Color(0.0, 0.0, 1.0), 0.3, Color(1.0, 1.0, 1.0))
    shape = Sphere(Vector(8.1, 0.0, -8.1), 8.0, mat)
    shape.setEp(0.00001)
    s.addShape(shape)
    mat = Material.createMirror(0.1, 0.5, Color(1.0, 1.0, 0.0), 0.3, Color(1.0, 1.0, 1.0))
    shape = Sphere(Vector(-8.1, 0.0, -8.1), 8.0, mat)
    shape.setEp(0.00001)
    s.addShape(shape)  

    # Bottom Squre
    mat = Material.createGlossy(0.6, 0.8, Color(1.0, 1.0, 1.0), 0.2, Color(0.0, 0.0, 1.0), 1.0)
    shape = Squre(Vector(0.0, -8.0, 0.0), 400.0, Vector(0.0, 1.0, 0.0), mat)
    shape.setEp(0.00001)
    s.addShape(shape)
    
    c = Camera(Vector(0.0, 60.0, -110.0), Vector(0.0, 0.0, 0.0), 0.01, 170.0, 1.0 * SCREEN_WIDTH / SCREEN_HEIGHT)
    
    w = Window(SCREEN_WIDTH, SCREEN_HEIGHT)

    sd = Phong(MultiJitteredSampler())
    sd.setAOSamplerNum(100)
    sd.setEnableAO(True)
    
    t = Tracer(s, c, SCREEN_WIDTH, SCREEN_HEIGHT, sd, 10, MultiJitteredSampler(), 16)
    render = Render(w, t)
    render.render()


if __name__ == "__main__":
    render_many_balls()
