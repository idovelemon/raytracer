#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Scene description, hold some basic shape
"""


import math
from abc import ABCMeta, abstractmethod

from color import *
from light import *
from material import *
from vector import *


__all__ = ["Ray", "Shape", "Sphere", "Scene", "Plane", "Triangle", "Squre"]


class Ray:
    """
        Ray used to cast ray to tracer
    """
    
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction


class Shape(metaclass=ABCMeta):
    """
        Basic shape interface, all subclass must implement isIntersection method
    """
    
    SPHERE = 0
    PLANE = 1
    TRIANGLE = 2
    SQURE = 3
    
    def __init__(self, shapeType, material):
        self.shape_type = shapeType
        self.material = material
        self.ep = 0.0
        self.enable_cast_shadow = True

    def getMaterial(self):
        return self.material

    def getEp(self):
        return self.ep

    def setEp(self, ep):
        self.ep = ep
        
    def setEnableCastShadow(self, enable):
        self.enable_cast_shadow = enable

    def getEnableCastShadow(self):
        return self.enable_cast_shadow
    
    @abstractmethod
    def isIntersection(self, ray):
        """
            Return (isIntersection, intersectionPoint)
        """
        pass

    @abstractmethod
    def genNormal(self, point):
        """
           Return normal of intersection point 
        """
        pass


class Sphere(Shape):
    """
        Sphere gemometry
    """
    
    def __init__(self, position, radius, material):
        super().__init__(Shape.SPHERE, material)
        self.p = position
        self.r = radius

    def isIntersection(self, ray):
        a = Vector.dot(ray.d, ray.d)
        b = 2 * Vector.dot(ray.o - self.p, ray.d)
        c = Vector.dot((ray.o - self.p), (ray.o - self.p)) - (self.r * self.r)
        
        d = b * b - 4 * a * c
        if d < 0:
            return False, Vector(0.0, 0.0, 0.0), 0.0
        elif d == 0:
            t = -b / (2 * a)
            q = ray.o + ray.d * t
            if (t > 0.0):
                return True, q, t
            else:
                return False, Vector(0.0, 0.0, 0.0), 0.0
        else:
            t0 = (-b + math.sqrt(d)) / (2 * a)
            t1 = (-b - math.sqrt(d)) / (2 * a)
            if t0 < 0.0 and t1 < 0.0:
                return False, Vector(0.0, 0.0, 0.0), 0.0
            elif t0 < 0.0 and t1 > 0.0:
                q = ray.o + ray.d * t1
                return True, q, t1
            elif t0 > 0.0 and t1 < 0.0:
                q = ray.o + ray.d * t0
                return True, q, t0
            else:
                t = 0.0
                if t0 > t1:
                    t = t1
                else:
                    t = t0
                q = ray.o + ray.d * t
                return True, q, t
            
    def genNormal(self, point):
        normal = point - self.p
        normal.normalize()
        return normal


class Plane(Shape):
    """
        Plane gemometry
    """

    def __init__(self, pos, normal, material):
        super().__init__(Shape.PLANE, material)
        self.pos = pos
        self.normal = normal

    def isIntersection(self, ray):
        t = self.pos - ray.o
        a = Vector.dot(t, self.normal)
        b = Vector.dot(ray.d, self.normal)
        if abs(b) < 0.0001:
            return False, Vector(0.0, 0.0, 0.0), 0.0
        else:
            t = a / b
            if t > 0.0:
                return True, ray.o + ray.d * t, t
            else:
                return False, Vector(0.0, 0.0, 0.0), 0.0

    def genNormal(self, point):
        return self.normal


class Triangle(Shape):
    def __init__(self, v0, v1, v2, material):
        super().__init__(Shape.TRIANGLE, material)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        e0 = v1 - v0
        e0.normalize()
        e1 = v2 - v0
        e1.normalize()
        self.normal = Vector.cross(e0, e1)

    def isIntersection(self, ray):
        a = self.v0.x - self.v1.x
        b = self.v0.x - self.v2.x
        c = ray.d.x
        d = self.v0.x - ray.o.x

        e = self.v0.y - self.v1.y
        f = self.v0.y - self.v2.y
        g = ray.d.y
        h = self.v0.y - ray.o.y

        i = self.v0.z - self.v1.z
        j = self.v0.z - self.v2.z
        k = ray.d.z
        l = self.v0.z - ray.o.z

        m = f * k - g * j
        n = h * k - g * l
        p = f * l - h * j
        q = g * i - e * k
        s = e * j - f * i

        if abs(a * m + b * q + c * s) < 0.0001:
            return False, Vector(0, 0, 0), 0.0
        
        inv_denom = 1.0 / (a * m + b * q + c * s)

        e1 = d * m - b * n - c * p
        beta = e1 * inv_denom

        if beta < 0.0:
            return False, Vector(0, 0, 0), 0.0

        r = e * l - h * i
        e2 = a * n + d * q + c * r
        gamma = e2 * inv_denom

        if gamma < 0.0:
            return False, Vector(0.0, 0.0, 0.0), 0.0

        if beta + gamma > 1.0:
            return False, Vector(0.0, 0.0, 0.0), 0.0

        e3 = a * p - b * r + d * s
        t = e3 * inv_denom

        if t < 0.0001:
            return False, Vector(0.0, 0.0, 0.0), 0.0

        return True, ray.o + ray.d * t, t

    def genNormal(self, point):
        return self.normal


class Squre(Shape):
    def __init__(self, p, s, n, material):
        super().__init__(Shape.SQURE, material)
        self.pos = p
        self.size = s
        self.normal = n
        up = Vector(0.0, 1.0, 0.0)
        if abs(Vector.dot(n, up)) < 0.9999:
            right = Vector.cross(up, self.normal)
            right.normalize()
            up = Vector.cross(self.normal, right)
            up.normalize()
        else:
            if n.y > 0.0:
                right = Vector(1.0, 0.0, 0.0)
                up = Vector(0.0, 0.0, -1.0)
            else:
                right = Vector(-1.0, 0.0, 0.0)
                up = Vector(0.0, 0.0, 1.0)

        half_size = self.size / 2.0
        t0 = self.pos - right * half_size + up * half_size
        t1 = self.pos + right * half_size + up * half_size
        t2 = self.pos + right * half_size - up * half_size
        t3 = self.pos - right * half_size - up * half_size                       
        self.tr0 = Triangle(t0, t1, t2, None)
        self.tr1 = Triangle(t0, t2, t3, None)
        self.right = right
        self.up = up

    def isIntersection(self, ray):
        b,p,t = self.tr0.isIntersection(ray)
        if b is True:
            return b,p,t
        b,p,t = self.tr1.isIntersection(ray)
        if b is True:
            return b,p,t
        return False, Vector(0,0,0), 0.0

    def genNormal(self, shadeInfo):
        return self.normal

    def genSamplerPoint(self, sampler):
        sampler = sampler - Vector2(0.5, 0.5)
        return self.pos + self.right * (sampler.x * self.size) + self.up * (sampler.y * self.size)

    def getArea(self):
        return self.size * self.size
    

class Scene(object):
    """
        Scene, hold all the geometry
    """

    def __init__(self):
        self.shapes = []
        self.ambient_light = None
        self.parallel_light = None
        self.env_light = None
        self.area_lights = []

    def addShape(self, shape):
        self.shapes.append(shape)

    def getAllShapes(self):
        return self.shapes

    def setAmbientLight(self, light):
        self.ambient_light = light

    def getAmbientLight(self):
        return self.ambient_light

    def setParallelLight(self, light):
        self.parallel_light = light

    def getParallelLight(self):
        return self.parallel_light

    def addAreaLight(self, light):
        self.area_lights.append(light)

    def getAreaLights(self):
        return self.area_lights

    def setEnvLight(self, light):
        self.env_light = light

    def getEnvLight(self):
        return self.env_light

    def isIntersection(self, ray, ep = 0.0):
        for shape in self.shapes:
            b,p,t = shape.isIntersection(ray)
            if b is True:
                if t > ep:
                    return True
        return False

    def isTwoPointsVisible(self, p0, ep0, p1, ep1):
        d = p0 - p1
        l = d.length()
        l = l - ep0
        d.normalize()
        r = Ray(p1, d)
        for shape in self.shapes:
            b,p,t = shape.isIntersection(r)
            if b is True:
                if ep1 < t and t < l:
                    return False
        return True


if __name__ == "__main__":
    s = Sphere(Vector(0, 0, 0), 15.0, None)
    p = Plane(Vector(0, 0, 0), Vector(0.0, 1.0, 0.0), None)
    d = Vector(0.0, -1.0, 1.0)
    d.normalize()
    r = Ray(Vector(0, 10.0, 0.0), d)
    b,p,t = p.isIntersection(r)
    print(b)
    print(p.x)
    print(p.y)
    print(p.z)
