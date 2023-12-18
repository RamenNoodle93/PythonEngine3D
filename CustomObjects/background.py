import numpy as np
import time
import math
import pygame as pg
import copy
import random as rand

from Tools.Objects.object import Object

class Background(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)
        
        for j in range(4):
            nodes = [] 
                
            horizontalList = [-1.0, -0.8, -0.7, -0.6, -0.45, -0.35, -0.2, 0.0, 0.25, 0.5, 0.75, 0.85, 0.9, 1.0]
            verticalList = [0.15, 0.0, 0.0, 0.08, 0.0, 0.1, 0.0, 0.2, 0.25, 0.0, 0.11, 0.0, 0.26, 0.15]
            if j == 0:
                for i in range(len(horizontalList)):
                    nodes.append([horizontalList[i] * 2, verticalList[i], 2])
            elif j == 1:
                for i in range(len(horizontalList)):
                    nodes.append([-horizontalList[i] * 2, verticalList[i], -2])
            elif j == 2:
                for i in range(len(horizontalList)):
                    nodes.append([-2, verticalList[i], horizontalList[i] * 2])
            elif j == 3:
                for i in range(len(horizontalList)):
                    nodes.append([2, verticalList[i], -horizontalList[i] * 2])
                    
            print(len(self.edges))
            edgeCount = 14 * j

            for i in [0, 2, 3, 5, 6, 7, 8, 10, 12]:
                self.AddEdges([edgeCount + i, edgeCount + i + 1])
        
            for i in [0, 3, 8, 10]:
                self.AddEdges([edgeCount + i, edgeCount + i + 2])

            self.AddNodes(nodes)
            
        self.CreateHitbox()
        
    def Reposition(self, camera):
        self.position[0] = -camera.position[0]
        self.position[2] = -camera.position[2]