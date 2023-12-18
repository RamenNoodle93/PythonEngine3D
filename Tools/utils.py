import math
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random as rand

def degToRad(angle):
    return angle * math.pi / 180    

def textureFromSurface(pygameSurface):

    dimensions = pygameSurface.get_rect()

    if ((dimensions.width & (dimensions.width - 1) == 0) and dimensions.width != 0) and ((dimensions.height & (dimensions.height - 1) == 0) and dimensions.height != 0):
        texID = glGenTextures(1)
        rgbaSurface = pg.image.tostring(pygameSurface, 'RGBA')
        glBindTexture(GL_TEXTURE_2D, texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        surface_rect = pygameSurface.get_rect()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface_rect.width, surface_rect.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgbaSurface)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, surface_rect.width, surface_rect.height, GL_RGBA, GL_UNSIGNED_BYTE, rgbaSurface)
        glBindTexture(GL_TEXTURE_2D, 0)
    
        return texID

def makeRandPos(restrictedPos, boundary, minDist = 2, axisZ = False):
        randX = rand.choice([rand.uniform(-boundary, restrictedPos[0] - minDist), rand.uniform(boundary, restrictedPos[0] + minDist)])
        randY = rand.choice([rand.uniform(-boundary, restrictedPos[1] - minDist), rand.uniform(boundary, restrictedPos[1] + minDist)])
        if axisZ:
            randZ = rand.choice([rand.uniform(-boundary, restrictedPos[2] - minDist), rand.uniform(boundary, restrictedPos[2] + minDist)])
        else:
            randZ = 0
        return [randX, randY, randZ]