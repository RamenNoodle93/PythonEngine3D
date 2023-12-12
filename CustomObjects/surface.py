import pygame as gp
import numpy as np

from settings import *
from Tools.Objects.object import Object

class Surface(Object):
     
     def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 800, color = (0, 200, 0), size = 1):
        
        super().__init__(position, rotation, scale, color, size)

        scale = 5        

        nodes = []
        for y in range(10):
            for x in range(10):
                nodes.append([-1 + 2 * y, 0, -1 + 2 * x])
                nodes.append([1 + 2 * y, 0, -1 + 2 * x])
                nodes.append([1 + 2 * y, 0, 1 + 2 * x])
                nodes.append([-1 + 2 * y, 0, 1 + 2 * x])
            
                self.AddEdges([0 + 4 * x + 40 * y, 1 + 4 * x + 40 * y])
                self.AddEdges([1 + 4 * x + 40 * y, 2 + 4 * x + 40 * y])
                self.AddEdges([2 + 4 * x + 40 * y, 3 + 4 * x + 40 * y])
                self.AddEdges([3 + 4 * x + 40 * y, 0 + 4 * x + 40 * y])
                
        

        self.AddNodes(nodes)



        # nodestoadd = []
        # for x in range(24):
        #     nodestoadd.append([x - 12, 0, 12])
        #     nodestoadd.append([x - 12, 0, -12])
            
        # for x in range(48):
        #     if x%2 == 0:
        #         self.AddEdges([x, x+1])
        #         print(self.edges)
                
        # for z in range(24, 49):
        #     nodestoadd.append([12, 0, z - 36])
        #     nodestoadd.append([-12, 0, z - 36])
                
        # for z in range(48, 98):
        #     if z % 2 == 0:
        #         self.AddEdges([z, z+1])
        
        # for index, node in enumerate(nodestoadd):
        #     print(index, node)
        # self.AddNodes(nodestoadd)
        