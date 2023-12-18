import numpy as np

class Camera:
    
    def __init__(self, position = np.array([0, 0, -5], dtype = float), rotation = np.array([0, 0, 0], dtype = float)):
        self.position = position
        self.rotation = rotation