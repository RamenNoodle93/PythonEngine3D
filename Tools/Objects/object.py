import numpy as np
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Object:
    
    def __init__(self, position, rotation, scale, color):
        self.nodes = np.zeros((0, 3), float)
        self.edges = np.zeros((0, 2), int)
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color

    def AddEdges(self, edgeList):
        
        self.edges = np.vstack([self.edges, edgeList])
        
    def AddNodes(self, nodeList):
        
        for node in nodeList:
            node[0] *= self.scale
            node[1] *= self.scale
            node[2] *= self.scale
            
        self.nodes = np.vstack([self.nodes, nodeList])
        
    # def CalculateProjection(self, rotationMatrix, camera):
        
    #     count = self.nodes.shape[1]
        
    #     self.visible = np.full((count), True)
        
    #     rotatedSelf = np.dot(rotationMatrixAll(self), self.nodes)

    #     fullProjection = np.dot(rotationMatrix, translationMatrix(camera, self.position))
    #     projections = np.dot(fullProjection, rotatedSelf)

    #     for i in range(projections.shape[1]):
    #         if projections[:, i][2] <= 0:
    #             self.visible[i] = False

    #     perspective = np.zeros((count, 2))
        
    #     for i in range(count):
    #         if projections[2, i] == 0:
    #             projections[2, i] += 1e-4
            
    #         if projections[2, i] <= -0.25:
    #             projections[2, i] = 1e-4

    #         projections[2, i] = abs(projections[2, i])
            
    #         perspective[i, 0] = (0.5 * (1 / math.tan(hFov / 2)) * self.scale * projections[0, i] / projections[2, i])
    #         perspective[i, 1] = (0.5 * (1 / math.tan(vFov / 2)) * self.scale * projections[1, i] / projections[2, i])
        
    #     self.perspective = perspective

    def CreateHitbox(self, shape = 1):
        Xmin = min(self.nodes[:, 0])
        Xmax = max(self.nodes[:, 0])
        Ymin = min(self.nodes[:, 1])
        Ymax = max(self.nodes[:, 1])
        Zmin = min(self.nodes[:, 2])
        Zmax = max(self.nodes[:, 2])

        nodes = []
        for x in [Xmin, Xmax]:
            for y in [Ymin, Ymax]:
                for z in [Zmin, Zmax]:
                    nodes.append([x, y, z])
                    
        edges = []
        
        for n in [0, 1, 4, 5]:
            edges.append([n, n + 2])
        for n in range(4):
            edges.append([n, n + 4])
        for n in range(0, 8, 2):
            edges.append([n, n + 1])
        
        self.boundingBox = Object(self.position, self.rotation, 1, (255, 255, 255))
        self.boundingBox.AddNodes(nodes)
        self.boundingBox.AddEdges(edges)

    def Draw(self, showNodes, showEdges, showHitbox = False):
        
        glPushMatrix()
        
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)
        
        glTranslatef(self.position[0], self.position[1], self.position[2])

        glColor3f(self.color[0], self.color[1], self.color[2])

        if showNodes:
            glBegin(GL_POINTS)
            glPointSize(10)
            for node in self.nodes:
                glVertex3f(node[0], node[1], node[2])
            glEnd()
            
        if showEdges:
            glBegin(GL_LINES)
            for edge in self.edges:
                for vertex in edge:
                    glVertex3fv(self.nodes[vertex])
            glEnd()
            
        if showHitbox:
            glColor3f(self.boundingBox.color[0], self.boundingBox.color[1], self.boundingBox.color[2])
            glBegin(GL_LINES)
            for edge in self.boundingBox.edges:
                for vertex in edge:
                    glVertex3fv(self.boundingBox.nodes[vertex])
            glEnd()

        glPopMatrix()