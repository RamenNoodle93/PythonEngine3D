import numpy as np
import math
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

    def ProjectCollision(self):
        rotation = self.rotation
        position = self.position
        nodes = self.boundingBox.nodes        

        rotation = [n * math.pi / 180 for n in rotation]

        xTransform = np.array([
        [1, 0, 0],
        [0, math.cos(rotation[0]), math.sin(rotation[0])],
        [0, -math.sin(rotation[0]) ,math.cos(rotation[0])]
        ])
            
        yTransform = np.array([
        [math.cos(rotation[1]), 0, -math.sin(rotation[1])],
        [0, 1, 0],
        [math.sin(rotation[1]), 0, math.cos(rotation[1])]
        ])
            
        zTransform = np.array([
        [math.cos(rotation[2]), -math.sin(rotation[2]), 0],
        [math.sin(rotation[2]), math.cos(rotation[2]), 0],
        [0, 0, 1]
        ])

        transformationMatrix = np.dot(xTransform, np.dot(yTransform, zTransform))
        
        transformed = []

        for node in nodes:
            node = np.dot(node, transformationMatrix)
            
            node[0] += position[0]
            node[1] += position[1]
            node[2] += position[2]
                
            transformed.append(node)
            
        arr = np.array(transformed)

        maxInd = np.argmax(arr, axis = 0)
        minInd = np.argmin(arr, axis = 0)
        
        xMax, yMax, zMax = arr[maxInd]
        xMin, yMin, zMin = arr[minInd]
        
        glPointSize(5)
        glBegin(GL_POINTS)
        
        glVertex3f(xMax[0], -8, xMax[2])
        glVertex3f(xMin[0], -8, xMin[2])
        glVertex3f(-8, yMax[1], yMax[2])
        glVertex3f(-8, yMin[1], yMin[2])
        
        glEnd()

        return [xMax, xMin, yMax, yMin]        

    def CheckCollision(self, otherObj):
        boundsSelf = self.ProjectCollision()
        boundsOther = otherObj.ProjectCollision()
        
        if (boundsSelf[0][0] > boundsOther[1][0] and boundsSelf[1][0] < boundsOther[0][0]) and (boundsSelf[2][1] > boundsOther[3][1] and boundsSelf[3][1] < boundsOther[2][1]):
            return True
        else:
            return False

    def Draw(self, showNodes, showEdges, showHitbox = False):
        
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        glColor3f(255,0,0)
        
        glPointSize(4.0)
        
        if showNodes:
            glBegin(GL_POINTS)
            
            for node in self.nodes:
                
                glVertex3f(node[0], node[1], node[2])
            glEnd()
            
        glColor3f(self.color[0], self.color[1], self.color[2])

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