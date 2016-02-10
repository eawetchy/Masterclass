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

SelP0 = cmds.ls(sl=1)
SelP1 = cmds.ls(sl=1)
KP0 = []
KP1 = []
for i in range(0, len(SelP1)):
    KP0.append( cmds.pointPosition(SelP0[i], w=True) )
    KP1.append( cmds.pointPosition(SelP1[i], w=True) )
    
AllP0 = cmds.ls(sl=1)
AllP1 = cmds.ls(sl=1)
P0 = []
P1 = []
for j in range(0, 7):
    P0.append( cmds.pointPosition("nurbsCircle1.cv["+str(j)+"]", w=True) )
    P1.append( cmds.pointPosition("nurbsCircle2.cv["+str(j)+"]", w=True) )
    
H = sympy.zeros(len(P0),len(KP0));
for i in range(0, len(P0)):
    for j in range(0, len(KP0)):
        H[i,j]=RBFbasis( sympy.Point3D(P0[i]).distance( sympy.Point3D( KP0[j] ) ), closestPoint( KP0[j], P0 ) )

Htrans = H.transpose()
Hsquare = Htrans * H
Hinv = Hsquare.inv()
w = Hinv * Htrans *sympy.Matrix(P0)

P2 = sympy.zeros(len(P0), 3)
h = sympy.zeros(len(w)/3,1) #vector with number of weights elements
for i in range(0,len(P0)):
    for j in range(0, len(KP1)):
        h[0] = RBFbasis( sympy.Point3D(P0[0]).distance( sympy.Point3D(KP1[0]) ), closestPoint(KP1[0], P0) )
    # reconstruct point i
    P2[0] = w.transpose() * h
