import numpy as np

from Tools.Objects.object import Object

class Cube(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (255, 0, 255)):
        
        super().__init__(position, rotation, scale, color)

        self.AddNodes(np.array([
        [-1, -1, -1],
        [-1, -1, 1],
        [-1, 1, -1],
        [-1, 1, 1],
        [1, -1, -1],
        [1, -1, 1],
        [1, 1, -1],
        [1, 1, 1]
        ]))
        
        for n in range(0, 4): self.AddEdges([n, n + 4])
        for n in range(0, 8, 2): self.AddEdges([n, n + 1])
        for n in (0, 1, 4, 5): self.AddEdges([n, n + 2])
        
        self.CreateHitbox()