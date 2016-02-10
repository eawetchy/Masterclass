#vertex list transformTarget
TP0 = getVtxPos( "targetShape" )

#vertex list transformSource
SP0 = getVtxPos( "sourceShape1" )

#extreme points transformTarget
TLM = []
tHX = getExtremePoint( "x", True, TP0 )
TLM.append(TP0[tHX])
tLX = getExtremePoint( "x", False, TP0 )
TLM.append(TP0[tLX])
tHY = getExtremePoint( "y", True, TP0 )
TLM.append(TP0[tHY])
tLY = getExtremePoint( "y", False, TP0 )
TLM.append(TP0[tLY])
tHZ = getExtremePoint( "z", True, TP0 )
TLM.append(TP0[tHZ])
tLZ = getExtremePoint( "z", False, TP0 )
TLM.append(TP0[tLZ])

#extreme points transformSource
SLM = []
sHX = getExtremePoint( "x", True, SP0 )
SLM.append(SP0[sHX])
sLX = getExtremePoint( "x", False, SP0 )
SLM.append(SP0[sLX])
sHY = getExtremePoint( "y", True, SP0 )
SLM.append(SP0[sHY])
sLY = getExtremePoint( "y", False, SP0 )
SLM.append(SP0[sLY])
sHZ = getExtremePoint( "z", True, SP0 )
SLM.append(SP0[sHZ])
sLZ = getExtremePoint( "z", False, SP0 )
SLM.append(SP0[sLZ])

#move transform source points
count = 0
for i in sourceLM:
    listIndex = targetLM[count]
    count+=1    
    cmds.polyMoveVertex( "source1.vtx[" + str(i) + "]", t =  targetVtcs[listIndex])

#so far only this works because world space won't let itself be turned on
count = 0
for i in sourceLM:
    listIndex = targetLM[count]
    listIndex2 = sourceLM[count]   
    x = targetVtcs[listIndex][0] - sourceVtcs[listIndex2][0]
    y = targetVtcs[listIndex][1] - sourceVtcs[listIndex2][1]
    z = targetVtcs[listIndex][2] - sourceVtcs[listIndex2][2]
    count+=1    
    cmds.polyMoveVertex( "source1.vtx[" + str(i) + "]", t =  [x, y, z])
