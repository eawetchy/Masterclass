'''
import sympy

def RBF (x1, x2):
    # x1, x2: 3D points expressed as row matrices
    s = x1 - x2
    R = sympy.sqrt((x1 - x2).transpose()*(x1 - x2) + s.transpose()*s)
    return R 

M = sympy.eye(6)

for i in range(0,5):
    for j in range(0,5) :
        x1 = sympy.Matrix(sourceVtcs[sourceLM[i]])
        x2 = sympy.Matrix(sourceVtcs[sourceLM[j]])
        M[i,j] = RBF(x1, x2)


F = sympy.zeros(6,3)
for i in range(0,5):
    for j in range(0,2):
            F[i,j] = sourceVtcs[sourceLM[i]][j

'''


#SECOND TRY, BETTER!
import sympy
import maya.cmds as cmds

def RBF (x1, x2, s):
    # x1, x2: 3D points expressed as row matrices
    R = ( x1.distance(x2)**2 + s**2)**0.5
    return R 
    
def closestPoint (xi, vertPos): #current point, vertex position array, landmark array
    d = [] #distances between LM points
    for j in range(0,len(vertPos)):
        v = x1.distance(sourceVtcs[j])
        if v != 0:
            d.append(v)
    return min(d)
    
def closestLMPoint (xi, vertPos, LM): #current point, vertex position array, landmark array
    d = [] #distances between LM points
    for i in range(0,len(LM)):
        v = x1.distance(sourceVtcs[sourceLM[i]])
        if v != 0:
            d.append(v)
    return min(d)

#M: matrix of evaluated RBF for each landmark point
M = sympy.eye(6)

for i in range(0,5):
    for j in range(0,5) :
        x1 = sympy.Point3D(sourceVtcs[sourceLM[i]])
        x2 = sympy.Point3D(sourceVtcs[sourceLM[j]])
        s = closestLMPoint(x2, sourceVtcs, sourceLM)
        M[i,j] = RBF(x1, x2, s)

#matrix of "actual" result values as f(x) --> x
F = sympy.zeros(6,3)
for i in range(0,5):
    for j in range(0,2):
            F[i,j] = sourceVtcs[sourceLM[i]][j]
            
MInv = M.inv()
X = F.transpose() * MInv

M2 = sympy.eye(6)

cmds.progressWindow(isInterruptable=1)

for i in range(0, len(sourceVtcs)-2):
    x1 = sympy.Point3D(sourceVtcs[i])
    x2 = sympy.Point3D(sourceVtcs[i+1])
    s = closestPoint(x2, sourceVtcs)
    M2[i,j] = RBF(x1, x2, s)
    if cmds.progressWindow(query=1, isCancelled=1) :
        break

#THIRD TRY

import sympy
import maya.cmds as cmds

def RBF (x1, x2, s):
    # x1, x2: 3D points expressed as row matrices
    R = ( x1.distance(x2)**2 + s**2)**0.5
    return R 
    
def closestLMPoint (xi, vertPos, LM): #current point, vertex position array, landmark array
    d = [] #distances between LM points
    for k in range(0,len(LM)):
        v = xi.distance(vertPos[LM[k]])
        if v != 0:
            d.append(v)
    return min(d)

def closestPoint(xi, vertPos):
    e = []
    for m in range(0, (len(vertPos)-1)):
        w = xi.distance(vertPos[m])
        if w != 0:
            e.append(w)
    return min(e)

#M: matrix of evaluated RBF for each landmark point
M = sympy.eye(6)

for i in range(0,5):
    for j in range(0,5) :
        x1 = sympy.Point3D(sourceVtcs[sourceLM[i]])
        x2 = sympy.Point3D(targetVtcs[targetLM[j]])
        s = closestLMPoint(x2, targetVtcs, targetLM)
        M[i,j] = RBF(x1, x2, s)

#matrix of "actual" result values as f(x) --> x
F = sympy.zeros(6,3)
for i in range(0,5):
    for j in range(0,2):
            F[i,j] = targetVtcs[targetLM[i]][j]
            
MInv = M.inv()
X = MInv * F

TP = sympy.eye(len(sourceVtcs))
for m in range(0, (len(sourceVtcs)-1)):
    for n in range(0, (len(sourceVtcs)-1)):
        print m
        y1 = sympy.Point3D(sourceVtcs[m])
        y2 = sympy.Point3D(sourceVtcs[n])
        t = closestPoint(y2, sourceVtcs)
        TP[m,n] = RBF(y1, y2, t)
