import numpy as np
import math
import time

from Tools.Objects.object import Object
from Tools.utils import *

class Bullet(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (255, 255, 255), speed = 0.1):
        
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [0, 0, 0]
        ]))
        
        self.velocity = [-math.sin(degToRad(self.rotation[2])) * speed, math.cos(degToRad(self.rotation[2])) * speed]
        self.created = time.time()

        self.CreateHitbox()
        
    def Move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
    def Lifetime(self):
        if time.time() - 1.7 > self.created:
            return True
        return False