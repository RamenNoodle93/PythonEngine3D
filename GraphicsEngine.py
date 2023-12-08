import pygame as pg
import numpy as np
import math
from Tools.Objects.cube import *
from Tools.Objects.camera import *
from Tools.matrix import *
from Tools.constants import *
from event import *

screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()

running = True

cubes = []

for i in range(5):
    for j in range(2):
        cubes.append(Cube([i - 2.5, j - 1, 0]))

camera = Camera()

while running:
    fps = clock.get_fps()
    if not handleEvents(pg.event.get(), camera):
        running = False

    screen.fill("white")
    
    projectionMatrix = rotationMatrixAll(camera)
    for cube in cubes:
        cube.CalculateProjection(projectionMatrix, camera)
        cube.Draw(screen, True, True)

    pg.display.flip()
    clock.tick(fps)
    
