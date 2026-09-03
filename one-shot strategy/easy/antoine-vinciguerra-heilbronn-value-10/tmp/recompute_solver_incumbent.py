from decimal import Decimal, getcontext
from itertools import combinations

getcontext().prec = 60
D = Decimal

points = [
    (D(0), D("1.5776966564337988e-01")),
    (D("1.5776918279894869e-01"), D(0)),
    (D(1), D("2.5229899436114711e-01")),
    (D("2.5229821227659222e-01"), D(1)),
    (D(0), D("7.4771265099701756e-01")),
    (D("3.1554545332229172e-01"), D("6.8446114578430783e-01")),
    (D("6.8446133340174209e-01"), D("3.1554633629339085e-01")),
    (D("7.4771205608820868e-01"), D(0)),
    (D("8.4222781044957729e-01"), D(1)),
    (D(1), D("8.4222525064314724e-01")),
]

def area(t):
    i, j, k = t
    p, q, r = points[i], points[j], points[k]
    det = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])
    return abs(det)/2

areas = sorted((area(t), t) for t in combinations(range(10), 3))
reported = D("4.6537650338668655e-02")
known = D("0.0465374195825417726")
print("reported delta =", reported)
print("direct minimum =", areas[0][0], "at", areas[0][1])
print("reported minus direct =", reported - areas[0][0])
print("direct minus exact known A =", areas[0][0] - known)
print("ten smallest:")
for value, triple in areas[:10]:
    print(triple, value)
