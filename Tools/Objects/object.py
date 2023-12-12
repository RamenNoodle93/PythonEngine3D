import numpy as np
import math
import pygame as pg

from Tools.utils import *

class Object:
    
    def __init__(self, position, rotation, scale, color, size):
        self.nodes = np.zeros((0, 4), float)
        self.edges = np.zeros((0, 2), int)
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.size = size
        self.color = color

    def AddEdges(self, edgeList):
        
        self.edges = np.vstack([self.edges, edgeList])
        
    def AddNodes(self, nodeList):
        
        for node in nodeList:
            node[0] *= self.size
            node[1] *= self.size
            node[2] *= self.size
            
        onesColumn = np.ones((len(nodeList), 1))
        onesAdded = np.hstack((nodeList, onesColumn))
        self.nodes = np.matrix(np.transpose(np.vstack((self.nodes, onesAdded))))
        
    def CalculateProjection(self, rotationMatrix, camera):
        
        count = self.nodes.shape[1]
        
        self.visible = np.full((count), True)
        
        rotatedSelf = np.dot(rotationMatrixAll(self), self.nodes)

        fullProjection = np.dot(rotationMatrix, translationMatrix(camera, self.position))
        projections = np.dot(fullProjection, rotatedSelf)

        for i in range(projections.shape[1]):
            if projections[:, i][2] <= 0:
                self.visible[i] = False

        perspective = np.zeros((count, 2))
        
        for i in range(count):
            if projections[2, i] == 0:
                projections[2, i] += 1e-4
            
            if projections[2, i] <= -0.25:
                projections[2, i] = 1e-4

            projections[2, i] = abs(projections[2, i])
            
            perspective[i, 0] = (0.5 * (1 / math.tan(hFov / 2)) * self.scale * projections[0, i] / projections[2, i])
            perspective[i, 1] = (0.5 * (1 / math.tan(vFov / 2)) * self.scale * projections[1, i] / projections[2, i])
        
        self.perspective = perspective

    def Draw(self, surface, showNodes, showEdges):
        
        if showNodes:
            for index, point in enumerate(self.perspective):
                if self.visible[index]:
                    pg.draw.circle(surface, self.color, getCentered(point), 3)
                
        if showEdges:
            for edge in self.edges:
                if not bothPointsHidden(self.visible, edge):
                    start = getCentered(self.perspective[edge[0]])
                    end = getCentered(self.perspective[edge[1]])
                    pg.draw.aaline(surface, self.color, start, end)