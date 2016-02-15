import maya.cmds as cmds
import numpy
import re
import functools as ft
import copy

def RBFbasis (r):
    '''
    Evaluates radial basis function for radius between two points
    Using Hardy multi-quadrics as suggested by Noh and Neumann
    (Noh, J. and Neumann, U., 2001. Expression Cloning. In: SIGGRAPH '01. New York: ACM, pp.277-288.)
    
    Returns the value of the function as a float
    
    r: distance between two points Xi and Xj, with Xj typically being a key point on the mesh
    '''
    R = (r**2 + 1)**0.5
    return R 
    
def rbfeval(C, W, P):
    '''
    Evaluates the RBF for all points on the source mesh after the system has been solved for the weights
    
    Returns a matrix of size(numPoints, 3) containing the deformed x, y  and z-positions of the source mesh vertices
    
    C: key points on the source mesh
    W: weight vector
    P: all vertices on the source mesh
    '''
    P2 = numpy.copy(P)
    h = numpy.asmatrix(numpy.zeros((len(W),1)))
    for i in range(0, len(P)):
        for j in range(0, len(C)):
            h[j] = RBFbasis(numpy.linalg.norm(P[i] - C[j]))
    #reconstruct point i
        P2[i] = (W.transpose() * h).transpose()
    return P2

# will return an array containing positions in space of all object vertices
def getVtxPos( shapeNode ) :
    '''
    Takes an object in Maya and finds the positions in world space of its vertices
    
    Returns an array of the vertices' world space position
    '''
    vtxWorldPosition = []    
    vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )

    for i in vtxIndexList :
        curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
        vtxWorldPosition.append( curPointPosition )
 
    return vtxWorldPosition
    
def getVertexNormal(P):
    '''
    For a given vertex of a polygon mesh, queries the normal for each vertex-face combination and calculates the average vertex normal.
    
    P: input vertex
    '''
    cmds.select(P)
    # query x,y and z-values of the normals of all faces around the vertex
    n = cmds.polyNormalPerVertex( query=True, xyz=True )
    num = len(n)/3
    x = 0
    y = 0
    z = 0
    # calculate average 
    for j in range (0,num):
        x += n[0+3*j]
        y += n[1+3*j]
        z += n[2+3*j]
        vn = numpy.array([[x/num, y/num, z/num]])
        # normalize
        length = numpy.linalg.norm(vn)
        vn = vn/length
    return vn
    
# will return a matrix of vertex normals, calculated by averaging the surrounding face normals
def normalMatrix(P):
    '''
    Finds the average vertex normal for each point in an array of points
    Returns a matrix of size (numPoints, 3) containing one normal for each input point
    
    P: input array of points
    '''
    N = numpy.zeros((len(P),3)) # normal matrix for source
    for i in range(0, len(P)):
        vn = getVertexNormal(P[i])
        N[i] = vn
    return N
    
def findLocal(point, normal):
    '''
    Finds a local coordinate system for a vertex.
    X-axis is the average vertex normal
    Y-axis is the projection of any edge connected to the vertex onto the plane whose normal is the X-axis
    Z-axis is the cross product of the X- and Y-axes
    Returns a 3x3 matrix whose elements are the axes of the local coordinate system.
    '''
    # local X-axis of the vertex's coordinate system is given by average of the surface normals of all the polygons sharing a vertex
    # To find Y-axis project any edge connected to the vertex onto the tangent plane whose normal is the just-determined X-axis
    
    # find tangent plane of the normal
    edges = cmds.polyListComponentConversion( point, fv=True, te=True ) # Will return the edges in numeric order
    edges = cmds.ls( edges, flatten=True )
    # convert edges into vertices and remove our original point to make sure it won't be used
    vList = cmds.polyListComponentConversion( edges, fe=True, tv=True )
    vList = cmds.ls( vList, flatten=True )
    vList.remove(point)
    # find end point of any connected edge 
    q = cmds.pointPosition(vList[0], w=True)

    # projected onto a plane given by the vertex we're examining and the determined vertex normal 
    p = cmds.pointPosition(point) # plane point 
    n = normal # plane normal, normalised
    
    q = numpy.asarray(q)
    p = numpy.asarray(p)
    n = numpy.asarray(n)
    # end point of the edge projected onto tangent plane of the normal
    q_proj = q - numpy.dot((q - p), numpy.transpose(n)) * n

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
    '''
    Finds the rotation matrix to transform the local coordinate system of a vertex on the source mesh to the one of a vertex on the deformed source.
    This is used to rotate the motion vectors of each point to account for changes in the local surface when the source model is deformed.
    Returns a 3x3 matrix that describes the rotation from source to target vertex
    '''
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
    '''
    Finds the highest or lowest x-, y- or z-value in a list of vertex positions 
    Returns that value
    
    dir: the axis to be examined
    high: If True, function finds the highest value. If false, finds the lowest value
    vertexList: array of vertex positions
    '''
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
    '''
    Finds the change in local scale at a vertex by comparing the bounding boxes around the polygons sharing a vertex before and after transformation.
    This is used to scale the motion vectors for each vertex to account for differences in proportion between the source and target models
    Returns a 3x3 scale matrix
    
    point: Point to be examined
    allPoints: list of Maya vertex indices, e.g. 'sourceModel.vtx[0]
    allPointPos: list of positions of these vertices in world space 
    rotationMat: rotation matrix describing transformation from source to deformed source vertex. 
        Necessary to undo the rotation before bounding box calculation to ensure a correct ration
    '''
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
    '''
    Takes an array of Maya vertices and queries their position in world space
    Returns a matrix of size(numPoints, 3) containing these position
    
    AllP: Array of vertex indices 
    '''
    P0 = []
    for j in AllP:
        P0.append( cmds.pointPosition(j, w=True) )
    P0 = numpy.matrix(P0)    
    return P0
    
