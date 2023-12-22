import numpy as np
import copy
import random

from Tools.Objects.object import Object


class Barrier(Object):
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 1, 0)):
        super().__init__(position, rotation, scale, color)
        
        self.AddNodes(np.array([
        [0.5, 0.0, 0.2],
        [-0.5, 0.0, 0.2],
        [-0.5, 0.0, -0.2],
        [0.5, 0.0, -0.2],
        [0.5, 0.3, 0.2],
        [-0.5, 0.3, 0.2],
        [-0.5, 0.3, -0.2],
        [0.5, 0.3, -0.2]
        ]))
        
        offset = copy.deepcopy(random.uniform(0.4, 1.2))
        for node in self.nodes[4:8]:
            node[1] *= offset + copy.deepcopy(random.uniform(-0.3, 0.3))

        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7],
        [4, 5],
        [5, 6],
        [6, 7],
        [7, 4]
        ]))
        
        self.CreateHitbox()