import itertools
from fractions import Fraction

import sympy as s

z = s.symbols("z")
f = 12*z**3 - 27*z**2 + 20*z - 4
x = z/2
y = (1-z)*(1-2*z)
A = s.rem((5*z**2 - 4*z**3)/8, f, domain=s.QQ)

pts = [
    (x, 0), (1-y, 0), (0, x), (1, y), (1-z, z),
    (z, 1-z), (0, 1-y), (1, 1-x), (y, 1), (1-x, 1),
]

lo, hi = s.Rational(789, 2500), s.Rational(3157, 10000)

def red(expr):
    return s.factor(s.rem(s.together(expr), f, domain=s.QQ))

def det_area(i, j, k):
    p, q, r = pts[i], pts[j], pts[k]
    return red(((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]))/2)

def interval(poly):
    poly = s.Poly(poly, z, domain=s.QQ)
    values = [poly.eval(lo), poly.eval(hi)]
    if poly.degree() == 2:
        aa, bb, _ = poly.all_coeffs()
        vertex = -bb/(2*aa)
        if lo <= vertex <= hi:
            values.append(poly.eval(vertex))
    return min(values), max(values)

assert s.discriminant(f, z) < 0
assert f.subs(z, lo) < 0 < f.subs(z, hi)
assert red(A - (-3*z**2 + 5*z - 1)/6) == 0
assert s.factor(s.resultant(f, 6*A - (-3*z**2 + 5*z - 1), z)) == 0

critical = []
strict_margins = []
for triple in itertools.combinations(range(10), 3):
    q = det_area(*triple)
    qlo, qhi = interval(q)
    assert qlo > 0 or qhi < 0  # orientation is constant on the isolating interval
    signed = q if qlo > 0 else -q
    dlo, dhi = interval(red(signed - A))
    assert dlo >= 0
    if red(signed - A) == 0:
        critical.append(triple)
    else:
        strict_margins.append(dlo)

T = s.symbols("T")
minpoly = s.factor(s.resultant(f, 6*T - (-3*z**2 + 5*z - 1), z))
print("disc(f) =", s.discriminant(f, z))
print("isolating signs =", f.subs(z, lo), f.subs(z, hi))
print("A =", A)
print("minimal polynomial resultant =", minpoly)
print("critical triangle count =", len(critical))
print("critical triples =", critical)
print("smallest rigorous strict interval margin =", min(strict_margins))
print("numeric z, A =", s.N(s.RootOf(f, 0), 18), s.N(A.subs(z, s.RootOf(f, 0)), 18))
