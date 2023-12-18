from numpy import kaiser
import pygame as pg
import math
import copy
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from CustomObjects.player import Player
from CustomObjects.asteroid import Asteroid
from CustomObjects.bullet import Bullet
from Tools.utils import *
from settings import *

class Game:
    
    def __init__(self, display):
        self.defaultColor = (1, 1, 1)

        self.display = display

        self.objectList = []
        self.objectList.append(Player(color = self.defaultColor))
        
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        self.objectList.append([])
        
        self.player = self.objectList[0]
        self.asteroids = self.objectList[1]
        self.bullets = self.objectList[2]
        self.debris = self.objectList[3]
        
        self.lives = 3
        self.score = 0

        self.UpdateScore()

    def GetStartVal(self):
        #Pozycja startowa kamery
        position = [0, 0, -15]
        #Kat podany w stopniach, nie w radianach
        rotation = [0, 0, 0]

        self.boundary = abs(position[2]) * math.tan(degToRad(hFov / 2))
        return [position, rotation]

    def HandleEvents(self, camera):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and len(self.objectList[2]) < 5:
                if self.player.Shoot():
                    self.AddObject(Bullet(copy.deepcopy(self.player.position), copy.deepcopy(self.player.rotation)))
        return True

    def AddObject(self, obj):
        name = type(obj).__name__
        if name == 'Asteroid':
            self.objectList[1].append(obj)
        elif name =='Bullet':
            self.objectList[2].append(obj)
            
    def Update(self, camera):
        pressed = pg.key.get_pressed()
    
        if not self.player.collision:
            if time.time() - 3 > self.player.lastCollision and self.player.lives > 0:
                if not self.player.alive:
                    self.debris = []
                    self.player.Respawn()
                if time.time() - 0.5 > self.player.lastColorChange:
                    if self.player.color == self.defaultColor:
                        self.player.color = [color * 0.4 for color in self.defaultColor]
                    else:
                        self.player.color = self.defaultColor
                    self.player.lastColorChange = time.time()                        

                if time.time() - 6 > self.player.lastCollision:
                    self.player.collision = True
                    self.player.color = self.defaultColor

            self.player.flame.color = self.player.color

        if self.player.alive:
            self.player.Move(pressed)

        self.Wrap(self.player)

        for obj in self.objectList[1]:
            obj.Move()
            self.Wrap(obj)
                
        if len(self.objectList[1]) < 5:
            newAst = Asteroid(playerPos = copy.deepcopy(self.player.position), boundary = copy.deepcopy(self.boundary))
            newAst.position = makeRandPos(self.player.position, self.boundary)
            self.AddObject(copy.deepcopy(newAst))

        for index1, obj in enumerate(self.objectList[2]):
            if obj.Lifetime():
                self.objectList[2].pop(index1)
                break
            obj.Move()
            self.Wrap(obj)
            for index2, asteroid in enumerate(self.objectList[1]):
                if asteroid.CheckCollision(obj):
                    self.objectList[2].pop(index1)
                    
                    newAsteroids = asteroid.Break()

                    if newAsteroids != 0:
                        for obj in newAsteroids:
                            self.AddObject(obj)

                    if asteroid.count == 2:
                        self.score += 20
                    elif asteroid.count == 1:
                        self.score += 50
                    else:
                        self.score += 70

                    self.UpdateScore()

                    self.objectList[1].pop(index2)
                    
                    break

        if self.player.collision:
            for obj in self.objectList[1]:
                if self.player.CheckCollision(obj):
                    self.player.Collision()
                    self.debris = self.player.RenderParticles()
                    self.UpdateScore()                
        
    def Wrap(self, obj):
        if obj.position[0] > self.boundary:
            obj.position[0] = -self.boundary
        elif obj.position[0] < -self.boundary:
            obj.position[0] = self.boundary
        if obj.position[1] > self.boundary:
            obj.position[1] = -self.boundary
        elif obj.position[1] < -self.boundary:
            obj.position[1] = self.boundary

    def UpdateScore(self):
        textSurface = pg.Surface((256, 128))
        textSurface.fill((0, 0, 0))
        pg.font.init()
        myfont = pg.font.SysFont('Comic Sans MS ', 45)
        textDis = myfont.render(f'Score: {self.score}', False, (255, 255, 255))
        textSurface.blit(textDis, (0, 0))
        for i in range(self.player.lives):
            pg.draw.polygon(textSurface, (255, 255, 255), ((30 + 45 * i, 120), (60 + 45 * i, 120), (45 + 45 * i, 70)), 2)
        self.texID = textureFromSurface(textSurface)

    def RenderScore(self):
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glEnable(GL_TEXTURE_2D)
        glColor3f(self.defaultColor[0], self.defaultColor[1], self.defaultColor[2])
        glBegin(GL_QUADS)
    
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.boundary + 1.0, self.boundary - 1.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.boundary + 1.0, self.boundary - 3.0, 0.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-self.boundary + 5.0, self.boundary - 3.0, 0.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-self.boundary + 5.0, self.boundary - 1.0, 0.0)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

    def Render(self, camera, showNodes = False, showEdges = True, showHitbox = False):
        glPushMatrix()

        glRotatef(camera.rotation[0], 1, 0, 0)
        glRotatef(camera.rotation[1], 0, 1, 0)
        glRotatef(camera.rotation[2], 0, 0, 1)

        glTranslatef(camera.position[0], camera.position[1], camera.position[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        

        self.RenderScore()

        self.player.Draw(showNodes, showEdges, showHitbox)
        if showHitbox:
            self.player.ProjectCollision()
            
        for obj in self.debris:
            obj.position[0] += obj.movement[0]
            obj.position[1] += obj.movement[1]
            obj.rotation[0] += obj.rotate
            obj.rotation[2] += obj.rotate
            obj.Draw(showNodes, showEdges, True)

        for obj in self.asteroids:
            obj.Draw(showNodes, showEdges, showHitbox)
            if showHitbox:
                obj.ProjectCollision()
            glColor3f(self.defaultColor[0], self.defaultColor[1], self.defaultColor[2])            

        for obj in self.bullets:
            obj.Draw(True, False, showHitbox)

        if self.player.moving:
            self.player.flame.Draw(showNodes, showEdges, showHitbox)  

        glPopMatrix()