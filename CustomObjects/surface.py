import pygame as gp
import numpy as np

from settings import *
from Tools.Objects.object import Object

class Surface(Object):
     
     def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)

        scale = 5        

        nodes = []
        for y in range(10):
            for x in range(10):
                nodes.append([-1 + 0.2 * y, 0, -1 + 0.2 * x])
                nodes.append([1 + 0.2 * y, 0, -1 + 0.2 * x])
                nodes.append([1 + 0.2 * y, 0, 1 + 0.2 * x])
                nodes.append([-1 + 0.2 * y, 0, 1 + 0.2 * x])
            
                self.AddEdges([0 + 4 * x + 40 * y, 1 + 4 * x + 40 * y])
                self.AddEdges([1 + 4 * x + 40 * y, 2 + 4 * x + 40 * y])
                self.AddEdges([2 + 4 * x + 40 * y, 3 + 4 * x + 40 * y])
                self.AddEdges([3 + 4 * x + 40 * y, 0 + 4 * x + 40 * y])

        self.AddNodes(nodes)

        self.CreateHitbox()
        
     def Reposition(self, camera):
        posX, posZ = self.position[0], self.position[2]
        
        scale = self.scale * 0.2
        if round(camera.position[0]) % scale == 0:
            posX = -round(camera.position[0]) - self.scale
        if round(camera.position[2]) % scale == 0:
            posZ = -round(camera.position[2]) - self.scale

        self.position = [posX, 0, posZ]

