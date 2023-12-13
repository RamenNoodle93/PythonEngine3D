import pygame as pg
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from CustomObjects.surface import Surface
from CustomObjects.tank import Tank

class Game:
    
    def __init__(self):
        self.objectList = []
        self.objectList.append(Surface())
        for i in range(4, 11, 2):
            self.objectList.append(Tank(position = [3, 0, i]))
        self.speed = 0.05

    def GetStartVal(self):
        #Pozycja startowa kamery
        position = [0, -0.3, 0]
        #Kat podany w stopniach, nie w radianach
        rotation = [0, 135, 0]
        return [position, rotation]

    def HandleEvents(self, camera):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True

    def AddObject(self, obj):
        self.objectList.append(obj)

    def Update(self, camera):
        
        pressed = pg.key.get_pressed()
        
        if pressed[pg.K_w]:
            camera.position[2] += math.cos(camera.rotation[1] * math.pi / 180) * self.speed
            camera.position[0] += -math.sin(camera.rotation[1] * math.pi / 180) * self.speed
        if pressed[pg.K_s]:
            camera.position[2] -= math.cos(camera.rotation[1] * math.pi / 180) * self.speed
            camera.position[0] -= -math.sin(camera.rotation[1] * math.pi / 180) * self.speed

        if pressed[pg.K_SPACE]:
            camera.position[1] -= 0.05
        if pressed[pg.K_LCTRL]:
            camera.position[1] += 0.05
        
        if pressed[pg.K_q]:
            camera.rotation[1] -= 1
        if pressed[pg.K_e]:
            camera.rotation[1] += 1
        if pressed[pg.K_r]:
            camera.rotation[0] -= 1
        if pressed[pg.K_f]:
            camera.rotation[0] += 1
        
    def Render(self, camera, showNodes = False, showEdges = True, showHitbox = True):
        glPushMatrix()

        glRotatef(camera.rotation[0], 1, 0, 0)
        glRotatef(camera.rotation[1], 0, 1, 0)
        glRotatef(camera.rotation[2], 0, 0, 1)

        glTranslatef(camera.position[0], camera.position[1], camera.position[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.objectList:
            obj.Draw(showNodes, showEdges, showHitbox)
    
        glPopMatrix()