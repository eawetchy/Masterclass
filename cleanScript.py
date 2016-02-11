import maya.cmds as cmds
import numpy
import re

def RBFbasis (r,s):
    R = (r**2 + 1)**0.5
    return R 
    
def rbfeval(C, W, P):
    P2 = numpy.copy(P)
    h = numpy.asmatrix(numpy.zeros((len(W),1)))
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(numpy.linalg.norm(P[i] - C[j]), 1)
    #reconstruct point i
        P2[i] = (W.transpose() * h).transpose()
    return P2

# will return an array containing positions in space of all object vertices
def getVtxPos( shapeNode ) :
 
	vtxWorldPosition = []    
	
	vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
 
	for i in vtxIndexList :
		curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
		vtxWorldPosition.append( curPointPosition )
 
	return vtxWorldPosition
	
# will return a matrix of vertex normals, calculated by averaging the surrounding face normals
def normalMatrix(P):
    N = numpy.zeros((len(P),3)) # normal matrix for source
    for i in range(0, len(P)):
        cmds.select(P[i])
        n = cmds.polyNormalPerVertex( query=True, xyz=True )
        num = len(n)/3
        x = 0
        y = 0
        z = 0
        for j in range(0, num):
            x += n[0+3*j]
            y += n[1+3*j]
            z += n[2+3*j]
            vn = numpy.matrix([[x/num, y/num, z/num]])
            length = numpy.linalg.norm(vn)
            vn = vn/length
        N[i] = vn
    return N
    
def findLocal(point, normal):
    # local X-axis of the vertex's coordinate system is given by average of the surface normals of all the polygons sharing a vertex
    # To find Y-axis project any edge connected to the vertex onto the tangent plane whose normal is the just-determined X-axis
    
    # find tangent plane of the normal
    edges = cmds.polyListComponentConversion( point, fv=True, te=True ) # Will return the edges in numeric order:
    edges = cmds.ls( edges, flatten=True )
    vList = cmds.polyListComponentConversion( edges, fe=True, tv=True )
    vList = cmds.ls( vList, flatten=True )
    
    # find end point of the edge 
    if (point == vList[0]):
        q = cmds.pointPosition(vList[1], w=True)
    else:
        q = cmds.pointPosition(vList[0], w=True)

    # projected onto a plane given by the vertex we're examining and the determined vertex normal 
    p = cmds.pointPosition(point) # plane point 
    n = normal # plane normal, normalised
    
    q = numpy.asarray(q)
    p = numpy.asarray(p)
    n = numpy.asarray(n)
    # end point of the edge projected onto tangent plane of the normal
    q_proj = q - numpy.dot((q - p), numpy.transpose(n)) * n
    # Y-axis of the vertex's local coordinate system

    lX = normal
    lY = q_proj - p
    lenY = numpy.linalg.norm(lY)
    lY = lY/lenY
    lZ = numpy.cross(lX, lY)
    lenZ = numpy.linalg.norm(lZ)
    lZ = lZ/lenZ
    local = numpy.matrix([lX, lY, lZ])   
    return local

