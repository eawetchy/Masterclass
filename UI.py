SelP0 = [u'BruceLeeHead:head.vtx[814]', u'BruceLeeHead:head.vtx[819]', u'BruceLeeHead:head.vtx[826]', u'BruceLeeHead:head.vtx[5299]', u'BruceLeeHead:head.vtx[1245]', u'BruceLeeHead:head.vtx[808]', u'BruceLeeHead:head.vtx[5276]', u'BruceLeeHead:head.vtx[1222]', u'BruceLeeHead:head.vtx[7264]', u'BruceLeeHead:head.vtx[7315]', u'BruceLeeHead:head.vtx[6440]', u'BruceLeeHead:head.vtx[6467]', u'BruceLeeHead:head.vtx[2361]', u'BruceLeeHead:head.vtx[3261]', u'BruceLeeHead:head.vtx[3262]', u'BruceLeeHead:head.vtx[2413]', u'BruceLeeHead:head.vtx[8136]', u'BruceLeeHead:head.vtx[7925]', u'BruceLeeHead:head.vtx[7661]', u'BruceLeeHead:head.vtx[3592]', u'BruceLeeHead:head.vtx[3872]', u'BruceLeeHead:head.vtx[4088]', u'BruceLeeHead:head.vtx[5183]', u'BruceLeeHead:head.vtx[771]', u'BruceLeeHead:head.vtx[3164]', u'BruceLeeHead:head.vtx[7841]', u'BruceLeeHead:head.vtx[3786]', u'BruceLeeHead:head.vtx[5740]', u'BruceLeeHead:head.vtx[1686]', u'BruceLeeHead:head.vtx[6769]', u'BruceLeeHead:head.vtx[6925]', u'BruceLeeHead:head.vtx[6324]', u'BruceLeeHead:head.vtx[6752]', u'BruceLeeHead:head.vtx[2715]', u'BruceLeeHead:head.vtx[2872]', u'BruceLeeHead:head.vtx[2799]', u'BruceLeeHead:head.vtx[2699]', u'BruceLeeHead:head.vtx[835]', u'BruceLeeHead:head.vtx[7626]', u'BruceLeeHead:head.vtx[3572]', u'BruceLeeHead:head.vtx[847]', u'BruceLeeHead:head.vtx[6078]', u'BruceLeeHead:head.vtx[1445]', u'BruceLeeHead:head.vtx[859]', u'BruceLeeHead:head.vtx[1471]', u'BruceLeeHead:head.vtx[5526]', u'BruceLeeHead:head.vtx[0]', u'BruceLeeHead:head.vtx[4338]', u'BruceLeeHead:head.vtx[161]', u'BruceLeeHead:head.vtx[4670]', u'BruceLeeHead:head.vtx[693]', u'BruceLeeHead:head.vtx[515]', u'BruceLeeHead:head.vtx[17]', u'BruceLeeHead:head.vtx[785]']  
SelP1 = [u'Emily_2_1:Emily_head.vtx[1490]', u'Emily_2_1:Emily_head.vtx[10749]', u'Emily_2_1:Emily_head.vtx[11855]', u'Emily_2_1:Emily_head.vtx[6083]', u'Emily_2_1:Emily_head.vtx[4857]', u'Emily_2_1:Emily_head.vtx[11556]', u'Emily_2_1:Emily_head.vtx[5788]', u'Emily_2_1:Emily_head.vtx[10260]', u'Emily_2_1:Emily_head.vtx[21785]', u'Emily_2_1:Emily_head.vtx[20671]', u'Emily_2_1:Emily_head.vtx[20262]', u'Emily_2_1:Emily_head.vtx[20926]', u'Emily_2_1:Emily_head.vtx[18330]', u'Emily_2_1:Emily_head.vtx[19045]', u'Emily_2_1:Emily_head.vtx[18565]', u'Emily_2_1:Emily_head.vtx[19895]', u'Emily_2_1:Emily_head.vtx[22014]', u'Emily_2_1:Emily_head.vtx[21424]', u'Emily_2_1:Emily_head.vtx[21250]', u'Emily_2_1:Emily_head.vtx[20094]', u'Emily_2_1:Emily_head.vtx[19613]', u'Emily_2_1:Emily_head.vtx[11553]', u'Emily_2_1:Emily_head.vtx[2449]', u'Emily_2_1:Emily_head.vtx[452]', u'Emily_2_1:Emily_head.vtx[8791]', u'Emily_2_1:Emily_head.vtx[15499]', u'Emily_2_1:Emily_head.vtx[1381]', u'Emily_2_1:Emily_head.vtx[1708]', u'Emily_2_1:Emily_head.vtx[1555]', u'Emily_2_1:Emily_head.vtx[22377]', u'Emily_2_1:Emily_head.vtx[22417]', u'Emily_2_1:Emily_head.vtx[22872]', u'Emily_2_1:Emily_head.vtx[23195]', u'Emily_2_1:Emily_head.vtx[956]', u'Emily_2_1:Emily_head.vtx[13006]', u'Emily_2_1:Emily_head.vtx[6781]', u'Emily_2_1:Emily_head.vtx[18065]', u'Emily_2_1:Emily_head.vtx[13516]', u'Emily_2_1:Emily_head.vtx[2429]', u'Emily_2_1:Emily_head.vtx[13656]', u'Emily_2_1:Emily_head.vtx[14909]', u'Emily_2_1:Emily_head.vtx[16363]', u'Emily_2_1:Emily_head.vtx[3995]', u'Emily_2_1:Emily_head.vtx[16143]', u'Emily_2_1:Emily_head.vtx[3972]', u'Emily_2_1:Emily_head.vtx[17034]', u'Emily_2_1:Emily_head.vtx[2773]', u'Emily_2_1:Emily_head.vtx[14925]', u'Emily_2_1:Emily_head.vtx[11937]', u'Emily_2_1:Emily_head.vtx[3157]', u'Emily_2_1:Emily_head.vtx[7237]', u'Emily_2_1:Emily_head.vtx[3646]', u'Emily_2_1:Emily_head.vtx[8185]', u'Emily_2_1:Emily_head.vtx[6020]']
cmds.select(SelP0)
cmds.select(SelP1)

