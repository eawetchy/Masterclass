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
		
for i in range(0,len(nose)):
    noseVts.append( cmds.pointPosition(nose[i], w=True) )
    noseVts[i].append(i)
    noseVts[i].append(noseInd[i])
    
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

for i in range(0, len(nose)):
    if (bottom[1] < noseVts[i][1] and noseVts[i][1] < noseVts[noseTip[2]][1]+(noseVts[noseTip[2]][1]-bottom[1])):
        if (left[1] < noseVts[i][0] and noseVts[i][0] < noseVts[noseTip[2]][0]):
            poss.append(nose[i])
    
    normals = (normalMatrix(nose))
    normals = normals.tolist()
    # highest vertex with biggest angle between normals
    posSort = sorted(poss, key=lambda y: y[1], reverse=True)
    cmds.select(nose[posSort[0][3]])
    
    cmds.select(poss)

 #       bottom[1] < leftNoseY < noseVts[noseTip[2]][1]+(noseVts[noseTip[2]][1]-bottom[1])
#        left[1] < leftNoseX < noseVts[noseTip[2]][0]
    
cmds.inViewMessage( amg='In-view message <hl>test</hl>.', pos='midCenter', fade=True )

Spheres: SKP = [194, 254, 381, 380, 189, 199, 184]
TKP = [2986, 3626, 381, 380, 2949, 3347, 2911]


