from fractions import Fraction
from itertools import combinations, product


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


def bit(x, i):
    return (x >> i) & 1


def Q(x, arf):
    value = bit(x, 0) * bit(x, 1) ^ bit(x, 2) * bit(x, 3)
    if arf:
        a, b = bit(x, 4), bit(x, 5)
        value ^= a ^ (a * b) ^ b
    else:
        value ^= bit(x, 4) * bit(x, 5)
    return value


def dot(a, b):
    return bin(a & b).count("1") & 1


def best_projection(pairs):
    rows = list(pairs)
    slopes = {Fraction(0)}
    for i, p in enumerate(rows):
        for q in rows[i + 1:]:
            if p[1] != q[1]:
                slopes.add(Fraction(q[0] - p[0], p[1] - q[1]))
    return min((len({a + slope * b for a, b in rows}), slope,
                tuple(sorted({a + slope * b for a, b in rows}))) for slope in slopes)


representatives = [0, 1, 3, 64, 65, 67, 128, 129, 131, 192, 193, 195]
for arf in (0, 1):
    phase = tuple((-1) ** Q(x, arf) for x in range(256))
    base = tuple(sum(phase[x] for x in L) for L in spaces)
    for r in representatives:
        linear = tuple(sum((-1) ** dot(r, x) for x in L) for L in spaces)
        pairs = set(zip(base, linear))
        print("arf", arf, "r", r, "pair count", len(pairs), "best", best_projection(pairs))
