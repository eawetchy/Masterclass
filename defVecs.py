N0 = sympy.zeros(len(AllP0),1) #normal matrix of source shape
ind = 0
for i in AllP0:
	cmds.select(i)
	n = cmds.polyNormalPerVertex( query=True, xyz=True )
	vn = 0
	for j in n:
		vn += j
	vn = vn/len(n)
	N0[ind] = vn
	
N1 = sympy.zeros(len(AllP0),1) #normal matrix of source blendshape
ind = 0
for i in AllPBlend:
	cmds.select(i)
	n = cmds.polyNormalPerVertex( query=True, xyz=True )
	vn = 0
	for j in n:
		vn += j
	vn = vn/len(n)
	N[ind] = vn	 
	
# find tangent plane of the normal
# Will return the edges in numeric order:
edges = cmds.polyListComponentConversion( AllP0[0], fv=True, te=True )
vList = cmds.polyListComponentConversion( edges[0], fe=True, tv=True )
q = vList[0]
		 
q = (x, y, z) # end point of the edge 
# projected onto a plane given by a point 
p = (a, b, c) # plane point 
n = (d, e, f) # plane normal, normalised

q_proj = q - dot(q - p, n) * n
