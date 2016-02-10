import sympy

def RBFbasis (r,s):
    # x1, x2: 3D points expressed as row matrices
    R = ( r**2 + s**2)**0.5
    return R 
    
def closestPoint(lp, vertPos): #landmark point, query points
    e = []
    for m in range(0, (len(vertPos)-1)):
        w = lp.distance(sympy.Point3D(vertPos[m]))
        if w != 0:
            e.append(w)
    return min(e)
    
H = sympy.zeros(len(SP0),len(SLM));
for i in range(0,(len(SP0)-1)):
	for j in range(0, (len(SLM)-1)):
		H[i,j]=RBFbasis(sympy.Point3D(SP0[i]).distance(sympy.Point3D(SP0[SLM[j]])), 1)
		
HT = H.transpose()
HS = HT * H
Hinv = sympy.Matrix([[0.010796, -0.003159, -0.007284, 0.000000], 
[ -0.003159, 0.010796, -0.007284, 0.000000],
[-0.007284, -0.007284, 0.014769, 0.000000],
[0.000000, 0.000000, 0.000000, 0.000000]])
# Solve for the weights w
W = Hinv * HT * sympy.Matrix(SP0)

P1 = RBFeval(TLM, W, SP0)
    
def RBFeval( C, W, P0):
    #array of output points
    P = sympy.zeros(len(P0), 3)
    
    #h will contain the radial basis function evaluated at each point
    h = sympy.zeros(len(W),1)
    for i in range(0,len(P0)):
        for j in range(0, len(C)-1):
            h[j] = RBFbasis(sympy.Point3D(P0[i]).distance(sympy.Point3D(C[j])), 1)
        P[i] = W.transpose() * h
    return P
    

# Solve for the weights w_i
w = inv(H'*H)*H'*P0;#"fake" inverse because matrix isn't square


# This is flawed! You need to replace P0 with the points in the target
# model
P1 = rbfeval(KP1, w, P0);

for i in range(0,5):
    for j in range(0,5) :
        x1 = sympy.Point3D(SP0[SLM[i]])
        x2 = sympy.Point3D(TP0[TLM[j]])
        s = closestPoint(x2, SP0)
        M[i,j] = RBF(x1, x2, s)

#matrix of "actual" result values as f(x) --> x
F = sympy.zeros(6,3)
for i in range(0,5):
    for j in range(0,2):
            F[i,j] = TP0[TLM[i]][j]

MInv = M.inv()
X = MInv * F
