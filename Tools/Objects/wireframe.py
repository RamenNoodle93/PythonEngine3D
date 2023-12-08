import numpy as np
import pygame as pg
from Tools.matrix import *
from Tools.constants import *
from Tools.utils import *

class Wireframe:
    def __init__(self, position, scale, color):
        self.nodes = np.zeros((0, 4), float)
        self.edges = np.zeros((0, 2), int)
        self.position = position
        self.scale = scale
        self.color = color

    def AddEdges(self, edgeList):
        
        self.edges = np.vstack([self.edges, edgeList])
        
    def AddNodes(self, nodeList):
        
        onesColumn = np.ones((len(nodeList), 1))
        onesAdded = np.hstack((nodeList, onesColumn))
        self.nodes = np.matrix(np.transpose(np.vstack((self.nodes, onesAdded))))
        
    def CalculateProjection(self, rotationMatrix, camera):
        
        count = self.nodes.shape[1]
        
        self.visible = np.full((count), True)
        fullProjection = np.dot(rotationMatrix, translationMatrix(camera, self.position))
        projections = np.dot(fullProjection, self.nodes)

        for i in range(projections.shape[1]):
            if projections[:, i][2] <= 0:
                self.visible[i] = False

        perspective = np.zeros((count, 2))
        
        for i in range(count):
            if projections[2, i] == 0:
                projections[2, i] += 1e-4
            
            if projections[2, i] <= -1:
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
                    