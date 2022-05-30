from graphics.ray import *
from scene.camera import *

from abc import ABC, abstractmethod
import numpy as np


class Scene:
    def __init__(self):
        self.objects = list()
        self.lights = list()
        self.camera = Camera(np.array([-1, 0, -.1]), 500, 500)
        self.camera.set_scene(self)

    def add(self, *args):
        for ob in args:
            self.objects.append(ob)

    def intersect(self, ray):
        t = np.inf
        obj = None
        for ob in self.objects:
            d = ob.intersects(ray)
            if d < t and d != 0:
                t = d
                obj = ob

        return obj, t


class Object(ABC):
    def __init__(self):
        self.diffuse = 1.
        self.specular = 1.

    @abstractmethod
    def intersects(self, ray):
        pass

    @abstractmethod
    def normal(self, p):
        pass

    @abstractmethod
    def getColor(self, p):
        pass


class Light(ABC):
    def __init__(self, pos, brightness):
        self.pos = pos
        self.brightness0 = brightness
        self.color = np.array([0., 100., 0.])#(np.ones(3))

    def to(self, p):
        return Ray(self.pos, p - self.pos)

    @abstractmethod
    def brightness(self, p):
        pass


class Sun(Light):
    def __init__(self, pos, brightness):
        super().__init__(pos, brightness)

    def brightness(self, p):
        return self.brightness0


class PointLight(Light):
    def __init__(self, pos, brightness, color):
        super().__init__(pos, brightness)
        self.color = color

    def brightness(self, p):
        return self.brightness0 / pow(np.linalg.norm(self.pos - p), 2)


class SpotLight(Light):
    def __init__(self, pos, direction, angle, brightness):
        super().__init__(pos, brightness)
        self.direction = direction
        self.angle = angle

    def brightness(self, p):
        d = self.pos - p
        alpha = np.arccos((np.dot(d, self.direction))/(np.linalg.norm(self.direction)*np.linalg.norm(d)))
        if alpha <= self.angle:
            return self.brightness0 / pow(np.linalg.norm(self.pos - p), 2)
        else:
            return 0


class Plane(Object):
    def __init__(self, n, p, color, *args):
        super().__init__()
        self.n = n
        self.p = p
        self.color = color
        self.diffuse = 1
        self.specular = .75
        self.ref = .15

    def intersects(self, ray):
        N = self.n
        D = ray.direction
        O = ray.start
        P = self.p
        denom = np.dot(D, N)
        if np.abs(denom) < 1e-6:
            return np.inf
        d = np.dot(P - O, N) / denom
        if d < 0:
            return np.inf
        return d

    def normal(self, p):
        return self.n

    def getColor(self, p):
        return self.color


class Sphere(Object):
    def __init__(self, x, y, z, r, color, *args):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.specular = 1
        self.diffuse = .5
        self.color = color
        self.ref = .5

    def intersects(self, ray):
        S = np.array([self.x,self.y,self.z])
        R = self.r
        O = ray.start
        D = ray.direction
        a = np.dot(D, D)
        OS = O - S
        b = 2 * np.dot(D, OS)
        c = np.dot(OS, OS) - R * R
        disc = b * b - 4 * a * c
        if disc > 0:
            distSqrt = np.sqrt(disc)
            q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
            t0 = q / a
            t1 = c / q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
        return np.inf

    def normal(self, p):
        return normalize(p - np.array([self.x, self.y, self.z]))

    def getColor(self, p):
        return self.color
