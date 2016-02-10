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

cmds.select("blendshape1")
blendshape = cmds.ls(sl=1)
cmds.move(0,0,0, blendshape[0])
cmds.select(clear=True)
cmds.select("blendshape1.vtx[0:381]")
AllPBlend = cmds.ls(sl=1, fl=True)
	
#vertex list transformTarget
O = getVtxPos( sourceName[0] )

#vertex list transformSource
B = getVtxPos( blendshape[0] )


MV = numpy.matrix(B)-numpy.matrix(O) 

#-----ROTATION-----#

N0 = normalMatrix(AllP0) # normal matrix for source

N1 = normalMatrix(AllPDef) # normal matrix for deformed source

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

def findRotationMatrix(localOrig, localBlend):
    
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
    

MVdef = numpy.matrix((len(P0), 3)) # deformed motion vectors
MVdef[0] = R*MV