SP0 = [u'BruceLeeHead:head.vtx[814]', u'BruceLeeHead:head.vtx[819]', u'BruceLeeHead:head.vtx[826]', u'BruceLeeHead:head.vtx[5299]', \
u'BruceLeeHead:head.vtx[1245]', u'BruceLeeHead:head.vtx[808]', u'BruceLeeHead:head.vtx[5276]', u'BruceLeeHead:head.vtx[1222]', \
u'BruceLeeHead:head.vtx[7264]', u'BruceLeeHead:head.vtx[7315]', u'BruceLeeHead:head.vtx[6440]', u'BruceLeeHead:head.vtx[6467]', \
u'BruceLeeHead:head.vtx[2361]', u'BruceLeeHead:head.vtx[3261]', u'BruceLeeHead:head.vtx[3262]', u'BruceLeeHead:head.vtx[2413]', \
u'BruceLeeHead:head.vtx[8136]', u'BruceLeeHead:head.vtx[7925]', u'BruceLeeHead:head.vtx[7661]', u'BruceLeeHead:head.vtx[3592]', \
u'BruceLeeHead:head.vtx[3872]', u'BruceLeeHead:head.vtx[4088]', u'BruceLeeHead:head.vtx[5183]', u'BruceLeeHead:head.vtx[771]', \
u'BruceLeeHead:head.vtx[3164]', u'BruceLeeHead:head.vtx[7841]', u'BruceLeeHead:head.vtx[3786]', u'BruceLeeHead:head.vtx[5740]', \
u'BruceLeeHead:head.vtx[1686]', u'BruceLeeHead:head.vtx[6769]', u'BruceLeeHead:head.vtx[6925]', u'BruceLeeHead:head.vtx[6324]', \
u'BruceLeeHead:head.vtx[6752]', u'BruceLeeHead:head.vtx[2715]', u'BruceLeeHead:head.vtx[2872]', u'BruceLeeHead:head.vtx[2799]', \
u'BruceLeeHead:head.vtx[2699]', u'BruceLeeHead:head.vtx[835]', u'BruceLeeHead:head.vtx[7626]', u'BruceLeeHead:head.vtx[3572]', \
u'BruceLeeHead:head.vtx[847]', u'BruceLeeHead:head.vtx[6078]', u'BruceLeeHead:head.vtx[1445]', u'BruceLeeHead:head.vtx[859]', \
u'BruceLeeHead:head.vtx[1471]', u'BruceLeeHead:head.vtx[5526]', u'BruceLeeHead:head.vtx[0]', u'BruceLeeHead:head.vtx[4338]', \
u'BruceLeeHead:head.vtx[161]', u'BruceLeeHead:head.vtx[4670]', u'BruceLeeHead:head.vtx[693]', u'BruceLeeHead:head.vtx[515]', \
u'BruceLeeHead:head.vtx[17]', u'BruceLeeHead:head.vtx[785]']  
SP1 = [u'Emily_2_1:Emily_head.vtx[1490]', u'Emily_2_1:Emily_head.vtx[10749]', u'Emily_2_1:Emily_head.vtx[11855]', \
u'Emily_2_1:Emily_head.vtx[6083]', u'Emily_2_1:Emily_head.vtx[4857]', u'Emily_2_1:Emily_head.vtx[11556]', \
u'Emily_2_1:Emily_head.vtx[5788]', u'Emily_2_1:Emily_head.vtx[10260]', u'Emily_2_1:Emily_head.vtx[21785]', \
u'Emily_2_1:Emily_head.vtx[20671]', u'Emily_2_1:Emily_head.vtx[20262]', u'Emily_2_1:Emily_head.vtx[20926]', \
u'Emily_2_1:Emily_head.vtx[18330]', u'Emily_2_1:Emily_head.vtx[19045]', u'Emily_2_1:Emily_head.vtx[18565]', \
u'Emily_2_1:Emily_head.vtx[19895]', u'Emily_2_1:Emily_head.vtx[22014]', u'Emily_2_1:Emily_head.vtx[21424]', \
u'Emily_2_1:Emily_head.vtx[21250]', u'Emily_2_1:Emily_head.vtx[20094]', u'Emily_2_1:Emily_head.vtx[19613]', \
u'Emily_2_1:Emily_head.vtx[11553]', u'Emily_2_1:Emily_head.vtx[2449]', u'Emily_2_1:Emily_head.vtx[452]', \
u'Emily_2_1:Emily_head.vtx[8791]', u'Emily_2_1:Emily_head.vtx[15499]', u'Emily_2_1:Emily_head.vtx[1381]', \
u'Emily_2_1:Emily_head.vtx[1708]', u'Emily_2_1:Emily_head.vtx[1555]', u'Emily_2_1:Emily_head.vtx[22377]', \
u'Emily_2_1:Emily_head.vtx[22417]', u'Emily_2_1:Emily_head.vtx[22872]', u'Emily_2_1:Emily_head.vtx[23195]', \
u'Emily_2_1:Emily_head.vtx[956]', u'Emily_2_1:Emily_head.vtx[13006]', u'Emily_2_1:Emily_head.vtx[6781]', \
u'Emily_2_1:Emily_head.vtx[18065]', u'Emily_2_1:Emily_head.vtx[13516]', u'Emily_2_1:Emily_head.vtx[2429]', \
u'Emily_2_1:Emily_head.vtx[13656]', u'Emily_2_1:Emily_head.vtx[14909]', u'Emily_2_1:Emily_head.vtx[16363]', \
u'Emily_2_1:Emily_head.vtx[3995]', u'Emily_2_1:Emily_head.vtx[16143]', u'Emily_2_1:Emily_head.vtx[3972]', \
u'Emily_2_1:Emily_head.vtx[17034]', u'Emily_2_1:Emily_head.vtx[2773]', u'Emily_2_1:Emily_head.vtx[14925]', \
u'Emily_2_1:Emily_head.vtx[11937]', u'Emily_2_1:Emily_head.vtx[3157]', u'Emily_2_1:Emily_head.vtx[7237]', \
u'Emily_2_1:Emily_head.vtx[3646]', u'Emily_2_1:Emily_head.vtx[8185]', u'Emily_2_1:Emily_head.vtx[6020]']

SP0Ind = []
for i in SP0:
    temp = re.findall('\d+', i)
    SP0Ind.append(int(temp[len(temp)-1]))
cmds.select(clear = True)
for i in SP0Ind:
    cmds.select(sourceName[0]+".vtx["+str(i)+"]", add=True)
    
# then click "Set Selected Points" for source key points
    
SP1Ind = []
for i in SP1:
    temp = re.findall('\d+', i)
    SP1Ind.append(int(temp[len(temp)-1]))
cmds.select(clear = True)
for i in SP1Ind:
    cmds.select(targetName[0]+".vtx["+str(i)+"]", add=True)	
    
# then click "Set Selected Points" for target key points	

