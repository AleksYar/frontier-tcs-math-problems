from fractions import Fraction
from itertools import combinations


def span(vectors):
    result = {0}
    for v in vectors:
        result |= {x ^ v for x in tuple(result)}
    return frozenset(result)


points = tuple(range(1, 64))
three_spaces = sorted({
    span((a, b, c))
    for a, b, c in combinations(points, 3)
    if len(span((a, b, c))) == 8
}, key=lambda space: tuple(sorted(space)))


def bit(x, i):
    return (x >> i) & 1


def quadratic(x):
    # Two hyperbolic planes and one anisotropic plane over F_2.
    return (
        bit(x, 0) * bit(x, 1)
        + bit(x, 2) * bit(x, 3)
        + bit(x, 4)
        + bit(x, 4) * bit(x, 5)
        + bit(x, 5)
    ) % 2


def dot(a, b):
    return bin(a & b).count("1") % 2


def trivial_booleans():
    zero = (0,) * len(three_spaces)
    one = (1,) * len(three_spaces)
    result = {zero, one}
    for p in points:
        xp = tuple(int(p in L) for L in three_spaces)
        result.add(xp)
        result.add(tuple(1 - x for x in xp))
    for r in points:
        yr = tuple(int(all(dot(r, x) == 0 for x in L)) for L in three_spaces)
        result.add(yr)
        result.add(tuple(1 - y for y in yr))
        for p in points:
            if dot(p, r) == 1:
                xp = tuple(int(p in L) for L in three_spaces)
                plus = tuple(x + y for x, y in zip(xp, yr))
                assert set(plus) <= {0, 1}
                result.add(plus)
                result.add(tuple(1 - z for z in plus))
    return result


walsh_sums = tuple(sum((-1) ** quadratic(x) for x in L) for L in three_spaces)
f = tuple(1 + s // 4 for s in walsh_sums)
assert all(s in {-4, 0, 4} for s in walsh_sums)
assert set(f) == {0, 1, 2}

# Direct coefficient verification, including the zero-vector correction.
coefficients = {
    x: Fraction(5, 28) + Fraction((-1) ** quadratic(x), 4)
    for x in points
}
assert all(sum(coefficients[x] for x in L if x) == f[i] for i, L in enumerate(three_spaces))

booleans = trivial_booleans()
splittings = []
for g in booleans:
    h = tuple(x - y for x, y in zip(f, g))
    if set(h) <= {0, 1}:
        # h is degree one automatically, so the Boolean theorem says it is
        # one of the functions already in booleans; check this explicitly.
        assert h in booleans
        splittings.append((g, h))

print("3-spaces", len(three_spaces))
print("Walsh distribution", {s: walsh_sums.count(s) for s in sorted(set(walsh_sums))})
print("f level distribution", {s: f.count(s) for s in sorted(set(f))})
print("trivial Booleans", len(booleans))
print("Boolean splittings", len(splittings))
print("coefficient distribution", {
    value: tuple(coefficients.values()).count(value)
    for value in sorted(set(coefficients.values()))
})

