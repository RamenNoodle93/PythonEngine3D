import numpy as np
import math

class Camera:
    def __init__(self, position = np.array([0, 0, -5], float), rotation = np.array([0, 0, 0], float), fov = 60):
        self.position = position
        self.rotation = rotation