# key points neutral head
[u'neutral.vtx[437]',
 u'neutral.vtx[18]',
 u'neutral.vtx[1469]',
 u'neutral.vtx[246]',
 u'neutral.vtx[269]',
 u'neutral.vtx[979]',
 u'neutral.vtx[906]',
 u'neutral.vtx[981]',
 u'neutral.vtx[911]',
 u'neutral.vtx[1186]',
 u'neutral.vtx[3192]',
 u'neutral.vtx[1099]',
 u'neutral.vtx[81]',
 u'neutral.vtx[2560]',
 u'neutral.vtx[2814]',
 u'neutral.vtx[4980]',
 u'neutral.vtx[3167]',
 u'neutral.vtx[1572]',
 u'neutral.vtx[3266]',
 u'neutral.vtx[4307]',
 u'neutral.vtx[2236]',
 u'neutral.vtx[1546]',
 u'neutral.vtx[3335]',
 u'neutral.vtx[3054]',
 u'neutral.vtx[2971]',
 u'neutral.vtx[3360]',
 u'neutral.vtx[1992]',
 u'neutral.vtx[1951]',
 u'neutral.vtx[3080]',
 u'neutral.vtx[2727]',
 u'neutral.vtx[972]',
 u'neutral.vtx[897]',
 u'neutral.vtx[1561]',
 u'neutral.vtx[1070]',
 u'neutral.vtx[1596]',
 u'neutral.vtx[1044]',
 u'neutral.vtx[3300]',
 u'neutral.vtx[3389]',
 u'neutral.vtx[4976]',
 u'neutral.vtx[2483]',
 u'neutral.vtx[4880]',
 u'neutral.vtx[6264]',
 u'neutral.vtx[3467]',
 u'neutral.vtx[5696]',
 u'neutral.vtx[3230]',
 u'neutral.vtx[9920]',
 u'neutral.vtx[4946]',
 u'neutral.vtx[5377]',
 u'neutral.vtx[8882]',
 u'neutral.vtx[9315]',
 u'neutral.vtx[4658]',
 u'neutral.vtx[4272]',
 u'neutral.vtx[9016]',
 u'neutral.vtx[3902]',
 u'neutral.vtx[5836]',
 u'neutral.vtx[3575]',
 u'neutral.vtx[6923]',
 u'neutral.vtx[10154]',
 u'neutral.vtx[6791]']
 
 #MPC scanned head
 [u'BU_scan_neutral:target.vtx[14186]',
 u'BU_scan_neutral:target.vtx[14295]',
 u'BU_scan_neutral:target.vtx[13916]',
 u'BU_scan_neutral:target.vtx[14147]',
 u'BU_scan_neutral:target.vtx[17453]',
 u'BU_scan_neutral:target.vtx[8116]',
 u'BU_scan_neutral:target.vtx[13952]',
 u'BU_scan_neutral:target.vtx[4713]',
 u'BU_scan_neutral:target.vtx[13963]',
 u'BU_scan_neutral:target.vtx[24756]',
 u'BU_scan_neutral:target.vtx[14981]',
 u'BU_scan_neutral:target.vtx[17663]',
 u'BU_scan_neutral:target.vtx[8906]',
 u'BU_scan_neutral:target.vtx[20693]',
 u'BU_scan_neutral:target.vtx[19624]',
 u'BU_scan_neutral:target.vtx[37169]',
 u'BU_scan_neutral:target.vtx[23222]',
 u'BU_scan_neutral:target.vtx[37172]',
 u'BU_scan_neutral:target.vtx[10540]',
 u'BU_scan_neutral:target.vtx[36538]',
 u'BU_scan_neutral:target.vtx[26850]',
 u'BU_scan_neutral:target.vtx[10552]',
 u'BU_scan_neutral:target.vtx[19592]',
 u'BU_scan_neutral:target.vtx[26841]',
 u'BU_scan_neutral:target.vtx[4599]',
 u'BU_scan_neutral:target.vtx[13766]',
 u'BU_scan_neutral:target.vtx[19653]',
 u'BU_scan_neutral:target.vtx[19706]',
 u'BU_scan_neutral:target.vtx[39248]',
 u'BU_scan_neutral:target.vtx[23156]',
 u'BU_scan_neutral:target.vtx[8194]',
 u'BU_scan_neutral:target.vtx[6076]',
 u'BU_scan_neutral:target.vtx[13981]',
 u'BU_scan_neutral:target.vtx[8332]',
 u'BU_scan_neutral:target.vtx[23210]',
 u'BU_scan_neutral:target.vtx[17504]',
 u'BU_scan_neutral:target.vtx[14757]',
 u'BU_scan_neutral:target.vtx[10809]',
 u'BU_scan_neutral:target.vtx[13736]',
 u'BU_scan_neutral:target.vtx[8029]',
 u'BU_scan_neutral:target.vtx[16897]',
 u'BU_scan_neutral:target.vtx[7763]',
 u'BU_scan_neutral:target.vtx[13559]',
 u'BU_scan_neutral:target.vtx[3123]',
 u'BU_scan_neutral:target.vtx[37802]',
 u'BU_scan_neutral:target.vtx[2015]',
 u'BU_scan_neutral:target.vtx[4970]',
 u'BU_scan_neutral:target.vtx[13669]',
 u'BU_scan_neutral:target.vtx[3874]',
 u'BU_scan_neutral:target.vtx[16179]',
 u'BU_scan_neutral:target.vtx[16653]',
 u'BU_scan_neutral:target.vtx[9974]',
 u'BU_scan_neutral:target.vtx[22611]',
 u'BU_scan_neutral:target.vtx[39743]',
 u'BU_scan_neutral:target.vtx[21375]',
 u'BU_scan_neutral:target.vtx[27164]',
 u'BU_scan_neutral:target.vtx[22100]',
 u'BU_scan_neutral:target.vtx[28091]',
 u'BU_scan_neutral:target.vtx[23544]']
 
 SP0 = [u'BruceLeeHead:head.vtx[814]', u'BruceLeeHead:head.vtx[819]', u'BruceLeeHead:head.vtx[826]', u'BruceLeeHead:head.vtx[5299]', u'BruceLeeHead:head.vtx[1245]', u'BruceLeeHead:head.vtx[808]', u'BruceLeeHead:head.vtx[5276]', u'BruceLeeHead:head.vtx[1222]', u'BruceLeeHead:head.vtx[7264]', u'BruceLeeHead:head.vtx[7315]', u'BruceLeeHead:head.vtx[6440]', u'BruceLeeHead:head.vtx[6467]', u'BruceLeeHead:head.vtx[2361]', u'BruceLeeHead:head.vtx[3261]', u'BruceLeeHead:head.vtx[3262]', u'BruceLeeHead:head.vtx[2413]', u'BruceLeeHead:head.vtx[8136]', u'BruceLeeHead:head.vtx[7925]', u'BruceLeeHead:head.vtx[7661]', u'BruceLeeHead:head.vtx[3592]', u'BruceLeeHead:head.vtx[3872]', u'BruceLeeHead:head.vtx[4088]', u'BruceLeeHead:head.vtx[5183]', u'BruceLeeHead:head.vtx[771]', u'BruceLeeHead:head.vtx[3164]', u'BruceLeeHead:head.vtx[7841]', u'BruceLeeHead:head.vtx[3786]', u'BruceLeeHead:head.vtx[5740]', u'BruceLeeHead:head.vtx[1686]', u'BruceLeeHead:head.vtx[6769]', u'BruceLeeHead:head.vtx[6925]', u'BruceLeeHead:head.vtx[6324]', u'BruceLeeHead:head.vtx[6752]', u'BruceLeeHead:head.vtx[2715]', u'BruceLeeHead:head.vtx[2872]', u'BruceLeeHead:head.vtx[2799]', u'BruceLeeHead:head.vtx[2699]', u'BruceLeeHead:head.vtx[835]', u'BruceLeeHead:head.vtx[7626]', u'BruceLeeHead:head.vtx[3572]', u'BruceLeeHead:head.vtx[847]', u'BruceLeeHead:head.vtx[6078]', u'BruceLeeHead:head.vtx[1445]', u'BruceLeeHead:head.vtx[859]', u'BruceLeeHead:head.vtx[1471]', u'BruceLeeHead:head.vtx[5526]', u'BruceLeeHead:head.vtx[0]', u'BruceLeeHead:head.vtx[4338]', u'BruceLeeHead:head.vtx[161]', u'BruceLeeHead:head.vtx[4670]', u'BruceLeeHead:head.vtx[693]', u'BruceLeeHead:head.vtx[515]', u'BruceLeeHead:head.vtx[17]', u'BruceLeeHead:head.vtx[785]']  