def matchTarget(source, target, SelP0, SelP1):
    '''
    Performs the surface match between source and target models. Results in a duplicated, deformed version of the source mesh
    
    source: Name of the source mesh
    target: Name of the target mesh. Both meshes should have their centres at the origin
    SelP0: Selected key points on the source mesh
    SelP1: Selected key points on the target mesh. Must be the same number and in the same order as SelP0 or the mapping will go horribly wrong
    '''
    cmds.move(0,0,0,source)
    cmds.move(0,0,0,target)
    cmds.select(clear=True)
    # get indices of all vertices in source and target meshes
    cmds.select(source+".vtx[*]")
    global AllP0
    AllP0 = cmds.ls(sl=1, fl=True)
    cmds.select(clear=True)
    cmds.select(target+".vtx[*]")
    AllP1 = cmds.ls(sl=1, fl=True)
    #----------------#
    # get positions in space of key points and all points on source and target meshes
    KP0 = pointPositions(SelP0)
    KP1 = pointPositions(SelP1)
    if (len(KP0) != len(KP1)):
        print "Number of source and target key points does not match!"
        quit()
    P0 = pointPositions(AllP0)
    P1 = pointPositions(AllP1)
    #------------
      
    # number of points on source mesh
    n = len(P0)
    # number of key points
    m = len(KP1)
    # build radial basis function matrix
    H = numpy.zeros((m,m))
    for i in range(0, m):
        for j in range(0, m):
            H[i,j]=RBFbasis( numpy.linalg.norm(KP0[i] - KP0[j])) # closestPoint( KP0[j], KP0 ) )

    H = numpy.asmatrix(H)
    # solve for weights
    w = numpy.linalg.solve(H, KP1)
    
    # evaluate new positions for source vertices
    P02  = rbfeval(KP0, w, P0)

    # duplicate source, then apply the transformation
    cmds.duplicate(source, n = "sourceDeformed")
    cmds.move(0,0,0, "sourceDeformed")
    cmds.select(clear=True)
    cmds.select("sourceDeformed.vtx[*]")
    global AllPDef
    AllPDef = cmds.ls(sl=1, fl=True)
    ind = 0
    for i in range(0,n):
        cmds.move(float(P02[i][ind]), float(P02[i][ind+1]), float(P02[i][ind+2]), AllPDef[i])
    
def createBlendshape(source, blendshape, AllP0, AllPDef):
    #------------MOTION VECTOR TRANSFER-------------#
    # create array of all vertices of the blendshape
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
    
    '''
    # rotating and scaling of motion vectors using these functions gives wrong results
    # and is not deforming the motion vectors like it should.
    # I have not been able to debug this in the given time and have therefore taken these parts out for the moment.
    # Simply using the motion vectors on the deformed source mesh results in acceptable blend shapes
    
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
    '''
    # duplicate deformed source to make blendshape
    blendName = "target" + blendshape
    cmds.duplicate("sourceDeformed", n = blendName)
    cmds.select(clear=True)
    cmds.select(blendName+".vtx[*]")
    defBlend = cmds.ls(sl=1, fl=True)


    for i in range(0,len(AllP0)):
        cmds.move(float(MV[i, 0]), float(MV[i, 1]), float(MV[i, 2]), defBlend[i], r=True)
        '''
        MVdef = S[i]*R[i]*numpy.transpose(MV[i])
        cmds.move(float(MVdef[0]), float(MVdef[1]), float(MVdef[2]), defBlend[i], r=True)
        '''
    
def useSelection(_field, *args):
    '''
    Puts name of the currently selected object into a text field on the GUI
    _field: Text field
    '''
    txt = cmds.ls(sl=True)
    cmds.textField( _field, edit=True, text=txt[0])  
        
def selectBlendshapes(_field, *args):
    '''
    Stores the selected meshes in a global list of blend shapes and confirms this in the text field
    _field: Text field
    '''
    txt = cmds.ls(sl=True)
    cmds.textField(_field, edit=True, text = "Blendshapes set")
    global BS 
    BS = txt       
    
def useSelectedPoints(_field, source, *args):
    '''
    Stores the selected points as the source or target key points
    _field: Text field
    source: Boolean, if true sets points as source key points, if false as target key points
    '''
    txt = cmds.ls(fl=True, os=True)
    cmds.textField( _field, edit=True, text="Set "+str(len(txt))+" key points")
    if (source == True):
        global SelP0 
        SelP0 = copy.deepcopy(txt)
    else:
        global SelP1 
        SelP1 = copy.deepcopy(txt)

def retrieveText(_field, *_args):
    '''
    Retrieves text from a given text field
    _field: Text field
    '''
    val = cmds.textField(_field, q=True, text=True)
    return val
    
def matchTarg(sourceName, targetName, *args):
    '''
    Calls the procedure to map the source onto the target mesh
    '''
    source = retrieveText(sourceName)
    target = retrieveText(targetName)
    matchTarget(source, target, SelP0, SelP1)
    
def blendShapes(sourceName, blendshapes, *args):
    shapes = str(retrieveText(blendshapes))
    source = retrieveText(sourceName)
    for i in BS:
        createBlendshape(source, i, AllP0, AllPDef)

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
    cmds.button(label = 'Create Blendshapes ', c=ft.partial(blendShapes, sourceName, blendshapes), w = 450)
    cmds.setParent('..')
    
    cmds.showWindow()

def main():
    # declare some global variables
    SelP0 = []
    SelP1 = []
    BS = []
    AllP0 = []
    AllPDef = []
    makeGUI()
    
main()
