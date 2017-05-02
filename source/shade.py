#!/usr/bin/env


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/02
    Brief: To calculate color of a point in surface
"""


import math
from abc import ABCMeta, abstractmethod

from color import *
from material import *
from sampler import *
from scene import *
from vector import *


__all__ = ["ShadeInfo", "Shader", "Matte", "Phong"]


class ShadeInfo(object):
    def __init__(self):
        self.normal = None
        self.material = None
        self.scene = None
        self.point = None
        self.camera = None
        self.tracer = None
        self.ep = 0.0
        self.depth = 0
        self.ray = None

    def setNormal(self, normal):
        self.normal = normal

    def getNormal(self):
        return self.normal

    def setMaterial(self, material):
        self.material = material

    def getMaterial(self):
        return self.material

    def setScene(self, scene):
        self.scene = scene
        
    def getScene(self):
        return self.scene

    def setPoint(self, p):
        self.point = p

    def getPoint(self):
        return self.point

    def setCamera(self,camera):
        self.camera = camera

    def getCamera(self):
        return self.camera

    def setTracer(self, tracer):
        self.tracer = tracer

    def getTracer(self):
        return self.tracer

    def setEp(self, ep):
        self.ep = ep

    def getEp(self):
        return self.ep

    def setDepth(self, depth):
        self.depth = depth

    def getDepth(self):
        return self.depth

    def setRay(self, r):
        self.ray = d

    def getRay(self):
        return self.ray


class Shader(metaclass=ABCMeta):
    MATTE = 0
    PHONG = 1
    
    def __init__(self, shade_type, ao_sampler):
        self.shade_type = shade_type
        self.ao_sampler = ao_sampler
        self.ao_sampler_num = 256
        self.enable_ao = False

    def setAOSamplerNum(self, num):
        self.ao_sampler_num = num

    def setEnableAO(self, enable):
        self.enable_ao = enable

    @abstractmethod
    def shade(self, shadeInfo):
        """
            Return result color
        """
        pass


class Matte(Shader):
    def __init__(self, ao_sampler):
        super().__init__(Shader.MATTE, ao_sampler)

    def shade(self, shadeInfo):
        ambient_mat = shadeInfo.getMaterial().getAmbient()
        diffuse_mat = shadeInfo.getMaterial().getDiffuse()
        normal = shadeInfo.getNormal()
        scene = shadeInfo.getScene()
        ambient_color = self.__ambient_shade(ambient_mat.getBRDF(shadeInfo),
                                            scene)
        diffuse_color = self.__diffuse_shade(normal,
                                            diffuse_mat.getBRDF(shadeInfo),
                                            scene)
        return ambient_color + diffuse_color

    def __ambient_shade(self, brdf, scene):
        ambient_light = scene.getAmbientLight()
        return ambient_light.getLightColor() * brdf

    def __diffuse_shade(self, normal, brdf, scene):
        parallel_light = scene.getParallelLight()
        parallel_light_dir = parallel_light.getLightDir() * (-1)
        
        cos = Vector.dot(parallel_light_dir, normal)
        if cos < 0.0:
            return Color(0.0, 0.0, 0.0)

        parallel_light_color = parallel_light.getLightColor()
        return parallel_light_color * brdf * cos


class Phong(Shader):
    def __init__(self, ao_sampler):
        super().__init__(Shader.PHONG, ao_sampler)

    def shade(self, shadeInfo):
        emission_mat = shadeInfo.getMaterial().getEmission()
        if emission_mat is not None:
            emission_color = emission_mat.getCe() * emission_mat.getKe()
            return emission_color

        # Direct Lighting
        result_direct_color = self.__direct(shadeInfo)

        # InDirect Lighting
        result_indirect_color = self.__indirect(shadeInfo)

        return result_direct_color + result_indirect_color


    def __direct(self, shadeInfo):
        # Environment Light
        result_env_color = self.__env_light(shadeInfo)
            
        # Ambient Light
        result_ambient_color = self.__ambient_light(shadeInfo)

        # Parallel Light
        result_parallel_color = self.__parallel_light(shadeInfo)

        # Area Light
        result_area_color = self.__area_light(shadeInfo)

        return (result_env_color + result_ambient_color
                + result_parallel_color + result_area_color)

    def __indirect(self, shadeInfo):
        result_indirect_color = Color(0.0, 0.0, 0.0)
        
        if shadeInfo.material.getMirror() is not None:
            if shadeInfo.depth < shadeInfo.tracer.getDepth():
                reflect_dir = Vector.reflect(shadeInfo.normal,
                                             shadeInfo.ray.d * (-1))
                reflect_ray = Ray(shadeInfo.point, reflect_dir)
                new_shade_info = shadeInfo.tracer.hit_object(reflect_ray,
                                                             shadeInfo.ep)
                if new_shade_info is not None:
                    new_shade_info.depth = shadeInfo.depth + 1
                    incident_color = shadeInfo.tracer.calcColor(reflect_ray,
                                                                new_shade_info)
                    mirror_brdf = shadeInfo.material.getMirror().getBRDF(
                        None, None, None, None
                        )
                    result_indirect_color = incident_color * mirror_brdf
        
        return result_indirect_color
    
    def __env_light(self, shadeInfo):
        if shadeInfo.scene.getEnvLight() is None:
            return Color(0.0, 0.0, 0.0)

        env_light = shadeInfo.scene.getEnvLight()
        samplers = env_light.getSamplers()
        to_eye = shadeInfo.camera.getPos() - shadeInfo.point
        to_eye.normalize()        

        # Calculate orthonormal basie
        w = shadeInfo.normal
        u = Vector.cross(Vector(0.0072, 1.0, 0.0034), w)  # slightly jitter up vector
        u.normalize()
        v = Vector.cross(w, u)

        # Calculate samplers on hemisphere and store the direction
        hemi_sphere_samplers=[]
        for i in range(self.ao_sampler_num):
            cos_phi = math.cos(samplers[i].x)
            sin_phi = math.sin(samplers[i].x)
            cos_theta = math.cos(samplers[i].y)
            sin_theta = math.sin(samplers[i].y)
            pu = sin_theta * cos_phi
            pv = sin_theta * sin_phi
            pw = cos_theta
            direction = u * pu + v * pv + w * pw
            hemi_sphere_samplers.append(direction)

        result_env_colors = Color(0.0, 0.0, 0.0)
        env_light_color = env_light.getLightColor()
        diffuse_brdf = shadeInfo.material.getDiffuse().getBRDF(
            None, None, None, None
            )
        
        for sampler in hemi_sphere_samplers:
            r = Ray(shadeInfo.point, sampler)
            if shadeInfo.scene.isIntersection(r, shadeInfo.ep) is False:
                cos = Vector.dot(shadeInfo.normal, sampler)
                pdf = env_light.getPDF(cos)

                # Diffuse
                diffuse_color = env_light_color * diffuse_brdf * (cos / pdf)
                result_env_colors = result_env_colors + diffuse_color

                # Glossy
                glossy_color = Color(0.0, 0.0, 0.0)
                if shadeInfo.material.getGlossy() is not None:
                    glossy_brdf = shadeInfo.material.getGlossy().getBRDF(
                        shadeInfo.point, shadeInfo.normal, sampler, to_eye
                        )
                    glossy_color = env_light_color * glossy_brdf * (cos / pdf)
                    result_env_colors = result_env_colors + glossy_color

        result_env_colors = result_env_colors * (1.0 / len(hemi_sphere_samplers))
        return result_env_colors

    def __ambient_light(self, shadeInfo):
        if shadeInfo.scene.getAmbientLight() is None:
            return Color(0.0, 0.0, 0.0)
        ambient_ratio = self.__ambient_occluder__(shadeInfo)
        ambient_color = self.__ambient_shade__(shadeInfo)
        ambient_color = ambient_color * ambient_ratio
        return ambient_color

    def __parallel_light(self, shadeInfo):
        if shadeInfo.scene.getParallelLight() is None:
            return Color(0.0, 0.0, 0.0)

        is_in_shadow = self.__check_in_parallel_light_shadow__(shadeInfo)
        if is_in_shadow is True:
            return Color(0.0, 0.0, 0.0)

        diffuse_color = Color(0.0, 0.0, 0.0)
        glossy_color = Color(0.0, 0.0, 0.0)

        parallel_light = shadeInfo.scene.getParallelLight()
        parallel_light_color = parallel_light.getLightColor()
        light_dir = parallel_light.getLightDir() * (-1)
        cos = Vector.dot(light_dir, shadeInfo.normal)
        if cos < 0.0:
            return Color(0.0, 0.0, 0.0)

        # Diffuse
        diffuse_brdf = shadeInfo.material.getDiffuse().getBRDF(
            None, None, None, None
            )
        diffuse_color = parallel_light_color * diffuse_brdf * cos

        # Glossy
        glossy_color = Color(0.0, 0.0, 0.0)
        if shadeInfo.material.getGlossy() is not None:
            to_eye = shadeInfo.camera.getPos() - shadeInfo.point
            to_eye.normalize()
            glossy_brdf = shadeInfo.material.getGlossy().getBRDF(
                shadeInfo.point, shadeInfo.normal, light_dir, to_eye
                )
            glossy_color = parallel_light_color * glossy_brdf * cos

        return diffuse_color + glossy_color

    def __area_light(self, shadeInfo):
        to_eye = shadeInfo.camera.getPos() - shadeInfo.point
        to_eye.normalize()
        diffuse_brdf = shadeInfo.material.getDiffuse().getBRDF(
            None, None, None, None
            )
        
        result_areas = Color(0.0, 0.0, 0.0)
        area_lights = shadeInfo.scene.getAreaLights()
        for area_light in area_lights:
            result_area = Color(0.0, 0.0, 0.0)
            area_light_samplers = area_light.getSamplers()
            for area_light_sampler in area_light_samplers:
                visibility = shadeInfo.scene.isTwoPointsVisible(
                    shadeInfo.point,shadeInfo.ep, area_light_sampler,
                    area_light.getShape().getEp()
                    )
                if visibility is True:
                    pp = area_light_sampler - shadeInfo.point
                    light_dir = Vector(pp.x, pp.y, pp.z)
                    light_dir.normalize()
                    pdf = area_light.getPDF()
                    cos_theta = Vector.dot(light_dir, shadeInfo.normal)
                    cos_phi = Vector.dot(
                        light_dir * (-1),
                        area_light.getShape().genNormal(shadeInfo)
                        )
                    geoterm = cos_theta * cos_phi / pp.lengthSqure()
                    if cos_theta > 0.0 and cos_phi > 0.0:
                        emission_material = area_light.getShape().getMaterial().getEmission()
                        emission_light_color = emission_material.getCe()
                        emission_light_color = emission_light_color * emission_material.getKe()
                        
                        # Diffuse
                        result_area = result_area + emission_light_color * diffuse_brdf * (geoterm / pdf)
                        
                        # Glossy
                        if shadeInfo.material.getGlossy() is not None:
                            glossy_brdf = shadeInfo.material.getGlossy().getBRDF(
                                shadeInfo.point, shadeInfo.normal, light_dir, to_eye
                                )
                            result_area = result_area + emission_light_color * glossy_brdf * (geoterm / pdf)
            result_area = result_area * (1.0 / len(area_light_samplers))
            result_areas = result_areas + result_area

        return result_areas

    def __ambient_shade(self, shadeInfo):
        ambient_mat = shadeInfo.material.getAmbient()
        brdf = ambient_mat.getBRDF(None, None, None, None)
        ambient_light = shadeInfo.scene.getAmbientLight()
        return ambient_light.getLightColor() * brdf

    def __check_in_parallel_light_shadow(self, shadeInfo):
        parallel_light = shadeInfo.scene.getParallelLight()
        if parallel_light is None:
            return False
        parallel_light_dir = parallel_light.d * (-1)
        shadow_ray = Ray(shadeInfo.point, parallel_light_dir)
        return shadeInfo.scene.isIntersection(shadow_ray, shadeInfo.ep)

    def __ambient_occluder(self, shadeInfo):
        if self.enable_ao is False:
            return 1.0
        
        # Calculate orthonormal basie
        w = shadeInfo.normal
        u = Vector.cross(Vector(0.0072, 1.0, 0.0034), w)  # slightly jitter up vector
        u.normalize()
        v = Vector.cross(w, u)

        # Genrate samplers
        self.ao_sampler.genSamplersInUnitSqure(self.ao_sampler_num)
        self.ao_sampler.mapToHemiSphere(1.0)
        samplers = self.ao_sampler.getSamplers()

        # Calculate samplers on hemisphere
        hemi_sphere_samplers=[]
        for i in range(self.ao_sampler_num):
            cos_phi = math.cos(samplers[i].x)
            sin_phi = math.sin(samplers[i].x)
            cos_theta = math.cos(samplers[i].y)
            sin_theta = math.sin(samplers[i].y)
            pu = sin_theta * cos_phi
            pv = sin_theta * sin_phi
            pw = cos_theta
            point = shadeInfo.point + u * pu + v * pv + w * pw
            hemi_sphere_samplers.append(point)

        # Calculate ambient ratio
        ratio = 0.1
        ratio_step = 1.0 / self.ao_sampler_num
        for sampler in hemi_sphere_samplers:
            d = sampler - shadeInfo.point
            d.normalize()
            ray = Ray(shadeInfo.point, d)
            if shadeInfo.scene.isIntersection(ray, shadeInfo.ep) is False:
                ratio = ratio + ratio_step

        if ratio > 1.0:
            ratio = 1.0
        return ratio
            
        
if __name__ == "__main__":
    sampler = JitteredSampler(1.0)
    m = Matte(sampler)
    mat = Material.create(0.1, 0.4, Color(0.5, 0.5, 0.5), 0.3, Color(0.5, 0.5, 0.5), 20)
    sce = Scene()
    s = ShadeInfo()
    s.setMaterial(mat)
    s.setScene(sce)
    s.setNormal(Vector(0.0, 1.0, 0.0))
    m.shade(s)