SP1 = [u'Emily_2_1:Emily_head.vtx[1490]', u'Emily_2_1:Emily_head.vtx[10749]', u'Emily_2_1:Emily_head.vtx[11855]', u'Emily_2_1:Emily_head.vtx[6083]', u'Emily_2_1:Emily_head.vtx[4857]', u'Emily_2_1:Emily_head.vtx[11556]', u'Emily_2_1:Emily_head.vtx[5788]', u'Emily_2_1:Emily_head.vtx[10260]', u'Emily_2_1:Emily_head.vtx[21785]', u'Emily_2_1:Emily_head.vtx[20671]', u'Emily_2_1:Emily_head.vtx[20262]', u'Emily_2_1:Emily_head.vtx[20926]', u'Emily_2_1:Emily_head.vtx[18330]', u'Emily_2_1:Emily_head.vtx[19045]', u'Emily_2_1:Emily_head.vtx[18565]', u'Emily_2_1:Emily_head.vtx[19895]', u'Emily_2_1:Emily_head.vtx[22014]', u'Emily_2_1:Emily_head.vtx[21424]', u'Emily_2_1:Emily_head.vtx[21250]', u'Emily_2_1:Emily_head.vtx[20094]', u'Emily_2_1:Emily_head.vtx[19613]', u'Emily_2_1:Emily_head.vtx[11553]', u'Emily_2_1:Emily_head.vtx[2449]', u'Emily_2_1:Emily_head.vtx[452]', u'Emily_2_1:Emily_head.vtx[8791]', u'Emily_2_1:Emily_head.vtx[15499]', u'Emily_2_1:Emily_head.vtx[1381]', u'Emily_2_1:Emily_head.vtx[1708]', u'Emily_2_1:Emily_head.vtx[1555]', u'Emily_2_1:Emily_head.vtx[22377]', u'Emily_2_1:Emily_head.vtx[22417]', u'Emily_2_1:Emily_head.vtx[22872]', u'Emily_2_1:Emily_head.vtx[23195]', u'Emily_2_1:Emily_head.vtx[956]', u'Emily_2_1:Emily_head.vtx[13006]', u'Emily_2_1:Emily_head.vtx[6781]', u'Emily_2_1:Emily_head.vtx[18065]', u'Emily_2_1:Emily_head.vtx[13516]', u'Emily_2_1:Emily_head.vtx[2429]', u'Emily_2_1:Emily_head.vtx[13656]', u'Emily_2_1:Emily_head.vtx[14909]', u'Emily_2_1:Emily_head.vtx[16363]', u'Emily_2_1:Emily_head.vtx[3995]', u'Emily_2_1:Emily_head.vtx[16143]', u'Emily_2_1:Emily_head.vtx[3972]', u'Emily_2_1:Emily_head.vtx[17034]', u'Emily_2_1:Emily_head.vtx[2773]', u'Emily_2_1:Emily_head.vtx[14925]', u'Emily_2_1:Emily_head.vtx[11937]', u'Emily_2_1:Emily_head.vtx[3157]', u'Emily_2_1:Emily_head.vtx[7237]', u'Emily_2_1:Emily_head.vtx[3646]', u'Emily_2_1:Emily_head.vtx[8185]', u'Emily_2_1:Emily_head.vtx[6020]']
# key points neutral head
SP0 = [u'neutral.vtx[437]',  u'neutral.vtx[18]', u'neutral.vtx[1469]', u'neutral.vtx[246]', u'neutral.vtx[269]', u'neutral.vtx[979]', u'neutral.vtx[906]', u'neutral.vtx[981]', u'neutral.vtx[911]', u'neutral.vtx[1186]', u'neutral.vtx[3192]', u'neutral.vtx[1099]', u'neutral.vtx[81]', u'neutral.vtx[2560]', u'neutral.vtx[2814]', u'neutral.vtx[4980]', u'neutral.vtx[3167]', u'neutral.vtx[1572]', u'neutral.vtx[3266]', u'neutral.vtx[4307]', u'neutral.vtx[2236]', u'neutral.vtx[1546]', u'neutral.vtx[3335]', u'neutral.vtx[3054]', u'neutral.vtx[2971]', u'neutral.vtx[3360]', u'neutral.vtx[1992]', u'neutral.vtx[1951]', u'neutral.vtx[3080]', u'neutral.vtx[2727]', u'neutral.vtx[972]', u'neutral.vtx[897]', u'neutral.vtx[1561]', u'neutral.vtx[1070]', u'neutral.vtx[1596]', u'neutral.vtx[1044]', u'neutral.vtx[3300]', u'neutral.vtx[3389]', u'neutral.vtx[4976]', u'neutral.vtx[2483]', u'neutral.vtx[4880]', u'neutral.vtx[6264]', u'neutral.vtx[3467]', u'neutral.vtx[5696]', u'neutral.vtx[3230]', u'neutral.vtx[9920]', u'neutral.vtx[4946]', u'neutral.vtx[5377]', u'neutral.vtx[8882]', u'neutral.vtx[9315]', u'neutral.vtx[4658]', u'neutral.vtx[4272]', u'neutral.vtx[9016]', u'neutral.vtx[3902]', u'neutral.vtx[5836]', u'neutral.vtx[3575]', u'neutral.vtx[6923]', u'neutral.vtx[10154]', u'neutral.vtx[6791]']  
SP0Ind = []
	# extracting the vertex indices in vList adjusted from http://stackoverflow.com/questions/10365225/extract-digits-in-a-simple-way-from-a-python-string
	# answer by user senderle
