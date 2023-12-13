import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from Tools.Objects.camera import *
from settings import *
from game import *

class Engine:
    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        
        gluPerspective(hFov, (width / height), 0.1, 50.0)

        self.clock = pg.time.Clock()
        self.game = Game()
        startData = self.game.GetStartVal()
        self.camera = Camera(position = startData[0], rotation = startData[1])
        self.objects = []
        self.running = True
        self.Run()

    def Run(self):

        while self.running:
            if not self.game.HandleEvents(self.camera):
                self.running = False            
            
            pg.display.set_caption(f'{self.clock.get_fps()}')

            self.game.Update(self.camera)
            
            self.game.Render(self.camera)

            pg.display.flip()
            self.clock.tick(60)
            
        pg.quit()
        
if __name__ == "__main__":
    app = Engine()