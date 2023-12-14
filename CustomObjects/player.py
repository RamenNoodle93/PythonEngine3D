import numpy as np

from Tools.Objects.object import Object


class Player(Object):
    
    def __init__(self, position = np.array([0, 0, 0], float), rotation = np.array([0, 0, 0], float), scale = 1, color = (0, 200, 0)):
        
        super().__init__(position, rotation, scale, color)

        self.velocity = [0, 0]

        self.moving = False

        self.AddNodes(np.array([
        [0, 0.5, 0],
        [-0.3, -0.5, 0],
        [0.3, -0.5, 0]
        ]))
        
        self.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 0]
        ]))
        
        self.flame = Object(self.position, self.rotation, self.scale, self.color)
        
        self.flame.AddNodes(np.array([
        [-0.125, -0.55, 0],
        [0.125, -0.55, 0],
        [0, -0.85, 0]   
        ]))
        
        self.flame.AddEdges(np.array([
        [0, 1],
        [1, 2],
        [2, 0]
        ]))

        self.flame.CreateHitbox()

        self.CreateHitbox()