for i in SP0:
    temp = re.findall('\d+', i)
    SP0Ind.append(int(temp[len(temp)-1]))
cmds.select(clear = True)
for i in SP0Ind:
    cmds.select(sourceName[0]+".vtx["+str(i)+"]", add=True)	
#MPC scanned head
SP1 = [u'BU_scan_neutral:target.vtx[14186]', u'BU_scan_neutral:target.vtx[14295]', u'BU_scan_neutral:target.vtx[13916]', u'BU_scan_neutral:target.vtx[14147]', u'BU_scan_neutral:target.vtx[17453]', u'BU_scan_neutral:target.vtx[8116]', u'BU_scan_neutral:target.vtx[13952]', u'BU_scan_neutral:target.vtx[4713]', u'BU_scan_neutral:target.vtx[13963]', u'BU_scan_neutral:target.vtx[24756]', u'BU_scan_neutral:target.vtx[14981]', u'BU_scan_neutral:target.vtx[17663]', u'BU_scan_neutral:target.vtx[8906]', u'BU_scan_neutral:target.vtx[20693]', u'BU_scan_neutral:target.vtx[19624]', u'BU_scan_neutral:target.vtx[37169]', u'BU_scan_neutral:target.vtx[23222]', u'BU_scan_neutral:target.vtx[37172]', u'BU_scan_neutral:target.vtx[10540]', u'BU_scan_neutral:target.vtx[36538]', u'BU_scan_neutral:target.vtx[26850]', u'BU_scan_neutral:target.vtx[10552]', u'BU_scan_neutral:target.vtx[19592]', u'BU_scan_neutral:target.vtx[26841]', u'BU_scan_neutral:target.vtx[4599]', u'BU_scan_neutral:target.vtx[13766]', u'BU_scan_neutral:target.vtx[19653]', u'BU_scan_neutral:target.vtx[19706]', u'BU_scan_neutral:target.vtx[39248]', u'BU_scan_neutral:target.vtx[23156]', u'BU_scan_neutral:target.vtx[8194]', u'BU_scan_neutral:target.vtx[6076]', u'BU_scan_neutral:target.vtx[13981]', u'BU_scan_neutral:target.vtx[8332]', u'BU_scan_neutral:target.vtx[23210]', u'BU_scan_neutral:target.vtx[17504]', u'BU_scan_neutral:target.vtx[14757]', u'BU_scan_neutral:target.vtx[10809]', u'BU_scan_neutral:target.vtx[13736]', u'BU_scan_neutral:target.vtx[8029]', u'BU_scan_neutral:target.vtx[16897]', u'BU_scan_neutral:target.vtx[7763]', u'BU_scan_neutral:target.vtx[13559]', u'BU_scan_neutral:target.vtx[3123]', u'BU_scan_neutral:target.vtx[37802]', u'BU_scan_neutral:target.vtx[2015]', u'BU_scan_neutral:target.vtx[4970]', u'BU_scan_neutral:target.vtx[13669]', u'BU_scan_neutral:target.vtx[3874]', u'BU_scan_neutral:target.vtx[16179]', u'BU_scan_neutral:target.vtx[16653]', u'BU_scan_neutral:target.vtx[9974]', u'BU_scan_neutral:target.vtx[22611]', u'BU_scan_neutral:target.vtx[39743]', u'BU_scan_neutral:target.vtx[21375]', u'BU_scan_neutral:target.vtx[27164]', u'BU_scan_neutral:target.vtx[22100]', u'BU_scan_neutral:target.vtx[28091]', u'BU_scan_neutral:target.vtx[23544]']

SP1Ind = []
	# extracting the vertex indices in vList adjusted from http://stackoverflow.com/questions/10365225/extract-digits-in-a-simple-way-from-a-python-string
	# answer by user senderle
for i in SP1:
    temp = re.findall('\d+', i)
    SP1Ind.append(int(temp[len(temp)-1]))
cmds.select(clear = True)
for i in SP1Ind:
    cmds.select(targetName[0]+".vtx["+str(i)+"]", add=True)	
