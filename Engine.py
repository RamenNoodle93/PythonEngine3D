import pygame as pg
import numpy as np
import math

from Tools.Objects.camera import *
from Tools.utils import *
from settings import *
from game import *

class Engine:
    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.camera = Camera()
        self.game = Game()
        self.objects = []
        self.running = True
        self.Run()

    def Run(self):

        while self.running:
            if not self.game.HandleEvents(self.camera):
                self.running = False            
            
            projectionMatrix = rotationMatrixAll(self.camera)

            pg.display.set_caption(f'{self.clock.get_fps()}')

            self.game.Update(projectionMatrix, self.camera)
            self.game.Render(self.screen)

            pg.display.flip()
            self.clock.tick(60)
            
        pg.quit()
        
if __name__ == "__main__":
    app = Engine()