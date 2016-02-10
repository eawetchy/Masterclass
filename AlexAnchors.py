import maya.cmds as cmds
import functools


def main():
    UI()
    
def findPoints(_obj):
    
    #------Gets all vertex positions
    objTemp = str(cmds.ls(_obj))    #query object  
    obj = objTemp.split("'")[1]    #edit so we can use data 
    vertPosTemp = cmds.xform(obj + '.vtx[*]', q=True, ws=True, t=True)    #gets positions    
    vertList = zip(*[iter(vertPosTemp)]*3)    #makes each array element contain x, y, z
    
        
    #------Gets vertex normal value
    def getNormal(_vtx):
        vertName = _obj + '.vtx[' + str(_vtx) + ']'
        normTemp = cmds.polyNormalPerVertex(vertName, query=True, xyz=True)
        norms = zip(*[iter(normTemp)]*3)
        #values for averages
        xAve=0
        yAve=0
        zAve=0
        #get average vertex normal
        for i in range (len(norms)):
            xAve += norms[i][0]
            yAve += norms[i][1]
            zAve += norms[i][2]
        leng = len(norms) 
        xAve = xAve/leng
        yAve = yAve/leng
        zAve = zAve/leng
        aveList = [xAve, yAve, zAve]
        return aveList
    
    #------Gets all normal values
    normList = []
    for i in range (len(vertList)):
        normList.append(getNormal(i))
               
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~HEURISTIC VALUES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    """Finds bottom of head"""
    def headBot():
        yVal = vertList[0][1]
        for i in range (len(vertList)):
            if yVal > vertList[i][1] and normList[i][1] < -0.9:
                yVal = vertList[i][1]
                vtx = i
        return vtx  
        
    """Finds top of head"""
    def headTop():
        yVal = vertList[0][1]
        for i in range(len(vertList)):
            #Finds highest y value and returns vtx num
            if yVal < vertList[i][1]:
                yVal = vertList[i][1]
                vtx = i
        return vtx
    
    """Finds right ear"""
    def rightEar():
        xVal = vertList[0][0]
        for i in range(len(vertList)):
            #Finds lowest x value and returns vtx num
            if xVal > vertList[i][0]:
                xVal = vertList[i][0]
                vtx = i
        return vtx
        
    """Finds left ear"""
    def leftEar():
        xVal = vertList[0][0]
        for i in range(len(vertList)):
            #finds highest x value and returns vtx num
            if xVal < vertList[i][0]:
                xVal = vertList[i][0]
                vtx = i
        return vtx 
        
    """Finds nose tip"""
    def noseTip():
        zVal = vertList[0][2]
        #check through all entries, if central and highest z value, return it
        for i in range(len(vertList)):      
            if vertList[i][2] > zVal and -0.02 <= vertList[i][0] <= 0.02:
                zVal = vertList[i][2]
                vtx = i
        return vtx 
        
    """Finds top of nose"""
    def noseTop():
        nTip = noseTip()
        hTop = headTop()
        zVal = vertList[0][2]
        yVal = vertList[nTip][1]
        vtx = nTip      
        #finds approximate range to look for bridge
        gap = vertList[hTop][1] - vertList[nTip][1] #gap size between head and nose
        min = vertList[nTip][1]+(gap*0.15) 
        max = vertList[hTop][1]-(gap*0.55)   
        #if central in x, in the approximate y range, look for lowest z 
        for i in range(len(vertList)): 
            if -0.02 < vertList[i][0] < 0.02 and min <= vertList[i][1] <= max and 0 < vertList[i][2] < vertList[nTip][2]:
                if zVal > vertList[i][2]:
                    zVal = vertList[i][2]
                    vtx = i
        return vtx  
        
    '''Finds right lip corner''' 
    def rightLip():
        nTip = noseTip()
        hBot = headBot()
        rEar = rightEar()
        xGap = vertList[rEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.2)
        xMax = vertList[nTip][0] + (xGap * 0.5)
        yGap = vertList[nTip][1] - vertList[hBot][1]
        yMax = vertList[nTip][1] - (yGap * 0.3)
        yMin = vertList[nTip][1] - (yGap * 0.45)
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and normList[i][2] > 0.9 and xMin > vertList[i][0] > xMax: 
                vtx = i
        return vtx
        
    '''finds left lip corner'''
    def leftLip():
        nTip = noseTip()
        hBot = headBot()
        lEar = leftEar()
        xGap = vertList[lEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.2)
        xMax = vertList[nTip][0] + (xGap * 0.5)
        yGap = vertList[nTip][1] - vertList[hBot][1]
        yMax = vertList[nTip][1] - (yGap * 0.3)
        yMin = vertList[nTip][1] - (yGap * 0.45)
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and normList[i][2] > 0.9 and xMin < vertList[i][0] < xMax: 
                vtx = i   
        return vtx
    
    def leftBrowIn(): 
        nTop = noseTop()
        zVal = vertList[nTop][2]
        for i in range (len(vertList)):
            #if z value is higher than last queried and it's y is higher than nose bridge
            if vertList[i][2] > zVal and vertList[i][1] > vertList[nTop][1] and normList[i][1] < 0 and vertList[i][0] > 0 and normList[i][2] < 0.9:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def rightBrowIn(): 
        nTop = noseTop()
        zVal = vertList[nTop][2]
        for i in range (len(vertList)):
            #if z>zVal, y>nTop, yNorm faces down, is on right of face, points away from face
            if vertList[i][2] > zVal and vertList[i][1] > vertList[nTop][1] and normList[i][1] < 0 and vertList[i][0] < 0 and normList[i][2] < 0.9:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def leftBrowOut():
        nTop = noseTop()
        lEar = leftEar()
        lBrowIn = leftBrowIn()
        
        xGap = vertList[lEar][0] - vertList[nTop][0]
        xMin = vertList[nTop][0] + (xGap * 0.5)
        xMax = vertList[nTop][0] + (xGap * 0.75)
        xVal = vertList[lBrowIn][0]
        
        for i in range (len(vertList)):
            if 0.5 < normList[i][0] < 0.7 and vertList[nTop][1] < vertList[i][1] < vertList[lBrowIn][1] and xMin < vertList[i][0] < xMax and vertList[i][0] > xVal and normList[i][2] > 0:
                xVal = vertList[i][0]
                vtx = i
        return vtx
        
    def rightBrowOut():
        nTop = noseTop()
        rEar = rightEar()
        rBrowIn = rightBrowIn()
        
        xGap = vertList[rEar][0] - vertList[nTop][0]
        xMin = vertList[nTop][0] + (xGap * 0.5)
        xMax = vertList[nTop][0] + (xGap * 0.75)
        xVal = vertList[rBrowIn][0]
        
        for i in range (len(vertList)):
            if -0.5 > normList[i][0] > -0.7 and vertList[nTop][1] < vertList[i][1] < vertList[rBrowIn][1] and xMin > vertList[i][0] > xMax and vertList[i][0] < xVal and normList[i][2] > 0:
                xVal = vertList[i][0]
                vtx = i
        return vtx
    
    def topLip():
        nTip = noseTip()
        hBot = headBot()
        
        yGap = vertList[nTip][1] - vertList[hBot][1]
        yMax = vertList[nTip][1] - (yGap * 0.3)
        yMin = vertList[nTip][1] - (yGap * 0.6)
        zVal = vertList[nTip][2] * -1
        
        for i in range (len(vertList)):
            if normList[i][1] < -0.8 and -0.01 <= vertList[i][0] <= 0.01 and yMin < vertList[i][1] < yMax and zVal < vertList[i][2]:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def botLip():
        nTip = noseTip()
        hBot = headBot()
        
        yGap = vertList[nTip][1] - vertList[hBot][1]
        yMax = vertList[nTip][1] - (yGap * 0.3)
        yMin = vertList[nTip][1] - (yGap * 0.6)
        zVal = vertList[nTip][2] * -1
        
        for i in range (len(vertList)):
            if normList[i][1] > 0.75 and -0.01 <= vertList[i][0] <= 0.01 and yMin < vertList[i][1] < yMax and zVal < vertList[i][2]:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def chin():
        hBot = headBot()
        nTip = noseTip()
        
        yGap = vertList[nTip][1] - vertList[hBot][1]
        yMax = vertList[nTip][1] - (yGap * 0.6)
        yMin = vertList[nTip][1] - (yGap * 0.8)
        zVal = vertList[hBot][2]
        
        for i in range (len(vertList)):
            if vertList[i][2] > zVal and normList[i][2] > 0.9 and yMin <vertList[i][1] < yMax and -0.01 <= vertList[i][0] <= 0.01:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def forehead():
        nTop = noseTop()
         
        yNorm = 0
        for i in range (len(vertList)):
            if vertList[i][1] > vertList[nTop][1] and -0.01 <= vertList[i][0] <= 0.01 and yNorm < normList[i][1]:
                if yNorm < 0.5:
                    yNorm = normList[i][1]
                    vtx = i
        return vtx
    
    def leftCheek():
        nTip = noseTip()
        lEar = leftEar()
        hTop = headTop()
        hBot = headBot()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/20
        yMax = vertList[nTip][1] + yGap
        yMin = vertList[nTip][1] - yGap
        
        xGap = vertList[lEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.5)
        xMax = vertList[nTip][0] + (xGap * 0.6)
        zNorm = 0
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and normList[i][2] > zNorm:
                zNorm = normList[i][2]
                vtx = i
        return vtx
        
    def rightCheek():
        nTip = noseTip()
        rEar = rightEar()
        hTop = headTop()
        hBot = headBot()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/20
        yMax = vertList[nTip][1] + yGap
        yMin = vertList[nTip][1] - yGap
        
        xGap = vertList[rEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.5)
        xMax = vertList[nTip][0] + (xGap * 0.6)
        zNorm = 0
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin > vertList[i][0] > xMax and normList[i][2] > zNorm:
                zNorm = normList[i][2]
                vtx = i
        return vtx
        
    def rightNose():
        nTip = noseTip()
        rEar = rightEar()
        hTop = headTop()
        hBot = headBot()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/50
        yMax = vertList[nTip][1] + yGap
        yMin = vertList[nTip][1] - yGap
        
        xGap = vertList[rEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.15)
        xMax = vertList[nTip][0] + (xGap * 0.2)
        xVal = vertList[rEar][0]
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin > vertList[i][0] > xMax and vertList[i][0] > xVal and normList[i][0] < -0.9:
                xVal = vertList[i][0]
                vtx = i
        return vtx     
        
    def leftNose():
        nTip = noseTip()
        lEar = leftEar()
        hTop = headTop()
        hBot = headBot()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/50
        yMax = vertList[nTip][1] + yGap
        yMin = vertList[nTip][1] - yGap
        
        xGap = vertList[lEar][0] - vertList[nTip][0]
        xMin = vertList[nTip][0] + (xGap * 0.15)
        xMax = vertList[nTip][0] + (xGap * 0.2)
        xVal = vertList[lEar][0]
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and vertList[i][0] < xVal and normList[i][0] > 0.9:
                xVal = vertList[i][0]
                vtx = i
        return vtx 
        
    def leftEyeIn():
        nTop = noseTop()
        hTop = headTop()
        hBot = headBot()
        lBrowIn = leftBrowIn()
        lEar = leftEar()
        rEar = rightEar()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/10
        yMax = vertList[nTop][1]
        yMin = vertList[nTop][1] - yGap
        
        xGap = (vertList[lEar][0] - vertList[rEar][0])/40
        xMax = vertList[lBrowIn][0] + xGap
        xMin = vertList[lBrowIn][0]
        zVal = vertList[nTop][2]
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and normList[i][2] > 0.7 and zVal > vertList[i][2]:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def rightEyeIn():
        nTop = noseTop()
        hTop = headTop()
        hBot = headBot()
        rBrowIn = rightBrowIn()
        lEar = leftEar()
        rEar = rightEar()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/10
        yMax = vertList[nTop][1]
        yMin = vertList[nTop][1] - yGap
        
        xGap = (vertList[lEar][0] - vertList[rEar][0])/40
        xMax = vertList[rBrowIn][0]
        xMin = vertList[rBrowIn][0] - xGap
        zVal = vertList[nTop][2]
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and normList[i][2] > 0.7 and zVal > vertList[i][2]:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def leftEyeOut():
        nTop = noseTop()
        hTop = headTop()
        hBot = headBot()
        lBrowOut = leftBrowOut()
        lEar = leftEar()
        rEar = rightEar()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/10
        yMax = vertList[nTop][1]
        yMin = vertList[nTop][1] - yGap
        
        xGap = (vertList[lEar][0] - vertList[rEar][0])/15
        xMax = vertList[lBrowOut][0]
        xMin = vertList[lBrowOut][0] - xGap
        zVal = vertList[nTop][2]
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and zVal > vertList[i][2] and -0.3 < normList[i][0] < 0.3 and normList[i][2] > 0.2:
                zVal = vertList[i][2]
                vtx = i
        return vtx
        
    def rightEyeOut():
        nTop = noseTop()
        hTop = headTop()
        hBot = headBot()
        rBrowOut = rightBrowOut()
        lEar = leftEar()
        rEar = rightEar()
        
        yGap = (vertList[hTop][1] - vertList[hBot][1])/10
        yMax = vertList[nTop][1]
        yMin = vertList[nTop][1] - yGap
        
        xGap = (vertList[lEar][0] - vertList[rEar][0])/15
        xMax = vertList[rBrowOut][0] + xGap
        xMin = vertList[rBrowOut][0] 
        zVal = vertList[nTop][2]
        
        for i in range (len(vertList)):
            if yMin < vertList[i][1] < yMax and xMin < vertList[i][0] < xMax and zVal > vertList[i][2] and -0.3 < normList[i][0] < 0.3 and normList[i][2] > 0.2:
                zVal = vertList[i][2]
                vtx = i
        return vtx  
        
                    
    #Generates list of points   
    anchorList = [headTop(),headBot(), noseTip(),noseTop(), leftEar(),rightEar(), leftLip(),rightLip(),topLip(),botLip(), \
                 leftBrowIn(),rightBrowIn(),leftBrowOut(),rightBrowOut(), chin(),forehead(),leftCheek(),rightCheek(), \
                 leftNose(),rightNose(),leftEyeIn(),rightEyeIn(),leftEyeOut(),rightEyeOut()]
    print anchorList
    return anchorList
