from random import *
from math import pi, sin, cos
from colorsys import hsv_to_rgb as h2r

from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import Point3
from panda3d.core import *

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()

def frange(start, stop, step):
  while start < stop:
    yield float(start)
    start += step

class App(ShowBase):

  def spinCameraTask(self, task):
      t = task.time * 0.1
      angleRadians = t * (pi / 180.0)
      self.camera.setPos(10 * sin(t), 10 * cos(t), 0)
      self.camera.lookAt(0, 0, 0)
      return Task.cont

  def grid(self, scene):
    l = LineSegs()
    for x in range(-10, 10):
      for y in range(-10, 10):
        l.setColor(0.1, 0.1, 0.1, 1.0)
        l.setThickness(1)
        l.moveTo(x, -10, 0)
        l.drawTo(x, 10, 0)
        l.moveTo(-10, x, 0)
        l.drawTo(10, x, 0)
    lp = NodePath(l.create(scene))
    lp.setAntialias(AntialiasAttrib.MMultisample)
    lp.reparentTo(scene)

  def meshGrid(self, meshd, camera, scene):
    lp = meshd.getRoot()
    lp.reparentTo(scene)
    lp.setDepthWrite(False)
    lp.setTransparency(True)
    lp.setTwoSided(True)
    lp.setBin("fixed",0)
    lp.setLightOff(True)
    meshd.setBudget(1000)
    meshd.begin(camera, scene)
    for x in range(-10, 10):
      for y in range(-10, 10):
        meshd.segment(
          (x, -10, 0),
          (x, 10, 0),
          randint(181,207),
          10,
          (1, 1, 1, 1)
        )
    meshd.end()

  def create(self, scene, material):
    for x in range(-5, 5):
      for y in range(-5, 5):
        for z in range(-5, 5):
          rx = 0# random.randint(1, 10) / 10.0
          ry = 0# random.randint(1, 10) / 10.0
          rz = 0# random.randint(1, 10) / 10.0
          p = self.loader.loadModel("sphere.bam")
          p.reparentTo(scene)
          p.setPos(x + rx, y + ry, z + rz)
          p.setMaterial(material)
          p.setScale(0.1)

  def createM(self, h, s, v):
    m = Material()
    m.setShininess(0.9)
    (r, g, b) = h2r(h, s, v)
    m.setAmbient((r, g, b, 1))
    m.setDiffuse((0.3, 0.3, 0.3, 1))
    # m.setEmission((0.3, 0.1, 0.1, 1))
    return m

  def point(self, scene, location, material):
    p = self.loader.loadModel("sphere.bam")
    p.reparentTo(scene)
    p.setPos(location[0], location[1], location[2])
    p.setScale(0.1)
    p.setMaterial(material)
    return p


  def showIris(self, iris, scene):
    m1 = self.createM(0.3, 0.7, 0.5)
    m2 = self.createM(0.1, 0.7, 0.5)
    m3 = self.createM(0.7, 0.7, 0.5)
    m = [m1, m2, m3 ]
    for i in range(0, len(iris.data)):
      item = iris.data[i]
      label = iris.target[i]

      x1 = item[0] * 2.5 - 10
      y1 = item[1] * 2.5 - 10
      z1 = item[2] * 2.5

      x2 = item[0] * 2.5 - 20
      y2 = item[1] * 2.5 - 20
      z2 = item[3] * 2.5

      self.point(scene, (x1, y1, z1), m[label])
      self.point(scene, (x2, y2, z2), m[label])

  def __init__(self):
    ShowBase.__init__(self)


    #self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    base.setBackgroundColor(0, 0, 0)
    base.cam.setPos(0, -40, 10)
    base.cam.lookAt(0, 0, 10)

    scene = self.render
    scene.setAntialias(AntialiasAttrib.MAuto)

    #grid = Shader.load(Shader.SL_GLSL, vertex="grid.vert", fragment="grid.frag")
    #scene.set_shader(grid)

    aLight = AmbientLight('al')
    aLightP = scene.attachNewNode(aLight)
    aLightP.setPos(10, -20, 0)

    dl = DirectionalLight('dl')
    dlp = scene.attachNewNode(dl)
    dlp.lookAt(0, 0, 0)
    dlp.setPos(10, -20, 0)

    scene.setLight(aLightP)
    scene.setLight(dlp)

    self.grid(scene)
    self.showIris(iris, scene)

    taskMgr.add(self.spinCameraTask, "draw task")

app = App()
app.run()
