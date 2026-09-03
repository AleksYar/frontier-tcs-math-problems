from itertools import combinations, product
from collections import Counter
from fractions import Fraction


def rref_subspaces(n, k):
    for pivots in combinations(range(n), k):
        pivot_set = set(pivots)
        free_slots = []
        for col in range(n):
            if col not in pivot_set:
                for row, pivot in enumerate(pivots):
                    if pivot < col:
                        free_slots.append((row, col))
        for bits in product((0, 1), repeat=len(free_slots)):
            rows = [1 << pivot for pivot in pivots]
            for bit, (row, col) in zip(bits, free_slots):
                if bit:
                    rows[row] |= 1 << col
            space = [0]
            for row in rows:
                space += [x ^ row for x in tuple(space)]
            yield tuple(sorted(space))


def bit(x, i):
    return (x >> i) & 1


def quadratic(x):
    # Three hyperbolic planes and one anisotropic plane: O^-(8,2).
    return (
        bit(x, 0) * bit(x, 1)
        + bit(x, 2) * bit(x, 3)
        + bit(x, 4) * bit(x, 5)
        + bit(x, 6)
        + bit(x, 6) * bit(x, 7)
        + bit(x, 7)
    ) % 2


def dot(a, b):
    return bin(a & b).count("1") % 2


spaces = list(rref_subspaces(8, 4))
assert len(spaces) == 200787, len(spaces)

representatives = {
    "zero": 0,
    "singular": next(x for x in range(1, 256) if quadratic(x) == 0),
    "nonsingular": next(x for x in range(1, 256) if quadratic(x) == 1),
}

walsh = {
    name: tuple(sum((-1) ** (quadratic(x) ^ dot(r, x)) for x in L) for L in spaces)
    for name, r in representatives.items()
}

print("spaces", len(spaces), "representatives", representatives)
for name, values in walsh.items():
    print(name, Counter(values))

for name in ("singular", "nonsingular"):
    for sign in (1, -1):
        values = tuple(a + sign * b for a, b in zip(walsh["zero"], walsh[name]))
        print("zero", "+" if sign == 1 else "-", name, Counter(values))

for name in ("singular", "nonsingular"):
    pairs = set(zip(walsh["zero"], walsh[name]))
    slopes = {Fraction(0)}
    for p in pairs:
        for q in pairs:
            if p != q and p[1] != q[1]:
                slopes.add(Fraction(q[0] - p[0], p[1] - q[1]))
    best = []
    for slope in slopes:
        values = {a + slope * b for a, b in pairs}
        best.append((len(values), slope, sorted(values)))
    print(name, "pairs", sorted(pairs))
    print(name, "best slopes", sorted(best, key=lambda row: row[0])[:10])

# Search a separate highly symmetric ansatz: point coefficients depending only
# on Hamming weight.  Normalize the weight-1 coefficient to zero and search
# small integral coefficients for the other seven weights.
weight_distributions = set()
for L in spaces:
    counts = [0] * 8
    for x in L:
        if x:
            counts[bin(x).count("1") - 1] += 1
    weight_distributions.add(tuple(counts))
print("distinct Hamming-weight distributions", len(weight_distributions))

small_solutions = []
for tail in product(range(-2, 3), repeat=7):
    coeff = (0,) + tail
    values = set()
    for distribution in weight_distributions:
        values.add(sum(a * b for a, b in zip(coeff, distribution)))
        if len(values) > 3:
            break
    if 1 < len(values) <= 3:
        ordered = sorted(values)
        if len(ordered) == 2 or ordered[0] + ordered[2] == 2 * ordered[1]:
            small_solutions.append((coeff, ordered))
print("small Hamming-weight three-level solutions", small_solutions[:50])
print("small Hamming-weight solution count", len(small_solutions))
