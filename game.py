import pygame as pg
import math
import numpy as np
import copy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from CustomObjects.player import Player
from CustomObjects.asteroid import Asteroid
from CustomObjects.bullet import Bullet
from Tools.utils import *

class Game:
    
    def __init__(self, display):
        self.defaultColor = (1, 1, 1)

        self.display = display

        self.objectList = []
        self.objectList.append(Player(color = self.defaultColor))
        
        self.objectList.append([])
        self.objectList.append([])
        
        for i in range(5):
            self.AddObject(Asteroid(position = [0, i, 0]))
            
        self.player = self.objectList[0]
        self.count = 0
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
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and len(self.objectList[2]) < 5:
                if self.player.Shoot():
                    self.AddObject(Bullet(copy.deepcopy(self.player.position), copy.deepcopy(self.player.rotation)))
        return True

    def AddObject(self, obj):
        name = type(obj).__name__
        print(name)
        if name == 'Asteroid':
            self.objectList[1].append(obj)
        elif name =='Bullet':
            self.objectList[2].append(obj)
            
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

        if pressed[pg.K_t]:
            self.player.position[2] += 0.1

        if pressed[pg.K_g]:
            self.player.position[2] -= 0.1


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

        self.Wrap(self.player)

        for obj in self.objectList[1]:
            obj.Move()
            self.Wrap(obj)
                
        for index1, obj in enumerate(self.objectList[2]):
            if obj.Lifetime():
                self.objectList[2].pop(index1)
                break
            obj.Move()
            self.Wrap(obj)
            for index2, asteroid in enumerate(self.objectList[1]):
                if asteroid.CheckCollision(obj):
                    self.objectList[2].pop(index1)
                    
                    position = copy.deepcopy(asteroid.position)
                    countAst = copy.deepcopy(asteroid.count)
                    scaleAst = copy.deepcopy(asteroid.scale)
                    
                    self.objectList[1].pop(index2)
                    
                    if countAst != 0:
                        for i in range(2):
                            self.AddObject(Asteroid(copy.deepcopy(position), scale = scaleAst * 0.8, count = countAst - 1))
                    break

                    

        for obj in self.objectList[1]:
            if self.player.CheckCollision(obj):
                print("Przegrales!")
            else:
                pass
                #print("no collision")
        
    def Wrap(self, obj):
        if obj.position[0] > self.boundary:
            obj.position[0] = -self.boundary
        elif obj.position[0] < -self.boundary:
            obj.position[0] = self.boundary
        if obj.position[1] > self.boundary:
            obj.position[1] = -self.boundary
        elif obj.position[1] < -self.boundary:
            obj.position[1] = self.boundary

    def Render(self, camera, showNodes = False, showEdges = True, showHitbox = False):
        glPushMatrix()

        glRotatef(camera.rotation[0], 1, 0, 0)
        glRotatef(camera.rotation[1], 0, 1, 0)
        glRotatef(camera.rotation[2], 0, 0, 1)

        glTranslatef(camera.position[0], camera.position[1], camera.position[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        

        self.player.Draw(showNodes, showEdges, showHitbox)
        if showHitbox:
            self.player.ProjectCollision()
            
        for obj in self.objectList[1]:
            obj.Draw(showNodes, showEdges, showHitbox)
            if showHitbox:
                obj.ProjectCollision()
            
        for obj in self.objectList[2]:
            obj.Draw(True, False, showHitbox)

        if self.player.moving:
            self.player.flame.Draw(showNodes, showEdges, showHitbox)  

        glPopMatrix()