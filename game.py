import pygame as pg
import math
import copy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import itertools

from CustomObjects.player import Player
from CustomObjects.surface import Surface
from CustomObjects.tank import Tank
from CustomObjects.fasttank import FastTank
from CustomObjects.background import Background
from CustomObjects.bullet import Bullet
from Tools.utils import makeRandPos

class Game:
    
    def __init__(self, display):
        self.objectList = []
        self.display = display
        
        bgColor = (0.2, 0.7, 0.4)
        self.defColor = (0.2, 0.8, 0.2)

        self.objectList.append(Player())
        self.objectList.append(Surface(scale = 10, color = bgColor))
        self.objectList.append(Background(scale = 25, position = [0, -0.5, 0], color = bgColor))
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        
        self.colliders = []
        self.renderStack = []

        self.player = self.objectList[0]
        self.surface = self.objectList[1]
        self.background = self.objectList[2]
        self.tanks = self.objectList[3]
        self.bullets = self.objectList[4]
        self.enemyBullets = self.objectList[5]
        self.barriers = self.objectList[6]

        self.tanks.append(FastTank(position = [2, 0, 0]))

        # for i in range(50):
        #     newObject = Object()

    def GetStartVal(self):
        #Pozycja startowa kamery
        position = [0, -0.2, 0]
        #Kat podany w stopniach, nie w radianach
        rotation = [0, 135, 0]
        return [position, rotation]

    def HandleEvents(self, camera):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.player.Shoot():
                    self.AddObject(Bullet(rotation = [0, copy.deepcopy(self.player.rotation[1]), 0], position = [copy.deepcopy(self.player.position)[0], 0.3, copy.deepcopy(self.player.position)[2]]))
        return True

    def AddObject(self, obj, enemy = False):
        name = type(obj).__name__
        if name == 'Tank':
            self.tanks.append(obj)
        elif name =='Bullet':
            if enemy:
                self.enemyBullets.append(obj)
            else:
                self.bullets.append(obj)

    def Update(self, camera):
        self.colliders = []
        self.renderStack = []
        
        pressed = pg.key.get_pressed()
        
        self.player.Move(pressed, camera)
        self.surface.Reposition(camera)
        self.background.Reposition(camera)
        self.renderStack.append(self.surface)
        self.renderStack.append(self.background)
        
        for obj in itertools.chain(self.tanks, self.bullets, self.enemyBullets):
            self.renderStack.append(obj)
        for obj in itertools.chain(self.tanks):
            self.colliders.append(obj)
            
        for obj in self.colliders:
            if obj.CheckCollision(self.player.moveColliders[0]):
                self.player.canMove[0] = False
            else:
                self.player.canMove[0] = True
                
            if obj.CheckCollision(self.player.moveColliders[1]):
                self.player.canMove[1] = False
            else:
                self.player.canMove[1] = True
                
        if len(self.tanks) < 1:
            newTank = Tank(color = self.defColor)
            newTank.position = makeRandPos(self.player.position, useBounds = False, axisX = True, axisY = False, axisZ = True)
            self.tanks.append(newTank)
            
        for tank in self.tanks:
            if tank.EnemyAI(self.player):
                self.AddObject(Bullet(rotation = [0, copy.deepcopy(tank.rotation[1]) + 180, 0], position = [copy.deepcopy(tank.position)[0], 0.3, copy.deepcopy(tank.position)[2]], speed = 0.25), enemy = True)

        for index1, bullet in enumerate(self.enemyBullets):
            if bullet.Lifetime():
                self.enemyBullets.pop(index1)
                break
            bullet.Move()
            if bullet.CheckCollision(self.player):
                print("dead!")

        for index1, bullet in enumerate(self.bullets):
            if bullet.Lifetime():
                self.bullets.pop(index1)
                break
            bullet.Move()
            for index2, tank in enumerate(self.tanks):
                if bullet.CheckCollision(tank):
                    self.bullets.pop(index1)
                    self.tanks.pop(index2)
            
    def Render(self, camera, showNodes = False, showEdges = True, showHitbox = False):
        glPushMatrix()
        
        glRotatef(camera.rotation[0], 1, 0, 0)
        glRotatef(camera.rotation[1], 0, 1, 0)
        glRotatef(camera.rotation[2], 0, 0, 1)

        glTranslatef(camera.position[0], camera.position[1], camera.position[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                
        for obj in self.renderStack:
            obj.Draw(showNodes, showEdges, showHitbox)

        glPopMatrix()