"""Compact n=10 global model, kept below Gurobi restricted-license variable limits."""
from gurobipy import Model, GRB
from itertools import combinations

n = 10
points = range(n)
triangles = list(combinations(points, 3))
m = Model("Heilbronn-n10-compact")

# Symmetry breaking justified by Proposition 2 of Sudermann--Merx (2026):
# p0,p4 on left; p1 bottom; p2 right; p3 top; remaining points x-sorted.
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

delta = m.addVar(lb=0, ub=0.05488068669327922, name="delta")
b = m.addVars(triangles, vtype=GRB.BINARY, name="orientation")

for i,j,k in triangles:
    area = 0.5*(x[i]*y[j] - x[i]*y[k] - x[j]*y[i] + x[j]*y[k]
                + x[k]*y[i] - x[k]*y[j])
    # b=1 selects positive orientation, b=0 negative.  Since |area|<=1/2,
    # M=1 makes the unselected inequality redundant.
    m.addConstr(area >= delta - (1-b[i,j,k]))
    m.addConstr(-area >= delta - b[i,j,k])

# All-boundary orientations are fixed by their counterclockwise labels.
for t in triangles:
    if t[2] <= 4:
        b[t].LB = b[t].UB = 1
    if t[0] == 0 and t[1] == 4:
        b[t].LB = b[t].UB = 0

candidate = {
    0: (0.0, 0.15780556880430557), 1: (0.15780556880430557, 0.0),
    2: (1.0, 0.2523873675393699), 3: (0.2523873675393699, 1.0),
    4: (0.0, 0.74761263246063), 5: (0.31561113760861115, 0.6843888623913889),
    6: (0.6843888623913889, 0.31561113760861115), 7: (0.74761263246063, 0.0),
    8: (0.8421944311956944, 1.0), 9: (1.0, 0.8421944311956944),
}
for i,(cx,cy) in candidate.items():
    if i not in (0, 2, 4): x[i].Start = cx
    if i not in (1, 3): y[i].Start = cy
for i,j,k in triangles:
    p,q,r = candidate[i],candidate[j],candidate[k]
    orient = (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    b[i,j,k].Start = int(orient >= 0)
delta.Start = 0.0465

m.setObjective(delta, GRB.MAXIMIZE)
m.Params.TimeLimit = 7200
m.Params.MIPFocus = 2
m.Params.NonConvex = 2
m.Params.LogFile = "n10-compact-global-search.log"
m.optimize()
m.write("n10-compact-result.sol")
print(f"STATUS={m.Status} BOUND={m.ObjBound:.17g} INCUMBENT={m.ObjVal:.17g} GAP={m.MIPGap:.17g}")
