import pygame as pg
import numpy as np
import math

from CustomObjects.surface import Surface
from CustomObjects.tank import Tank

class Game:
    
    def __init__(self):
        self.objectList = []
        self.objectList.append(Surface(size = 1.25))
        self.speed = 0.05

    def HandleEvents(self, camera):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True

    def AddObject(self, obj):
        self.objectList.append(obj)

    def Update(self, rotationMatrix, camera):
        
        pressed = pg.key.get_pressed()
        
        if pressed[pg.K_w]:
            camera.position[2] += math.cos(camera.rotation[1]) * self.speed
            camera.position[0] += -math.sin(camera.rotation[1]) * self.speed

        if pressed[pg.K_q]:
            camera.rotation[1] += 0.01
        if pressed[pg.K_e]:
            camera.rotation[1] -= 0.01

        if len(self.objectList) < 1:
            self.AddObject(Tank())

        for obj in self.objectList:
            obj.CalculateProjection(rotationMatrix, camera)
            
        
        
    def Render(self, surface, bgColor = "black", showNodes = False, showEdges = True):
        surface.fill(bgColor)
        for obj in self.objectList:
            obj.Draw(surface, showNodes, showEdges)
    
