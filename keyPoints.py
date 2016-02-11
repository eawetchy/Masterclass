#cmds.polyReduce(ver = 1, p = 70)
#cmds.polyReduce(ver = 1, p = 50)

def getExtremePoint( dir, high, vertexList, vertInds):
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
    return vertInds[vertIdx], extremeValue, vertIdx
    
cmds.select("neutral")
sourceName = cmds.ls(sl=1)
cmds.move(0,0,0,sourceName[0])
cmds.select(clear=True)
cmds.select(sourceName[0]+".vtx[*]")
AllP0 = cmds.ls(sl=1, fl=True)
P0 = []
for i in AllP0:
    P0.append( cmds.pointPosition(i, w=True) )

cmds.select("target")
targetName = cmds.ls(sl=1)
cmds.move(0,0,0,targetName[0])
cmds.select(clear=True)
cmds.select(targetName[0]+".vtx[*]")
AllP1 = cmds.ls(sl=1, fl=True)
P1 = []
for i in AllP1:
    P1.append( cmds.pointPosition(i, w=True) )

noseTip = getExtremePoint("z", True, P1)
cmds.select("target.vtx[" + str(noseTip[0])+"]")

nose = cmds.ls(sl=1, fl = 1)
cmds.select(nose)
noseVts = []
for i in nose:
    noseVts.append( cmds.pointPosition(i, w=True) )
    
noseTip = getExtremePoint("z", True, noseVts, nose)
top = getExtremePoint("y", True, noseVts, nose)
cmds.select(noseTip[0], top[0])
cmds.select(nose)

def findLeftNose():
    noseTip = getExtremePoint("z", True, noseVts, nose)
    left = getExtremePoint("x", False, noseVts, nose)
    right = getExtremePoint("x", True, noseVts, nose)
    
