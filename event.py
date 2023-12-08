import pygame as pg
import math

def handleEvents(events, camera):
    for event in events:
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                camera.position[2] += 0.25
            if event.key == pg.K_s:
                camera.position[2] -= 0.25
            if event.key == pg.K_a:
                camera.position[0] -= 0.25
            if event.key == pg.K_d:
                camera.position[0] += 0.25
            if event.key == pg.K_q:
                camera.rotation[1] -= math.pi / 12
            if event.key == pg.K_e:
                camera.rotation[1] += math.pi / 12
            if event.key == pg.K_LCTRL:
                camera.position[1] -= 0.25
            if event.key == pg.K_SPACE:
                camera.position[1] += 0.25
    return True