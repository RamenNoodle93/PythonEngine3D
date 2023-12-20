import numpy as np
import math
import time

from Tools.Objects.object import Object
from Tools.utils import *

class Enemy(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0), cooldown = 3, speed = 1, shootMove = False, shootRot = False):
        
        super().__init__(position, rotation, scale, color)
        self.lastReady = 0
        self.cooldown = cooldown
        self.speed = speed
        self.shootRot = shootRot
        self.shootMove = shootMove

    def EnemyAI(self, player):
        angle = math.atan2((self.position[2] - player.position[2]), (self.position[0] - player.position[0])) + degToRad(self.rotation[1]) - math.pi / 2
        
        ready = True

        if angle < -math.pi or angle > math.pi:
            angle %= 2 * math.pi

        print(angle)

        if not (angle < -math.pi + 0.1 or angle > math.pi - 0.1) or (angle > math.pi or angle < -math.pi):
            if angle > 2 * math.pi - 0.1 or (angle > 0 and angle < math.pi / 2 + math.pi / 18):
                self.rotation[1] += 1
            elif angle > math.pi / 2 + math.pi / 20:
                self.rotation[1] += 1
            elif angle < math.pi / 2 - math.pi / 20:
                self.rotation[1] -= 1
            if not self.shootRot:
                #self.lastReady = time.time()
                ready = False
        
        if ready and math.pow(self.position[0] - player.position[0], 2) + math.pow(self.position[2] - player.position[2], 2) > 36:
            moveVector = [math.sin(degToRad(self.rotation[1])) * 0.025 * self.speed, math.cos(degToRad(self.rotation[1])) * 0.025 * self.speed]
            self.Move(moveVector)
            if not self.shootMove:
                #self.lastReady = time.time()
                ready = False
            
        if ready:
            if time.time() - self.cooldown > self.lastReady:
                self.lastReady = time.time()
                return True
            
        return False
            
    def Move(self, moveVector):
        self.position[0] += moveVector[0]
        self.position[2] += moveVector[1]
        