from re import S
import numpy as np
import random as rand
from Tools.Objects.object import Object


class Asteroid(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (255, 255, 255), count = 2):
        
        color = [1 - 0.3 * (2 - count), 1 - 0.3 * (2 - count), 1 - 0.3 * (2 - count)]
                
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [-0.8, -0.2, 0],
        [-0.3, -0.7, 0],
        [0.5, -0.25, 0],
        [0.7, -0.2, 0],
        [0.55, 0.25, 0],
        [0, 0.65, 0]
        ]))
        
        for node in self.nodes:
            node[0] += + rand.randrange(-3, 3, 1) / 20
            node[1] += + rand.randrange(-3, 3, 1) / 20

        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 0]
        ]))
        
        self.count = count

        self.rotate = rand.randint(-5, 5) / 10
        
        self.movement = [rand.randrange(-3, 3, 1) / 80, rand.randrange(-3, 3, 1) / 80]
        
        self.CreateHitbox()

    def Move(self):
        self.rotation[2] += self.rotate
        self.position[0] += self.movement[0]
        self.position[1] += self.movement[1]
