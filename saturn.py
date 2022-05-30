from graphics import *
from scene import *
import random

renderer = Renderer()
scene = Scene()

#scene.add(Sphere(0, 0, 0, .2))

#scene.lights.append(PointLight(np.array([0.5, 0, 5]), 200))
scene.lights.append(SpotLight(np.array([1, 1.5, 0]), np.array([0, 1, 0]),1, 2))
scene.lights.append(PointLight(np.array([.2, 0, -2]), 8, color=np.array([0,255,0])))
for i in range(0, 3):
    scene.add(Sphere(np.sin(i*2*np.pi/5) + 0.5, np.cos(i*2*np.pi/5), 0.7, .3, color=np.array([1., 0., 0.])))
scene.add(Sphere(1, 0, .9, .1, color=np.array([1, 1, 0])))
scene.add(Plane(np.array([-1, 0, 0]), np.array([2.5, 0, 0]), color=np.array([0,0,1])))
#scene.lights.append(SpotLight(np.array([-1, 0, 0.9]), np.array([-1, 0, .9]) - np.array([1, 0, .9]), .8, 1))
#scene.lights.append(Sun(np.array([0, 0.5, -50]), 5))
scene.add(Plane(np.array([0, 0, -1.]), np.array([0., 0., 1]), color=np.array([1.,1.,1.])))
renderer.scene = scene

renderer.render()
