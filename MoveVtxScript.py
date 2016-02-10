import maya.cmds as cmds

sel = cmds.ls(sl=1, fl=1)
print sel

for i in sel:
    cmds.polyMoveVertex( i, ws= 0, tx=2.0 )
