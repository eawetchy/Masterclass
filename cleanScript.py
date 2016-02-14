import maya.cmds as cmds
import numpy
import re
import functools as ft
import copy

def RBFbasis (r,s):
    R = (r**2 + 1)**0.5
    #R = (numpy.exp(-r**2))
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
	
def getVertexNormal(P):
    cmds.select(P)
    n = cmds.polyNormalPerVertex( query=True, xyz=True )
    num = len(n)/3
    x = 0
    y = 0
    z = 0
    for j in range (0,num):
        x += n[0+3*j]
        y += n[1+3*j]
        z += n[2+3*j]
        vn = numpy.array([[x/num, y/num, z/num]])
        length = numpy.linalg.norm(vn)
        vn = vn/length
    return vn
	
# will return a matrix of vertex normals, calculated by averaging the surrounding face normals
def normalMatrix(P):
    N = numpy.zeros((len(P),3)) # normal matrix for source
    for i in range(0, len(P)):
        vn = getVertexNormal(P[i])
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
    vList.remove(point)
    # find end point of the edge 
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
            owR[i][j] = numpy.dot(world[j], numpy.transpose(localOrig[i]))

    wdR = numpy.zeros((3,3)) # rotation from world axes to the local deformed vertex axes vertex axes
    for i in range(0,2):
        for j in range(0,2):
            wdR[i][j] = numpy.dot(localDef[j], numpy.transpose(world[i]))
        
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
	
def pointPositions(AllP):
    P0 = []
    for j in AllP:
        P0.append( cmds.pointPosition(j, w=True) )
    P0 = numpy.matrix(P0)    
    return P0
	
def matchTarget(source, target, SelP0, SelP1):
	cmds.move(0,0,0,source)
	cmds.move(0,0,0,target)
	cmds.select(clear=True)
	cmds.select(source+".vtx[*]")
	AllP0 = cmds.ls(sl=1, fl=True)
	cmds.select(clear=True)
	cmds.select(target+".vtx[*]")
	AllP1 = cmds.ls(sl=1, fl=True)
	#----------------#

	KP0 = pointPositions(SelP0)
	KP1 = pointPositions(SelP1)
	if (len(KP0) != len(KP1)):
	    print "Number of source and target key points does not match!"
	    quit()
	P0 = pointPositions(AllP0)
	P1 = pointPositions(AllP1)
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
	cmds.duplicate(source, n = "sourceDeformed")
	cmds.move(0,0,0, "sourceDeformed")
	cmds.select(clear=True)
	cmds.select("sourceDeformed.vtx[*]")
	AllPDef = cmds.ls(sl=1, fl=True)


	ind = 0
	for i in range(0,n):
		cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllPDef[i])
	
def createBlendshape(source, blendshape, AllP0, AllPDef):
	#------------MOTION VECTOR TRANSFER-------------#
	print "Good Evening, Madam"
	blendName = "target" + blendshape
	print "blendName = ", blendName
	# create array of all vertices of the blendshape
	#cmds.select(blendshape)
	#blendshape = cmds.ls(sl=1)
	print blendshape
	cmds.move(0,0,0, blendshape)
	cmds.select(clear=True)
	cmds.select(blendshape+".vtx[*]")
	AllPBlend = cmds.ls(sl=1, fl=True)

	#vertex list original source mesh
	O = getVtxPos( source )

	#vertex list source mesh blendshape
	B = getVtxPos( blendshape )

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
	    cmds.move(float(MV[i, 0]), float(MV[i, 1]), float(MV[i, 2]), defBlend[i], r=True)
	    #MVdef = R[i]*numpy.transpose(MV[i])
	    #cmds.move(float(MVdef[0]), float(MVdef[1]), float(MVdef[2]), defBlend[i], r=True)
	    #MVdef = S[i]*R[i]*numpy.transpose(MV[i])
		#cmds.move(float(MVdef[0]), float(MVdef[1]), float(MVdef[2]), defBlend[i], r=True)
    
def useSelection(_field, *args):
    txt = cmds.ls(sl=True)
    cmds.textField( _field, edit=True, text=txt[0])  
        
def selectBlendshapes(_field, *args):
    txt = cmds.ls(sl=True)
    cmds.textField(_field, edit=True, text = "Blendshapes set")
    global BS 
    BS = txt       
    
def useSelectedPoints(_field, source, *args):
    # bool source
    txt = cmds.ls(fl=True, os=True)
    cmds.textField( _field, edit=True, text="Set "+str(len(txt))+" key points")
    if (source == True):
        global SelP0 
        SelP0 = copy.deepcopy(txt)
    else:
        global SelP1 
        SelP1 = copy.deepcopy(txt)

def retrieveText(_field, *_args):
    val = cmds.textField(_field, q=True, text=True)
    return val
    
def matchTarg(sourceName, targetName, *args):
    source = retrieveText(sourceName)
    target = retrieveText(targetName)
    matchTarget(source, target, SelP0, SelP1)
    
def blendShapes(blendshapes, *args):
    shapes = str(retrieveText(blendshapes))
    print "shapes: ", shapes
    for i in BS:
        print i
        createBlendshape(sourceName[0], i, AllP0, AllPDef)

def makeGUI():
    winID = 'Expression Cloning'
    if cmds.window(winID, exists = True):
        cmds.deleteUI(winID)
    cmds.window(winID)
    cmds.columnLayout(columnWidth = 450)
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 150))
    cmds.text(label='Source Mesh:')
    sourceName = cmds.textField(w = 200)
    cmds.button(label = 'Set Selected as Source', c = ft.partial(useSelection, sourceName), w=150)
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3 = (100,200,150))
    #target model
    cmds.text(label='Source Key Points:')
    SKP = cmds.textField(w = 200)
    cmds.button(label = 'Set Selected Points', c = ft.partial(useSelectedPoints, SKP, True), w = 150) 
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 150))
    #target model
    cmds.text(label='Target Mesh:')
    targetName = cmds.textField(w = 200)
    cmds.button(label = 'Set Selected as Target', c = ft.partial(useSelection, targetName), w = 150) 
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3 = (100, 200, 150))
    cmds.text(label='Target Key Points')
    TKP = cmds.textField(w = 200)
    cmds.button(label = 'Set Selected Points', c = ft.partial(useSelectedPoints, TKP, False), w = 150)
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(100, 200, 150))
    cmds.text(label='Blendshapes')
    blendshapes = cmds.textField(w = 200)
    cmds.button(label = 'Set Blendshapes', c = ft.partial(selectBlendshapes, blendshapes), w = 150)
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=1, columnWidth1=550)
    #, c = matchTarget(sourceName, targetName, SelP0, SelP1)) 
    cmds.button(label = 'Deform Source Model' , c=ft.partial(matchTarg, sourceName, targetName), w = 450)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=1, columnWidth1=550)
    cmds.button(label = 'Create Blendshapes ', c=ft.partial(blendShapes, blendshapes), w = 450)
    cmds.setParent('..')
    
    cmds.showWindow()

def main():
    SelP0 = []
    SelP1 = []
    BS = []
    makeGUI()
    
main()
