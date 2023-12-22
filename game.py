import pygame as pg
import math
import copy
import numpy as np
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
from CustomObjects.barrier import Barrier
from Tools.utils import *

class Game:
    
    def __init__(self, display):
        self.objectList = []
        self.display = display
        
        bgColor = (0.2, 0.7, 0.4)
        self.defColor = (0.2, 0.8, 0.3)
        self.enemyColor = (0.2, 0.9, 0.25)
        self.enemyColor = (0.2, 0.9, 0.25)

        self.objectList.append(Player())
        self.objectList.append(Surface(scale = 10, color = bgColor))
        self.objectList.append(Background(scale = 25, position = [0, -0.5, 0], color = bgColor))
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        
        self.colliders = []
        self.renderStack = []

        self.maxDist = 225
   
        self.player = self.objectList[0]
        self.surface = self.objectList[1]
        self.background = self.objectList[2]
        self.tanks = self.objectList[3]
        self.bullets = self.objectList[4]
        self.enemyBullets = self.objectList[5]
        self.barriers = self.objectList[6]

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
        elif name == 'Barrier':
            self.barriers.append(obj)
        elif name == 'Bullet':
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
            
        for index, obj in enumerate(self.tanks):
            distance = math.pow(obj.position[0] - self.player.position[0], 2) + math.pow(obj.position[2] - self.player.position[2], 2)
            if distance > self.maxDist:
                self.tanks.pop(index)
                break
            self.colliders.append(obj)

        for index, obj in enumerate(self.barriers):
            distance = math.pow(obj.position[0] - self.player.position[0], 2) + math.pow(obj.position[2] - self.player.position[2], 2)
            if distance > self.maxDist:
                self.barriers.pop(index)
                break
            self.colliders.append(obj)

        self.player.canMove = [True, True]

        for index, obj in enumerate(self.colliders):
            
            if obj.CheckCollision(self.player.moveColliders[0]):
                self.player.canMove[0] = False

            if obj.CheckCollision(self.player.moveColliders[1]):
                self.player.canMove[1] = False
                
        if len(self.barriers) < 20:
            newBarrier = Barrier(color = self.defColor)
            newBarrier.position = makeRandPos(self.player.position, useBounds = False, axisX = True, axisY = False, axisZ = True, maxDist = math.sqrt(self.maxDist) - 5)
            self.barriers.append(newBarrier)

        if len(self.tanks) < 1:
            newTank = Tank(color = self.enemyColor)
            newTank.position = makeRandPos(self.player.position, useBounds = False, axisX = True, axisY = False, axisZ = True)
            self.tanks.append(newTank)
            
        self.player.aim.nodes = np.array([
        [-0.03, 0.15, -0.3],
        [-0.05, 0.15, -0.3],
        [-0.05, 0.25, -0.3],
        [-0.03, 0.25, -0.3],
        [0.03, 0.15, -0.3],
        [0.05, 0.15, -0.3],
        [0.05, 0.25, -0.3],
        [0.03, 0.25, -0.3]
        ])

        for tank in self.tanks:
            for ray in self.player.raycast:
                if ray.CheckCollision(tank):
                    self.player.aim.nodes = np.array([
                    [-0.00, 0.18, -0.3],
                    [-0.02, 0.18, -0.3],
                    [-0.02, 0.22, -0.3],
                    [-0.00, 0.22, -0.3],
                    [0.00, 0.18, -0.3],
                    [0.02, 0.18, -0.3],
                    [0.02, 0.22, -0.3],
                    [0.00, 0.22, -0.3]
                    ])
            if tank.EnemyAI(self.player):
                self.AddObject(Bullet(rotation = [0, copy.deepcopy(tank.rotation[1]) + 180, 0], position = [copy.deepcopy(tank.position)[0], 0.3, copy.deepcopy(tank.position)[2]], speed = 0.25), enemy = True)

        for index1, bullet in enumerate(self.enemyBullets):
            if bullet.Lifetime():
                self.enemyBullets.pop(index1)
                break
            bullet.Move()
            for obj in self.barriers:
                if bullet.CheckCollision(obj):
                    self.enemyBullets.pop(index1)
                    break
            if bullet.CheckCollision(self.player):
                print("dead!")

        for index1, bullet in enumerate(self.bullets):
            if bullet.Lifetime():
                self.bullets.pop(index1)
                break
            bullet.Move()
            for obj in self.barriers:
                if bullet.CheckCollision(obj):
                    self.bullets.pop(index1)
                    break
            for index2, tank in enumerate(self.tanks):
                if bullet.CheckCollision(tank):
                    self.bullets.pop(index1)
                    self.tanks.pop(index2)
            
        for obj in itertools.chain(self.tanks, self.bullets, self.enemyBullets, self.barriers):
            self.renderStack.append(obj)
            
        self.renderStack.append(self.player.aim)

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