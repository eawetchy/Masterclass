cmds.polyReduce(ver = 1, p = 70)
cmds.polyReduce(ver = 1, p = 50)

# returns vertex index within the model, vertex position in the queried axis and index within the subset of points
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
            vn = numpy.array([[x/num, y/num, z/num]])
            length = numpy.linalg.norm(vn)
            vn = vn/length
        N[i] = vn
    return N
    
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

nose = cmds.ls(sl=1, fl = 1)
cmds.select(nose)
noseVts = []
import re
noseInd = []
for i in nose:
    obj = i.split("'")[0]
    temp = re.findall('\d+', obj)
    noseInd.append(int(temp[len(temp)-1]))

		
for i in nose:
    noseVts.append( cmds.pointPosition(i, w=True) )
    noseVts[i].append


    
noseTip = getExtremePoint("z", True, noseVts, nose)
top = getExtremePoint("y", True, noseVts, nose)
cmds.select(noseTip[0], top[0])
cmds.select(nose)
cmds.select(bottom[0])

def findLeftNose():
    noseTip = getExtremePoint("z", True, noseVts, nose)
    left = getExtremePoint("x", False, noseVts, nose) #leftmost selected vertex
    right = getExtremePoint("x", True, noseVts, nose) #rightmost selected vertex
    bottom = getExtremePoint("y", False, noseVts, nose) # lowest selected vertex
    cmds.select(left[0], right[0],bottom[0], noseTip[0])
    poss = []
from operator import itemgetter
for i in range(0, len(nose)):
    if (bottom[1] < noseVts[i][1] and noseVts[i][1] < noseVts[noseTip[2]][1]+(noseVts[noseTip[2]][1]-bottom[1])):
        if (left[1] < noseVts[i][0] and noseVts[i][0] < noseVts[noseTip[2]][0]):
            poss.append(nose[i]) 
    normals = (normalMatrix(nose))
    normals = normals.tolist()
    # highest vertex with biggest angle between normals
    posSort = sorted(noseVts, key=lambda y: y[1], reverse=True)
    
    
    cmds.select(poss)
            
            
            
        bottom[1] < leftNoseY < noseVts[noseTip[2]][1]+(noseVts[noseTip[2]][1]-bottom[1])
        left[1] < leftNoseX < noseVts[noseTip[2]][0]
    
    
    
    



cmds.inViewMessage( amg='In-view message <hl>test</hl>.', pos='midCenter', fade=True )
