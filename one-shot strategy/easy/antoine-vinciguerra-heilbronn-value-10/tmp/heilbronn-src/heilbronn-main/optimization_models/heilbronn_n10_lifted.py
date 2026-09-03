"""Lifted n=10 global model with fewer than 200 variables for a restricted license."""
from gurobipy import Model, GRB, Var
from itertools import combinations
import os

n = 10
points = range(n)
triangles = list(combinations(points, 3))
m = Model("Heilbronn-n10-lifted")

x = {0: 0.0, 1: m.addVar(lb=0, ub=1, name="x1"), 2: 1.0,
     3: m.addVar(lb=0, ub=1, name="x3"), 4: 0.0}
y = {0: m.addVar(lb=0, ub=1, name="y0"), 1: 0.0,
     2: m.addVar(lb=0, ub=1, name="y2"), 3: 1.0,
     4: m.addVar(lb=0, ub=1, name="y4")}
for i in range(5, n):
    x[i] = m.addVar(lb=0, ub=1, name=f"x{i}")
    y[i] = m.addVar(lb=0, ub=1, name=f"y{i}")
m.addConstr(x[1] <= x[3])
m.addConstr(y[0] <= y[4])
for i in range(6, n):
    m.addConstr(x[i-1] <= x[i])

# Lift only genuinely bilinear products. Products involving a fixed 0 or 1
# are simplified, saving 44 variables compared with the published script.
w = {}
def xy(i,j):
    a,c = x[i],y[j]
    if isinstance(a,(int,float)): return a*c
    if isinstance(c,(int,float)): return c*a
    if (i,j) not in w:
        w[i,j] = m.addVar(lb=0,ub=1,name=f"w{i}_{j}")
        m.addConstr(w[i,j] == a*c)
    return w[i,j]

delta = m.addVar(lb=float(os.getenv("DELTA_LB", "0")),
                 ub=0.054875999170896694, name="delta")

# Three x-ordered points in a vertical strip of width d form a triangle of
# area at most d/2.
for i in range(5,n-2):
    m.addConstr(x[i+2]-x[i] >= 2*delta)
m.addConstr(y[4]-y[0] >= 2*delta)
b = {}
areas = {}
for i,j,k in triangles:
    area = 0.5*(xy(i,j)-xy(i,k)-xy(j,i)+xy(j,k)+xy(k,i)-xy(k,j))
    areas[i,j,k]=area
    if k <= 4:
        m.addConstr(area >= delta)
    elif i == 0 and j == 4:
        m.addConstr(-area >= delta)
    else:
        b[i,j,k]=m.addVar(vtype=GRB.BINARY,name=f"b{i}_{j}_{k}")
        m.addQConstr((2*b[i,j,k]-1)*area >= delta)

# Rank-3 chirotope cuts. For four noncollinear points i<j<k<l, the signs of
# (ijk),(ijl),(ikl),(jkl) cannot be 0101 or 1010. Equivalently, their
# alternating sum lies in [-1,1]. These are exact realizability constraints.
def orient(t):
    i,j,k=t
    if k <= 4: return 1.0
    if i == 0 and j == 4: return 0.0
    return b[t]
for i,j,k,l in combinations(points,4):
    alt=orient((i,j,k))-orient((i,j,l))+orient((i,k,l))-orient((j,k,l))
    m.addConstr(alt <= 1)
    m.addConstr(alt >= -1)

candidate = {
    0: (0.0, 0.15780556880430557), 1: (0.15780556880430557, 0.0),
    2: (1.0, 0.2523873675393699), 3: (0.2523873675393699, 1.0),
    4: (0.0, 0.74761263246063), 5: (0.31561113760861115, 0.6843888623913889),
    6: (0.6843888623913889, 0.31561113760861115), 7: (0.74761263246063, 0.0),
    8: (0.8421944311956944, 1.0), 9: (1.0, 0.8421944311956944),
}
for i,(cx,cy) in candidate.items():
    if i not in (0,2,4): x[i].Start=cx
    if i not in (1,3): y[i].Start=cy
for (i,j),v in w.items(): v.Start=candidate[i][0]*candidate[j][1]
for (i,j,k),v in b.items():
    p,q,r=candidate[i],candidate[j],candidate[k]
    candidate_orientation=int((q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])>=0)
    v.Start=candidate_orientation
    if os.getenv("FIX_CANDIDATE_ORDER") == "1":
        v.LB=v.UB=candidate_orientation
delta.Start=0.0465

m.setObjective(delta,GRB.MAXIMIZE)
m.Params.TimeLimit=float(os.getenv("TIME_LIMIT", "7200"))
m.Params.MIPFocus=2
m.Params.NonConvex=2
if os.getenv("STRICT_NUMERICS") == "1":
    m.Params.MIPGap=1e-10
    m.Params.FeasibilityTol=1e-9
    m.Params.OptimalityTol=1e-9
    m.Params.NumericFocus=3
m.Params.LogFile="n10-lifted-global-search.log"
print(f"MODEL_VARIABLES={m.NumVars} LIFTED_PRODUCTS={len(w)} ORIENTATION_BINARIES={len(b)}")
m.optimize()
m.write("n10-lifted-result.sol")
print(f"STATUS={m.Status} BOUND={m.ObjBound:.17g} INCUMBENT={m.ObjVal:.17g} GAP={m.MIPGap:.17g}")
