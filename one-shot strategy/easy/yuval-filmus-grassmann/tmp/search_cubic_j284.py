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
monomials = [sum(1 << i for i in S) for degree in (1, 2, 3) for S in combinations(range(8), degree)]


def phase_from_anf(anf):
    result = []
    for x in range(256):
        value = sum((x & mask) == mask for mask in anf) & 1
        result.append(1 if value == 0 else -1)
    return result


def restricted_sums(phase, stop_after=6):
    values = set()
    for L in spaces:
        values.add(sum(phase[x] for x in L))
        if len(values) >= stop_after:
            break
    return values


def full_distribution(phase):
    return Counter(sum(phase[x] for x in L) for L in spaces)


rng = Random(20260827)
best = []
for trial in range(2000):
    anf = tuple(mask for mask in monomials if rng.randrange(2))
    phase = phase_from_anf(anf)
    values = restricted_sums(phase)
    best.append((len(values), anf, values))

# Maiorana--McFarland functions u dot pi(v) + g(v), for random permutations pi.
for trial in range(500):
    permutation = list(range(16))
    rng.shuffle(permutation)
    g = [rng.randrange(2) for _ in range(16)]
    phase = []
    for x in range(256):
        u, v = x & 15, x >> 4
        value = (bin(u & permutation[v]).count("1") + g[v]) & 1
        phase.append(1 if value == 0 else -1)
    values = restricted_sums(phase)
    best.append((len(values), ("MM", tuple(permutation), tuple(g)), values))

best.sort(key=lambda row: row[0])
print("spaces", len(spaces), "tested", len(best))
print("best early distinct counts", Counter(row[0] for row in best))
for count, description, early in best[:20]:
    phase = phase_from_anf(description) if description and description[0] != "MM" else None
    distribution = full_distribution(phase) if phase is not None and count <= 5 else None
    print(count, early, description, distribution)
