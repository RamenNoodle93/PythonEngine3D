import pygame as gp
import numpy as np

from settings import *
from Tools.Objects.object import Object

class Axis(Object):
     
     def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [-8, -8, 0],
        [8, -8, 0],
        [-8, 8, 0]
        ]))
        
        self.AddEdges(np.array([
        [0, 1],
        [0, 2]
        ]))
        
        self.CreateHitbox()