# adapted from Alex Pitter's UI code

import functools as ft
import copy

def useSelection(_field, *args):
    txt = cmds.ls(sl=True)
    cmds.textField( _field, edit=True, text=txt[0])
    
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
    
def matchTarg(sourceName, targetName, SKPs, TKPs, *args):
    source = str(retrieveText(sourceName))
    print "source: ", source
    target = str(retrieveText(targetName))
    print "target: ", target    
    print "SelP0: ", SelP0, "\nSelP1: ", SelP1
    matchTarget(source, target, SelP0, SelP1)

def makeGUI():
    winID = 'Expression Cloning'
    if cmds.window(winID, exists = True):
        cmds.deleteUI(winID)
    cmds.window(winID,widthHeight=(1000, 55))
    cmds.columnLayout(columnWidth = 500)
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(150, 150, 150))
    cmds.text(label='Source Mesh')
    sourceName = cmds.textField()
    cmds.button(label = 'Set Selected as Source', c = ft.partial(useSelection, sourceName))
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=4, columnWidth4 = (150,74,74,150))
    #target model
    cmds.text(label='Source Key Points:')
    SKP = cmds.textField()
    arraySource = cmds.textField(vis = False)
    cmds.button(label = 'Set Selected Points', c = ft.partial(useSelectedPoints, SKP, True)) 
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(150, 150, 150))
    #target model
    cmds.text(label='Target Mesh:')
    targetName = cmds.textField()
    cmds.button(label = 'Set Selected as Target', c = ft.partial(useSelection, targetName)) 
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=4, columnWidth4 = (150,74,74,150))
    cmds.text(label='Target Key Points')
    TKP = cmds.textField()
    arrayTarget = cmds.textField(vis = False)
    cmds.button(label = 'Set Selected Points', c = ft.partial(useSelectedPoints, TKP, False))
    cmds.setParent('..')
    
    #, c = matchTarget(sourceName, targetName, SelP0, SelP1)) 
    cmds.button(label = 'Deform Source Model' , c=ft.partial(matchTarg, sourceName, targetName, arraySource, arrayTarget))
    cmds.button(label = 'Create Blendshapes ')
    
    cmds.showWindow()

def main():
    SelP0 = []
    SelP1 = []
    makeGUI()
    
main()
