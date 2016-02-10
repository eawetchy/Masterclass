import maya.cmds as cmds
import numpy
from scipy import spatial

def RBFbasis (r,s):
    # x1, x2: 3D points expressed as row matrices
    R = ( r**2 + s**2)**0.5
    return R 
    
def closestPoint(lp, vertPos): #landmark point, query points
    e = []
    for m in range(0, (len(vertPos)-1)):
        if (numpy.array_equal(lp, vertPos[m])):
            continue
        w = scipy.spatial.distance.euclidean(lp, vertPos[m])
        #w = sympy.Point3D(lp).distance(sympy.Point3D(vertPos[m]))
        if w != 0:
            e.append(w)
    return min(e)
    
def rbfeval(C, W, P):
    P2 = numpy.copy(P)
    h = numpy.asmatrix(numpy.zeros((len(W),1)))
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(scipy.spatial.distance.euclidean(P[i], C[j]), closestPoint( C[j], P ))
    #reconstruct point i
        P2[i] = (W.transpose() * h).transpose()
    return P2

sourceName = cmds.ls(sl=1)
targetName = cmds.ls(sl=1)

SelP0 = cmds.ls(sl=1, fl=True)
SelP1 = cmds.ls(sl=1, fl=True)

AllP0 = cmds.ls(sl=1, fl=True)
AllP1 = cmds.ls(sl=1, fl=True)
AllPBlend = cmds.ls(sl=1, fl=True)

#----------------#

KP0 = []
KP1 = []
for i in SelP0:
    KP0.append( cmds.pointPosition(i, w=True) )
for j in SelP1:
    KP1.append( cmds.pointPosition(j, w=True) )
KP0 = numpy.matrix(KP0)
KP1 = numpy.matrix(KP1)
    
P0 = []
P1 = []
for j in AllP0:
    P0.append( cmds.pointPosition(j, w=True) )
for k in AllP1:
    P1.append( cmds.pointPosition(k, w=True) )
P0 = numpy.matrix(P0)
P1 = numpy.matrix(P1)

#------------
  
n = len(P0)
m = len(KP1)
    
H = numpy.zeros((m,m))
for i in range(0, m):
    for j in range(0, m):
        H[i,j]=RBFbasis( scipy.spatial.distance.euclidean(KP0[i], KP0[j]), closestPoint( KP0[j], KP0 ) )

H = numpy.asmatrix(H)
w = numpy.linalg.solve(H, KP1)


P02  = rbfeval(KP0, w, P0)

ind = 0
for i in range(0,n):
    cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllP0[i])
