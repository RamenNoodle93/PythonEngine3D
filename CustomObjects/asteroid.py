import numpy as np

from Tools.Objects.object import Object


class Asteroid(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [-0.8, -0.2, 0],
        [-0.3, -0.7, 0],
        [0.5, -0.25, 0],
        [0.7, -0.2, 0],
        [0.55, 0.25, 0],
        [0, 0.65, 0]
        ]))
        
        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 0]
        ]))
        
        self.CreateHitbox()