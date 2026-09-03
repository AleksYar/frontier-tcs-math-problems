from fractions import Fraction
from itertools import combinations, product
from random import Random
from collections import Counter


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


spaces = list(rref_subspaces(8, 4))
monomials = [sum(1 << i for i in S) for degree in (1, 2) for S in combinations(range(8), degree)]


def phase(anf):
    return tuple(1 if sum((x & mask) == mask for mask in anf) % 2 == 0 else -1 for x in range(256))


def sums(signs):
    return tuple(sum(signs[x] for x in L) for L in spaces)


def best_projection(pairs):
    slopes = {Fraction(0)}
    rows = list(pairs)
    for i, p in enumerate(rows):
        for q in rows[i + 1:]:
            if p[1] != q[1]:
                slopes.add(Fraction(q[0] - p[0], p[1] - q[1]))
    best = None
    for slope in slopes:
        values = {a + slope * b for a, b in rows}
        candidate = (len(values), slope, tuple(sorted(values)))
        if best is None or candidate < best:
            best = candidate
    return best


rng = Random(831944)
results = []
for trial in range(80):
    anf1 = tuple(m for m in monomials if rng.randrange(2))
    anf2 = tuple(m for m in monomials if rng.randrange(2))
    s1, s2 = sums(phase(anf1)), sums(phase(anf2))
    pairs = set(zip(s1, s2))
    results.append((best_projection(pairs), len(pairs), anf1, anf2))

results.sort(key=lambda row: row[0])
print("spaces", len(spaces), "trials", len(results))
print("minimum-level distribution", Counter(row[0][0] for row in results))
for row in results[:20]:
    print(row)
