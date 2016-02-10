import maya.cmds as cmds
import numpy

# automatically find key points
# will return an array containing positions in space of all object vertices
# code by Dorian Fevrier found on http://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-(English-Translation)
def getVtxPos( shapeNode ) :
	vtxWorldPosition = []    
	vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
	for i in vtxIndexList :
		curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
		vtxWorldPosition.append( curPointPosition )
	return vtxWorldPosition


# returns the highest/lowest value in the chosen direction
def getExtremePoint( dir, high, vertexList ):
    if dir == "x":
        val = 0  
    if dir == "y":
        val = 1
    if dir == "z":
        val = 2    
    vertIdx = 0
    extremeValue = vertexList[0][val]  
    if high == True:
        for i in range(0, len(vertexList)):
            if vertexList[i][val] > extremeValue:
                extremeValue = vertexList[i][val]
                vertIdx = i
    else:
        for i in range(0, len(vertexList)):
            if vertexList[i][val] < extremeValue:
                extremeValue = vertexList[i][val]
                vertIdx = i 
    return vertIdx

sourceVtcs = getVtxPos( sourceName[0] + "Shape")
toH = getExtremePoint( "y", True, sourceVtcs) # top of head
boH = getExtremePoint("z", False, sourceVtcs) # back of head
toN = getExtremePoint("z", True, sourceVtcs) # tip of Nose
rE = getExtremePoint("x", False, sourceVtcs) # outside of right ear
lE = getExtremePoint("x", True, sourceVtcs) # outside of left ear

lowerHalf = []
lHIdx = []
c = 0
for i in sourceVtcs:
	if (i[1] < sourceVtcs[toN][1]):
		lowerHalf.append(i)
		lHIdx.append(c)
	c += 1
	
# select verts in lower half to test
for i in lHIdx:
    cmds.select("neutral.vtx["+str(i)+"]", add = True)

#----------------#

def RBFbasis (r,s):
    #R = ( r**2 + s**2)**0.5
    R = (r**2 + 1)**0.5
    return R 
    
def closestPoint(lp, vertPos): #landmark point, query points
    minDist = 500000
    for m in range(0, (len(vertPos)-1)):
        if (numpy.array_equal(lp, vertPos[m])):
            continue
        d = distance.euclidean(lp, vertPos[m])
        if d < minDist:
            minDist = d
    return d
    
def rbfeval(C, W, P):
    P2 = numpy.copy(P)
    h = numpy.asmatrix(numpy.zeros((len(W),1)))
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(numpy.linalg.norm(P[i] - C[j]), 1)
            #h[j] = RBFbasis(distance.euclidean(P[i], C[j]), 1) # closestPoint( C[j], P ))
    #reconstruct point i
        P2[i] = (W.transpose() * h).transpose()
    return P2

sourceName = cmds.ls(sl=1)
targetName = cmds.ls(sl=1)


# turn on "Track selection order" in preferences > selection!
SelP0 = cmds.ls(fl=True, os=True)
SelP1 = cmds.ls(fl=True, os=True)

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
        H[i,j]=RBFbasis( numpy.linalg.norm(KP0[i] - KP0[j]), 1) # closestPoint( KP0[j], KP0 ) )

H = numpy.asmatrix(H)
w = numpy.linalg.solve(H, KP1)


P02  = rbfeval(KP0, w, P0)

#------------

# duplicate source, then apply the transformation
cmds.duplicate(sourceName[0], n = "sourceDeformed")
cmds.select(clear=True)
cmds.select("sourceDeformed.vtx[0:381]")
AllPDef = cmds.ls(sl=1, fl=True)
P2 = []
for i in AllPDef:
    P2.append( cmds.pointPosition(i) )
P2 = numpy.matrix(P2)

ind = 0
for i in range(0,n):
    cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllPDef[i])

#------------

# find local source vertex coordinate systems before deformation
for i in range(0, len(P0)):
    localO = findLocal(AllP0[i], N0[i])

#------------

# find local source vertex coordinate systems after deformation
for i in range(0, len(P0)):
    local1 = findLocal(AllPDef[i], N0[i])
