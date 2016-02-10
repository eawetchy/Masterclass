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

sourceName = cmds.ls(sl=1)
targetName = cmds.ls(sl=1)

SelP0 = cmds.ls(sl=1, fl=True)
SelP1 = cmds.ls(sl=1, fl=True)
KP0 = []
KP1 = []
for i in SelP0:
    KP0.append( cmds.pointPosition(i, w=True) )
for j in SelP1:
    KP1.append( cmds.pointPosition(j, w=True) )
    
AllP0 = cmds.ls(sl=1, fl=True)
AllP1 = cmds.ls(sl=1, fl=True)
P0 = []
P1 = []
for j in AllP0:
    P0.append( cmds.pointPosition(j, w=True) )
for k in AllP1:
    P1.append( cmds.pointPosition(k, w=True) )
    
n = len(P0)
m = len(KP0)
    
H = sympy.zeros(n, m);
for i in range(0, n):
    for j in range(0, m):
        H[i,j]=RBFbasis( sympy.Point3D(P0[i]).distance( sympy.Point3D( KP0[j] ) ), closestPoint( KP0[j], P0 ) )

Htrans = H.transpose()
Hsquare = Htrans * H
Hinv = Hsquare.inv()
w = Hinv * Htrans *sympy.Matrix(P1)

Y = H*w

ind = 0
for i in range(0,n):
    cmds.move(float(Y[ind]), float(Y[ind+1]), float(Y[ind+2]), AllP0[i])
    ind += 3 