def findRotationMatrix(localOrig, localDef):
    
    world = numpy.matrix([ [ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ])
    
    owR = numpy.zeros((3,3)) # rotation from a local source vertex coordinate axes to the world coordinate axes
    for i in range(0,2):
        for j in range(0,2):
            owR[i][j] = numpy.dot(world[i], numpy.transpose(localOrig[j]))

    wdR = numpy.zeros((3,3)) # rotation from world axes to the local deformed vertex axes vertex axes
    for i in range(0,2):
        for j in range(0,2):
            wdR[i][j] = numpy.dot(localDef[i], numpy.transpose(world[j]))
        
    odR = wdR * owR 
    return odR
    
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
    return extremeValue
    
def findScaleMatrix(point, allPoints, allPointPos, rotationMat):
		# find faces sharing a vertex
	faces = cmds.polyListComponentConversion( point, fv=True, tf=True )
	faces = cmds.ls( faces, flatten=True )
	vList = cmds.polyListComponentConversion( faces, ff=True, tv=True )
	vList = cmds.ls( vList, flatten=True )
	vertPos = []
	for i in range(0, len(vList)):
		vertPos.append(cmds.pointPosition(vList[i], w=True))

	#find bounding box of vertices
	BB = []
	BB.append(getExtremePoint("x", False, vertPos))
	BB.append(getExtremePoint("x", True, vertPos))
	BB.append(getExtremePoint("y", False, vertPos))
	BB.append(getExtremePoint("y", True, vertPos))
	BB.append(getExtremePoint("z", False, vertPos))
	BB.append(getExtremePoint("z", True, vertPos))
	sizeBB = numpy.array([BB[1] - BB[0], BB[3] - BB[2], BB[5] - BB[4]])

	vInd = []
	# extracting the vertex indices in vList adjusted from http://stackoverflow.com/questions/10365225/extract-digits-in-a-simple-way-from-a-python-string
	# answer by user senderle
	for i in vList:
		temp = re.findall('\d+', i)
		vInd.append(int(temp[len(temp)-1]))	
	
	vertPos2 = []
	for i in vInd:
		vertPos2.append(numpy.asarray(rotationMat[i] * numpy.transpose(allPointPos[i])))
	#find bounding box of deformed vertices
	BB2 = []
	BB2.append(float(getExtremePoint("x", False, vertPos2)))
	BB2.append(float(getExtremePoint("x", True, vertPos2)))
	BB2.append(float(getExtremePoint("y", False, vertPos2)))
	BB2.append(float(getExtremePoint("y", True, vertPos2)))
	BB2.append(float(getExtremePoint("z", False, vertPos2)))
	BB2.append(float(getExtremePoint("z", True, vertPos2)))
	sizeBB2 = numpy.array([BB2[1] - BB2[0], BB2[3] - BB2[2], BB2[5] - BB2[4]])

	s = sizeBB2/sizeBB
	S = numpy.matrix([[s[0],0,0],[0,s[1],0],[0,0,s[2]]])
	
	return S
	
def createBlendshape(source, blendshape, AllP0, AllPDef, blendName):
	#------------MOTION VECTOR TRANSFER-------------#

	# create array of all vertices of the blendshape
	cmds.select(blendshape)
	blendshape = cmds.ls(sl=1)
	cmds.move(0,0,0, blendshape[0])
	cmds.select(clear=True)
	cmds.select(blendshape[0]+".vtx[*]")
	AllPBlend = cmds.ls(sl=1, fl=True)

	#vertex list original source mesh
	O = getVtxPos( source )

	#vertex list source mesh blendshape
	B = getVtxPos( blendshape[0] )

	# matrix of motion vectors from source to blendshape vertex positions
	MV = numpy.matrix(B)-numpy.matrix(O) 
	MV = numpy.asmatrix(MV)
    
	#-------------------------ROTATION-----------------------------#

	N0 = normalMatrix(AllP0) # normal matrix for source

	N1 = normalMatrix(AllPDef) # normal matrix for deformed source
	#------------

	# list of motion vector rotations
	R = []
	# find local source vertex coordinate systems before deformation, then after deformation
	for i in range(0, len(P0)):
		localOrig = findLocal(AllP0[i], N0[i])
		localDef = findLocal(AllPDef[i], N1[i])
		ODR = findRotationMatrix(localOrig, localDef)
		R.append(ODR)
	R = numpy.asarray(R)
		
	#--------------------------MAGNITUDE---------------------------#
		
	S = []
	for i in AllP0:	
		S.append(findScaleMatrix(i, AllP0, P0, R))
	S = numpy.asarray(S)

	#--------OVERALL MOTION VECTOR ROTATION AND MAGNITUDE ADJUSTMENT--------#

	# duplicate deformed source to make blendshape
	cmds.duplicate("sourceDeformed", n = blendName)
	cmds.select(clear=True)
	cmds.select(blendName+".vtx[*]")
	defBlend = cmds.ls(sl=1, fl=True)

	for i in range(0,n):
		MVdef = S[i]*R[i]*numpy.transpose(MV[i])
		cmds.move(float(MVdef[0]), float(MVdef[1]), float(MVdef[2]), defBlend[i], r=True)
		
		
#------------------------------------------------------------------------------#

cmds.select("source1")
sourceName = cmds.ls(sl=1)
cmds.move(0,0,0,sourceName[0])
cmds.select("target")
targetName = cmds.ls(sl=1)
cmds.move(0,0,0,targetName[0])


# turn on "Track selection order" in preferences > selection!
cmds.select(clear=True)
SKP = [194, 254, 381, 380, 189, 199, 184]
# key points on bruce
#SKP = [814, 820, 827, 7265, 6415, 2361, 2401, 8133, 5703, 7644, 3592, 2206, 4084, 5181, 1126, 785, 4212, 5612, 6769, 2715, 7841, 5740, 1686, 3787, 6905, 2672, 1969, 861, 6010, 1, 4770, 437, 498, 19]
for i in SKP:
    cmds.select(sourceName[0]+".vtx["+str(i)+"]", add = True)
SelP0 = cmds.ls(fl=True, os=True)
cmds.select(clear=True)
TKP = [2986, 3626, 381, 380, 2949, 3347, 2911]
# key points on emily
#TKP = [11641, 10918, 2181, 20478, 20262, 18333, 18565, 21213, 22000, 200141, 2747, 19498, 5734, 11213, 8902, 11923, 1594, 15871, 23267, 4267, 15309, 14273, 5206, 11733, 22078, 13006, 14203, 16302, 22980, 6646, 17078, 14545, 14567, 8184]
for i in TKP:
    cmds.select(targetName[0]+".vtx["+str(i)+"]", add = True)
SelP1 = cmds.ls(fl=True, os=True)
if (len(SKP) != len(TKP)):
    print "Number of source and target key points don't match!"
    quit()

cmds.select(clear=True)
cmds.select(sourceName[0]+".vtx[*]")
AllP0 = cmds.ls(sl=1, fl=True)
cmds.select(clear=True)
cmds.select(targetName[0]+".vtx[*]")
AllP1 = cmds.ls(sl=1, fl=True)


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

# duplicate source, then apply the transformation
cmds.duplicate(sourceName[0], n = "sourceDeformed")
cmds.select(clear=True)
cmds.select("sourceDeformed.vtx[*]")
AllPDef = cmds.ls(sl=1, fl=True)


ind = 0
for i in range(0,n):
    cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllPDef[i])

    
blendshapes = ["Blendshape1", "Blendshape2"]
for i in blendshapes:
    createBlendshape(sourceName[0], i, AllP0, AllPDef, "target"+i)
