#!/usr/bin/env python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: Description of light properties of surface
"""


import math
from abc import ABCMeta, abstractmethod

from color import *
from vector import *

__all__ = ["MaterialBase", "AmbientMaterial", "DiffuseMaterial", "Material"]


class MaterialBase(object):
    AMBIENT = 0
    DIFFUSE = 1
    GLOSSY = 2
    EMISSION = 3
    MIRROR = 4
    
    def __init__(self, mat_type):
        self.type = mat_type

    def getType(self):
        return self.type

    @abstractmethod
    def getBRDF(self, p, n, wi, wo):
        pass


class AmbientMaterial(MaterialBase):
    def __init__(self, ka, cd):
        super().__init__(MaterialBase.AMBIENT)
        self.ka = ka
        self.cd = cd

    def getKa(self):
        return self.ka

    def getCd(self):
        return self.cd

    def getBRDF(self, p, n, wi, wo):
        return self.cd * self.ka


class DiffuseMaterial(MaterialBase):
    def __init__(self, kd, cd):
        super().__init__(MaterialBase.DIFFUSE)
        self.kd = kd
        self.cd = cd

    def getKd(self):
        return self.kd

    def getCd(self):
        return self.cd

    def getBRDF(self, p, n, wi, wo):
        return self.cd * (self.kd / math.pi)


class GlossyMaterial(MaterialBase):
    def __init__(self, ks, cs, e):
        super().__init__(MaterialBase.GLOSSY)
        self.ks = ks
        self.cs = cs
        self.e = e

    def getKs(self):
        return self.ks

    def getCs(self):
        return self.cs

    def getE(self):
        return self.e

    def getBRDF(self, p, n, wi, wo):
        r = Vector.reflect(n, wi)
        v = Vector.dot(r, wo)
        v = max(0.0, v)
        v = math.pow(v, self.e)
        return self.cs * (self.ks * v)


class EmissionMaterial(MaterialBase):
    def __init__(self, ke, ce):
        super().__init__(MaterialBase.EMISSION)
        self.ke = ke
        self.ce = ce

    def getBRDF(self, p, n, wi, wo):
        pass

    def getKe(self):
        return self.ke

    def getCe(self):
        return self.ce


class MirrorMaterial(MaterialBase):
    def __init__(self, km, cm):
        super().__init__(MaterialBase.MIRROR)
        self.km = km
        self.cm = cm

    def getBRDF(self, p, n, wi, wo):
        return self.cm * self.km

    def getKm(self):
        return self.km

    def getCm(self):
        return self.cm


class Material(object):
    @staticmethod
    def createGlossy(ka, kd, cd, ks, cs, e):
        ambient = AmbientMaterial(ka, cd)
        diffuse = DiffuseMaterial(kd, cd)
        glossy = GlossyMaterial(ks, cs, e)
        return Material(ambient, diffuse, glossy, None, None)

    def createMirror(ka, kd, cd, km, cm):
        ambient = AmbientMaterial(ka, cd)
        diffuse = DiffuseMaterial(kd, cd)
        mirror = MirrorMaterial(km, cm)
        return Material(ambient, diffuse, None, None, mirror)

    def createEmission(ke, ce):
        emission = EmissionMaterial(ke, ce)
        return Material(None, None, None, emission, None)
        
    def __init__(self, ambient_mat, diffuse_mat,
                 glossy_mat, emii_mat, mirror_mat):
        self.ambient_mat = ambient_mat
        self.diffuse_mat = diffuse_mat
        self.glossy_mat = glossy_mat
        self.emii_mat = emii_mat
        self.mirror_mat = mirror_mat

    def getAmbient(self):
        return self.ambient_mat

    def getDiffuse(self):
        return self.diffuse_mat

    def getGlossy(self):
        return self.glossy_mat

    def getEmission(self):
        return self.emii_mat

    def getMirror(self):
        return self.mirror_mat


if __name__ == "__main__":
    mat = Material.create(0.1, 0.4, Color(0.5, 0.5, 0.5), 0.3, Color(0.5, 0.5, 0.5), 20)
    mat = Material.createEmission(1.0, Color(1.0, 1.0, 1.0))
