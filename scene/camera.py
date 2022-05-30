import numpy as np
import math
from graphics.ray import Ray
from helpers import *


class Camera:
    def __init__(self, pos, width, height, fov=45):
        self.pos = pos
        self.width = width
        self.height = height
        self.fov = np.radians(fov)
        self.eye = np.array([-4., 0., 0.])
        r = float(self.width) / self.height
        S = (-1., -1. / r + .25, 1., 1. / r + .25)
        self.ydata = np.linspace(S[0], S[2], self.width)
        self.zdata = np.linspace(S[1], S[3], self.height)
        self.dir = np.array([0, 0, 0])# np.zeros(3)
        self.scene = None
        self.max_depth = 4

    def set_pos(self, pos):
        self.pos = pos

    def getRay(self, x, y):
        direction = np.zeros(3)
        direction[1], direction[2] = self.ydata[x], self.zdata[y]
        d = direction - self.eye
        d = rotate_x(d, self.dir[0])
        d = rotate_y(d, self.dir[1])
        d = rotate_z(d, self.dir[2])
        return Ray(self.eye + self.pos, normalize(d))

    def set_width(self, w):
        self.width = w

    def set_height(self, h):
        self.height = h

    def set_scene(self, scene):
        self.scene = scene

    def trace(self, ray):
        color = .05
        obj, t = self.scene.intersect(ray)
        if obj is None:
            return

        p = ray.start + ray.direction * t
        n = obj.normal(p)

        for light in self.scene.lights:
            lightray = light.to(p)
            robj, _ = self.scene.intersect(lightray)

            if robj != obj:
                continue

            lightray.direction = normalize(lightray.direction)
            color += obj.diffuse * max(np.dot(n, -lightray.direction), 0) * obj.getColor(p)
            toO = normalize(np.array([-4, 0., -.1]) - p)
            color += obj.specular * max(np.dot(n, normalize(toO - lightray.direction)), 0) ** 1000 * np.array([1.,1.,1.])# light.color
            color *= light.brightness(p)

        return obj, p, n, color

    def getPixel(self, x, y):
        color = np.zeros(3)
        ray = self.getRay(x, y)
        depth = 1
        reflection = 1.
        while depth < self.max_depth:
            trace = self.trace(ray)
            if not trace:
                break

            obj, p, n, col_ray = trace
            ray.start, ray.direction = p + n * .0001, normalize(ray.direction - 2 * np.dot(ray.direction, n) * n)
            depth += 1
            color += col_ray * reflection
            reflection *= obj.ref
        # print(x, y)
        return color * 255
