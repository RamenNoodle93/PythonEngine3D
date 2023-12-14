import numpy as np
import time

from Tools.Objects.object import Object
from CustomObjects.bullet import Bullet

class Player(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)

        self.velocity = [0, 0]

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

        self.flame.CreateHitbox()
        self.CreateHitbox()
        
    def Shoot(self, speed = 0.01):
        if time.time() - 0.25 > self.lastShot:
            self.lastShot = time.time()
            return True