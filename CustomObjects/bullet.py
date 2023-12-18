import numpy as np
import math
import time

from Tools.Objects.object import Object
from Tools.utils import *

class Bullet(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (255, 255, 255), speed = 0.5):
        
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [-0.1, -0.1, -0.1],
        [-0.1, -0.1, 0.1],
        [-0.1, 0.1, -0.1],
        [-0.1, 0.1, 0.1],
        [0.1, -0.1, -0.1],
        [0.1, -0.1, 0.1],
        [0.1, 0.1, -0.1],
        [0.1, 0.1, 0.1]
        ]))
        
        for n in range(0, 4): self.AddEdges([n, n + 4])
        for n in range(0, 8, 2): self.AddEdges([n, n + 1])
        for n in (0, 1, 4, 5): self.AddEdges([n, n + 2])
        
        self.velocity = [math.sin(degToRad(self.rotation[1])) * speed, 0, math.cos(degToRad(self.rotation[1])) * speed]
        self.created = time.time()

        self.CreateHitbox()
        
    def Move(self):
        self.position[0] -= self.velocity[0]
        self.position[2] -= self.velocity[2]
        
    def Lifetime(self):
        if time.time() - 1 > self.created:
            return True
        return False