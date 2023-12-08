import math
import numpy as np
from Tools.constants import *

def rotationMatrixX(rotX): #Macierz rzutujaca osi X --------------------------------------------------------
    
    matrix = np.matrix([
    [1, 0, 0, 0],
    [0, math.cos(rotX), math.sin(rotX), 0],
    [0, -math.sin(rotX), math.cos(rotX), 0],
    [0, 0, 0, 1]
    ])
    
    return matrix

def rotationMatrixY(rotY): #Macierz rzutujaca osi Y --------------------------------------------------------
    
    matrix = np.matrix([
    [ math.cos(rotY), 0,math.sin(rotY), 0],
    [ 0, 1, 0, 0],
    [ -math.sin(rotY), 0, math.cos(rotY), 0],
    [ 0, 0, 0, 1 ],
    ])
    
    return matrix
    
def rotationMatrixZ(rotZ): #Macierz rzutujaca osi Z --------------------------------------------------------
    
    matrix = np.matrix([
    [ math.cos(rotZ), math.sin(rotZ), 0, 0],
    [- math.sin(rotZ), math.cos(rotZ), 0, 0],
    [ 0, 0, 1, 0],
    [ 0, 0, 0, 1 ]
    ])
    
    return matrix

def translationMatrix(camera, objectPos): #Macierz przesuwania ----------------------------------------------------
    
    matrix = np.matrix([
    [1, 0, 0, -camera.position[0] + objectPos[0]],
    [0, 1, 0, -camera.position[1] + objectPos[1]],
    [0, 0, 1, -camera.position[2] + objectPos[2]],
    [0, 0, 0, 1]
    ])
    
    return matrix

def rotationMatrixAll(camera):
    return np.dot(rotationMatrixX(camera.rotation[0]), np.dot(rotationMatrixY(camera.rotation[1]), rotationMatrixZ(camera.rotation[2])))

def fullProjectionMatrix(camera):
    return np.dot(rotationMatrixAll(camera), translationMatrix(camera))

def centerPoint(x, y): #Koordynaty punktu wzgledem srodka ekranu, czyli punkt (0, 0) to srodek -------------
    return (x + width / 2, height / 2 - y)

def getCentered(point): #Zwraca koordynaty wysrodkowanego punktu -------------------------------------------
    return (centerPoint(point[0], point[1]))
