import numpy as np
import time
import math
import pygame as pg
import copy
import random as rand

from Tools.Objects.object import Object
from Tools.utils import *

class Player(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)

        self.AddNodes(np.array([
        [-0.3, 0, -0.3],
        [-0.3, 0, 0.3],
        [-0.3, 0.5, -0.3],
        [-0.3, 0.5, 0.3],
        [0.3, 0, -0.3],
        [0.3, 0, 0.3],
        [0.3, 0.5, -0.3],
        [0.3, 0.5, 0.3]
        ]))
        
        for n in range(0, 4): self.AddEdges([n, n + 4])
        for n in range(0, 8, 2): self.AddEdges([n, n + 1])
        for n in (0, 1, 4, 5): self.AddEdges([n, n + 2])
                        
        self.speed = 0.05

        self.moveColliders = []
        
        frontCollider = Object(position = self.position ,rotation = self.rotation, scale = self.scale, color = self.color)
        frontCollider.AddNodes(np.array([
        [-0.3, 0, 0.0],
        [-0.3, 0, 0.3],
        [-0.3, 0.5, 0.0],
        [-0.3, 0.5, 0.3],
        [0.3, 0, 0.0],
        [0.3, 0, 0.3],
        [0.3, 0.5, 0.0],
        [0.3, 0.5, 0.3]
        ]))
        frontCollider.CreateHitbox()
        self.moveColliders.append(frontCollider)

        backCollider = Object(position = self.position ,rotation = self.rotation, scale = self.scale, color = self.color)
        backCollider.AddNodes(np.array([
        [-0.3, 0, -0.3],
        [-0.3, 0, 0.0],
        [-0.3, 0.5, -0.3],
        [-0.3, 0.5, 0.0],
        [0.3, 0, -0.3],
        [0.3, 0, 0.0],
        [0.3, 0.5, -0.3],
        [0.3, 0.5, 0.0]
        ]))
        backCollider.CreateHitbox()
        self.moveColliders.append(backCollider)

        self.lastShot = 0
        self.lastCollision = 0

        self.canMove = [True, True] #back, front

        self.lives = 3
        self.alive = True

        self.CreateHitbox()
        
    def Shoot(self):
        if time.time() - 1 > self.lastShot and self.alive:
            self.lastShot = time.time()
            return True
        
    def Move(self, pressed, camera):
        if self.canMove[1] and pressed[pg.K_w]:
            camera.position[2] += math.cos(degToRad(camera.rotation[1])) * self.speed
            camera.position[0] += -math.sin(degToRad(camera.rotation[1])) * self.speed
        if self.canMove[0] and pressed[pg.K_s]:
            camera.position[2] -= math.cos(degToRad(camera.rotation[1])) * self.speed
            camera.position[0] -= -math.sin(degToRad(camera.rotation[1])) * self.speed
        
        if pressed[pg.K_q]:
            camera.rotation[1] -= 1
        if pressed[pg.K_e]:
            camera.rotation[1] += 1
        
        self.position[0] = -camera.position[0]
        self.position[2] = -camera.position[2]
        self.rotation[1] = -camera.rotation[1]
        
    def Respawn(self):
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.velocity = [0, 0]

        self.flame.position = self.position
        self.flame.rotation = self.rotation

        self.alive = True
        self.collision = False

    def Collision(self):
        self.lives -= 1
        self.RenderParticles()
        self.color = (0, 0, 0)
        self.flame.color = self.color
        self.collision = False
        self.alive = False
        self.lastCollision = time.time()

        