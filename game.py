import pygame as pg
import math
import numpy as np

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from CustomObjects.asteroid import Asteroid

from CustomObjects.player import Player

from CustomObjects.surface import Surface
from CustomObjects.tank import Tank
from CustomObjects.axes import Axis
from CustomObjects.asteroid import Asteroid

class Game:
    
    def __init__(self):
        self.defaultColor = (255, 255, 255)
        self.objectList = []
        self.objectList.append(Player(color = self.defaultColor))
        #self.objectList.append(Axis())
        self.objectList.append(Asteroid(position = [0, 1, 0]))
        self.player = self.objectList[0]
        
        self.speed = 0.0025

    def GetStartVal(self):
        #Pozycja startowa kamery
        position = [0, 0, -15]
        #Kat podany w stopniach, nie w radianach
        rotation = [0, 0, 0]
        
        self.boundary = abs(position[2]) / math.sqrt(3)

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
            self.player.moving = True
            if abs(self.player.velocity[1]) <= 0.1:
                self.player.velocity[1] += math.cos(self.player.rotation[2] * math.pi / 180) * self.speed
            if abs(self.player.velocity[0]) <= 0.1:
                self.player.velocity[0] += -math.sin(self.player.rotation[2] * math.pi / 180) * self.speed
        else:
            self.player.moving = False

        if pressed[pg.K_q]:
            self.player.rotation[2] += 3
        if pressed[pg.K_e]:
            self.player.rotation[2] -= 3
            
        if self.player.velocity[0] > 0:
            self.player.velocity[0] -= 0.0005
        elif self.player.velocity[0] < 0:
            self.player.velocity[0] += 0.0005
        if self.player.velocity[1] > 0:
            self.player.velocity[1] -= 0.0005
        elif self.player.velocity[1] < 0:
            self.player.velocity[1] += 0.0005

        self.player.position[1] += self.player.velocity[1]
        self.player.position[0] += self.player.velocity[0]

        if self.player.position[0] > self.boundary:
            self.player.position[0] = -self.boundary
        elif self.player.position[0] < -self.boundary:
            self.player.position[0] = self.boundary
        if self.player.position[1] > self.boundary:
            self.player.position[1] = -self.boundary
        elif self.player.position[1] < -self.boundary:
            self.player.position[1] = self.boundary

        for obj in self.objectList:
            self.Wrap(obj)
                
        for i in range(1, len(self.objectList)):
            self.player.CheckCollision(self.objectList[i])
        
    def Wrap(self, obj):
        if obj.position[0] > self.boundary:
            obj.position[0] = -self.boundary
        elif obj.position[0] < -self.boundary:
            obj.position[0] = self.boundary
        if obj.position[1] > self.boundary:
            obj.position[1] = -self.boundary
        elif obj.position[1] < -self.boundary:
            obj.position[1] = self.boundary

    def Render(self, camera, showNodes = True, showEdges = True, showHitbox = True):
        glPushMatrix()

        glRotatef(camera.rotation[0], 1, 0, 0)
        glRotatef(camera.rotation[1], 0, 1, 0)
        glRotatef(camera.rotation[2], 0, 0, 1)

        glTranslatef(camera.position[0], camera.position[1], camera.position[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        

        for obj in self.objectList:
            obj.Draw(showNodes, showEdges, showHitbox)
            obj.ProjectCollision()
            
        if self.player.moving:
            self.player.flame.Draw(showNodes, showEdges, showHitbox)
        
        
        glPopMatrix()