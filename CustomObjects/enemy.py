import numpy as np
import math

from Tools.Objects.object import Object
from Tools.utils import *

class Enemy(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)
        

    def EnemyAI(self, player):
        angle = math.atan2((self.position[2] - player.position[2]), (self.position[0] - player.position[0])) + degToRad(self.rotation[1]) - math.pi / 2
        
        if angle < -math.pi or angle > math.pi:
            angle %= math.pi

        if not (angle < -math.pi + 0.1 or angle > math.pi - 0.1):
            if angle > math.pi / 2 + math.pi / 20:
                self.rotation[1] += 1
            elif angle < math.pi / 2 - math.pi / 20:
                self.rotation[1] -= 1
        
        if math.pow(self.position[0] - player.position[0], 2) + math.pow(self.position[2] - player.position[2], 2) > 12:
            moveVector = [math.sin(degToRad(self.rotation[1])) * 0.025, math.cos(degToRad(self.rotation[1])) * 0.025]
            self.Move(moveVector)
            
    def Move(self, moveVector):
        self.position[0] += moveVector[0]
        self.position[2] += moveVector[1]