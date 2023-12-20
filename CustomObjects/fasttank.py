import numpy as np

from CustomObjects.enemy import Enemy

class FastTank(Enemy):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0), cooldown = 3.5, speed = 1.5):
        
        super().__init__(position, rotation, scale, color, cooldown, speed, True, True)
        
        self.AddNodes(np.array([
        [-0.3, 0.0, 0.45],
        [0.3, 0.0, 0.45],   
        [0.25, 0.2, -0.15],
        [0.3, 0.0, -0.45],
        [-0.3, 0.0, -0.45],
        [-0.25, 0.2, -0.15]
        ]))
        
        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [1, 3],
        [2, 3],
        [3, 4],
        [4, 5],
        [4, 0],
        [5, 0],
        [2, 5] 
        ]))
        
        self.CreateHitbox()