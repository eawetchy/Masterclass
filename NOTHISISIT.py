import maya.cmds as cmds
import sympy

def RBFbasis (r,s):
    # x1, x2: 3D points expressed as row matrices
    R = ( r**2 + s**2)**0.5
    return R 
    
def closestPoint(lp, vertPos): #landmark point, query points
    e = []
    for m in range(0, (len(vertPos)-1)):
        w = sympy.Point3D(lp).distance(sympy.Point3D(vertPos[m]))
        if w != 0:
            e.append(w)
    return min(e)
    
def rbfeval(C, W, P):
    P2 = sympy.zeros(len(P),3)
    h = sympy.zeros(W.shape[0],1)
    index = 0
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(sympy.Point3D(P[i]).distance( sympy.Point3D( C[j] ) ), closestPoint( C[j], P ))
    #reconstruct point i
        temp = W.transpose() * h
        print temp
        P2[index] = temp[0]
        P2[index+1] = temp[1]
        P2[index+2] = temp[2]
        index+=3
        print P2
    return P2

sourceName = cmds.ls(sl=1)
targetName = cmds.ls(sl=1)

SelP0 = cmds.ls(sl=1, fl=True)
SelP1 = cmds.ls(sl=1, fl=True)

AllP0 = cmds.ls(sl=1, fl=True)
AllP1 = cmds.ls(sl=1, fl=True)

#----------------#

KP0 = []
KP1 = []
for i in SelP0:
    KP0.append( cmds.pointPosition(i, w=True) )
for j in SelP1:
    KP1.append( cmds.pointPosition(j, w=True) )
    
P0 = []
P1 = []
for j in AllP0:
    P0.append( cmds.pointPosition(j, w=True) )
for k in AllP1:
    P1.append( cmds.pointPosition(k, w=True) )
    
n = len(P0)
m = len(KP1)
    
H = sympy.zeros(m);
for i in range(0, m):
    for j in range(0, m):
        H[i,j]=RBFbasis( sympy.Point3D(KP0[i]).distance( sympy.Point3D( KP0[j] ) ), closestPoint( KP0[j], KP0 ) )

Htrans = H.transpose()
A = Htrans * H
w = (A.inv() * Htrans) * sympy.Matrix(KP1)


P02 = rbfeval(KP0, w, P0)

ind = 0
for i in range(0,n):
    cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllP0[i])
