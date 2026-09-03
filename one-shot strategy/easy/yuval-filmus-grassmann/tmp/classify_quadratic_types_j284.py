from itertools import combinations, product
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


def bit(x, i):
    return (x >> i) & 1


def quadratic(x, rank, arf, radical_linear):
    pairs = rank // 2
    value = 0
    hyperbolic_pairs = pairs if arf == 0 else pairs - 1
    for i in range(hyperbolic_pairs):
        value ^= bit(x, 2 * i) & bit(x, 2 * i + 1)
    if arf and pairs:
        i = pairs - 1
        a, b = bit(x, 2 * i), bit(x, 2 * i + 1)
        value ^= a ^ (a & b) ^ b
    if radical_linear and rank < 8:
        value ^= bit(x, rank)
    return value


for rank in (0, 2, 4, 6, 8):
    for arf in ((0,) if rank == 0 else (0, 1)):
        for radical_linear in ((0,) if rank == 8 else (0, 1)):
            phase = tuple((-1) ** quadratic(x, rank, arf, radical_linear) for x in range(256))
            distribution = Counter(sum(phase[x] for x in L) for L in spaces)
            print("rank", rank, "arf", arf, "radical_linear", radical_linear,
                  "levels", len(distribution), "distribution", dict(sorted(distribution.items())))
