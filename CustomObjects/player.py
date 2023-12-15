import numpy as np
import time
import math
import pygame as pg
import copy
import random as rand

from Tools.Objects.object import Object

class Player(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)

        self.velocity = [0, 0]
        self.speed = 0.0025
        self.moving = False

        self.AddNodes(np.array([
        [0, 0.5, 0],
        [-0.3, -0.5, 0],
        [0.3, -0.5, 0]
        ]))
        
        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 0]
        ]))
        
        self.flame = Object(self.position, self.rotation, self.scale, self.color)
        
        self.flame.AddNodes(np.array([
        [-0.125, -0.55, 0],
        [0.125, -0.55, 0],
        [0, -0.85, 0]   
        ]))
        
        self.flame.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 0]
        ]))
        
        self.lastShot = 0
        self.lastCollision = 0
        self.lastColorChange = 0
        self.lives = 3
        self.alive = True
        self.flame.CreateHitbox()
        self.CreateHitbox()
        
    def Shoot(self, speed = 0.01):
        if time.time() - 0.25 > self.lastShot and self.alive:
            self.lastShot = time.time()
            return True
        
    def Move(self, pressed):
        if pressed[pg.K_w]:
            self.moving = True
            if abs(self.velocity[1]) <= 0.1:
                self.velocity[1] += math.cos(self.rotation[2] * math.pi / 180) * self.speed
            if abs(self.velocity[0]) <= 0.1:
                self.velocity[0] += -math.sin(self.rotation[2] * math.pi / 180) * self.speed
        else:
            self.moving = False

        if pressed[pg.K_q]:
            self.rotation[2] += 3
        if pressed[pg.K_e]:
            self.rotation[2] -= 3
            
        if self.velocity[0] > 0:
            self.velocity[0] -= 0.0005
        elif self.velocity[0] < 0:
            self.velocity[0] += 0.0005
        if self.velocity[1] > 0:
            self.velocity[1] -= 0.0005
        elif self.velocity[1] < 0:
            self.velocity[1] += 0.0005

        self.position[1] += self.velocity[1]
        self.position[0] += self.velocity[0]
        
    def RenderParticles(self):
        objects = []
        for i in range(3):
            line = Object(copy.deepcopy(self.position), copy.deepcopy(self.rotation), 1, copy.deepcopy(self.color))
            line.AddNodes(np.array([
            [0.0, 0.3, 0],
            [0.0, -0.3, 0]
            ]))
            line.AddEdges(np.array([
            [0, 1]
            ]))
            line.CreateHitbox()
            line.rotate = copy.deepcopy(rand.randrange(-3, 3, 1))
            line.movement = copy.deepcopy([rand.choice([rand.randrange(-3, -1, 1) / 240, rand.randrange(1, 3, 1) / 240]), rand.choice([rand.randrange(-3, -1, 1) / 80, rand.randrange(1, 3, 1) / 80])])
            objects.append(line)
        return objects

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

        