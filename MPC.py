import maya.cmds as cmds


# put all selected objects in array of strings
sel = cmds.ls(sl=1)
print sel

# moves vertices in sel
for i in sel:
    cmds.polyMoveVertex( i, ws= 0, tx=2.0 )

# will return relative transformation to original vert pos I think
pos = cmds.getAttr('pSphere1.vtx[253]')
print pos 


# will return an array containing positions in space of all object vertices
# by Dorian Fevrier, taken from http://www.fevrierdorian.com/blog/post/2011/09/27/Quickly-retrieve-vertex-positions-of-a-Maya-mesh-(English-Translation)
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
