import maya.cmds as cmds
import numpy

#------------------------------------------------------------#
#															 #
#															 #	
# Turn on "Track selection order" in preferences > selection!#
#															 #
#															 #
#------------------------------------------------------------#

'''calculate radial basis function value
	r: distance between two key points'''
def RBFbasis (r):
    R = (r**2 + 1)**0.5
    return R 
    
'''solve for all points in the source mesh using calculated weights
	C: source key points
	W: RBF weights
	P: all source vertices'''
def rbfeval(C, W, P):
    P2 = numpy.copy(P)
    h = numpy.asmatrix(numpy.zeros((len(W),1))) # vector with n = number of weights rows and 1 column
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(numpy.linalg.norm(P[i] - C[j]), 1)
    #reconstruct point i
        P2[i] = (W.transpose() * h).transpose()
    return P2

#----------Object and key point selection---------------------#


# stores names of source and target meshes
cmds.select("source1")
sourceName = cmds.ls(sl=1)
cmds.select("target")
targetName = cmds.ls(sl=1)

# selects key points
cmds.select(clear=True)
SKP = [194, 254, 381, 380, 189, 199, 184]
for i in SKP:
    cmds.select("source1.vtx["+str(i)+"]", add = True)
SelP0 = cmds.ls(fl=True, os=True)
cmds.select(clear=True)
TKP = [2986, 3626, 381, 380, 2949, 3347, 2911]
for i in TKP:
    cmds.select("target.vtx["+str(i)+"]", add = True)
SelP1 = cmds.ls(fl=True, os=True)

cmds.select(clear=True)
cmds.select("source1.vtx[0:381]")
AllP0 = cmds.ls(sl=1, fl=True)

#----------Store key points in matrix form-------------------#

KP0 = []
KP1 = []
for i in SelP0:
    KP0.append( cmds.pointPosition(i, w=True) )
for j in SelP1:
    KP1.append( cmds.pointPosition(j, w=True) )
KP0 = numpy.matrix(KP0)
KP1 = numpy.matrix(KP1)
    
P0 = []
for j in AllP0:
    P0.append( cmds.pointPosition(j, w=True) )
P0 = numpy.matrix(P0)

#----------RBF------------------------------------------------#
  
n = len(P0)
m = len(KP1)

# build matrix H using evaluated RBF between key points on the source mesh
H = numpy.zeros((m,m))
for i in range(0, m):
    for j in range(0, m):
        H[i,j]=RBFbasis( numpy.linalg.norm(KP0[i] - KP0[j]), 1) # closestPoint( KP0[j], KP0 ) )
H = numpy.asmatrix(H)

# f(x) = H * w
# f(x) --> key points on target mesh / deformed source key points:
# KP1 = H * w
# solve for w
w = numpy.linalg.solve(H, KP1)

# evaluate RBF for every vertex on source mesh using w
P02  = rbfeval(KP0, w, P0)

# move source vertices to new positions in deformed source mesh
ind = 0
for i in range(0,n):
    cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllP0[i])

# query new vertex positions to determine new normals
cmds.select(clear=True)
cmds.select("source1.vtx[0:381]")
AllPDef = cmds.ls(sl=1, fl=True)
P2 = []
for i in AllPDef:
    P2.append( cmds.pointPosition(i) )
P2 = numpy.matrix(P2)
