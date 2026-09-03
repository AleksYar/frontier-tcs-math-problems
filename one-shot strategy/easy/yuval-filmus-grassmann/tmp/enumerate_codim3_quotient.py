from fractions import Fraction
from itertools import product


def span(vectors):
    result = {0}
    for v in vectors:
        result |= {x ^ v for x in tuple(result)}
    return frozenset(result)


subspaces = sorted({span(gens) for gens in product(range(8), repeat=3)}, key=lambda R: (len(R), tuple(R)))
assert len(subspaces) == 16


def invert(matrix):
    n = len(matrix)
    work = [list(map(Fraction, row)) + [Fraction(i == j) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row != col and work[row][col]:
                scale = work[row][col]
                work[row] = [x - scale * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def rank(rows):
    work = [list(map(Fraction, row)) for row in rows]
    pivots = 0
    for col in range(8):
        pivot = next((i for i in range(pivots, len(work)) if work[i][col]), None)
        if pivot is None:
            continue
        work[pivots], work[pivot] = work[pivot], work[pivots]
        scale = work[pivots][col]
        work[pivots] = [x / scale for x in work[pivots]]
        for i in range(len(work)):
            if i != pivots and work[i][col]:
                scale = work[i][col]
                work[i] = [x - scale * y for x, y in zip(work[i], work[pivots])]
        pivots += 1
    return pivots


def distributions(k):
    rows = []
    for R in subspaces:
        r = len(R).bit_length() - 1
        fiber = 2 ** (k - r)
        rows.append(tuple((fiber - 1 if z == 0 else fiber) if z in R else 0 for z in range(8)))
    return rows


for k in (3, 4, 5, 6):
    rows = distributions(k)
    basis_indices = []
    basis = []
    for i, row in enumerate(rows):
        if rank(basis + [row]) > len(basis):
            basis.append(row)
            basis_indices.append(i)
        if len(basis) == 8:
            break
    inverse = invert(basis)
    solutions = {}
    for values in product(range(3), repeat=8):
        weights = tuple(sum(inverse[i][j] * values[j] for j in range(8)) for i in range(8))
        pattern = tuple(sum(w * x for w, x in zip(weights, row)) for row in rows)
        if all(x.denominator == 1 and 0 <= x <= 2 for x in pattern):
            solutions[tuple(int(x) for x in pattern)] = weights
    booleans = {p for p in solutions if set(p) <= {0, 1}}
    pair_sums = {tuple(a + b for a, b in zip(f, g)) for f in booleans for g in booleans}
    print("k", k, "solutions", len(solutions), "booleans", len(booleans),
          "pair sums", len(pair_sums), "non-pair", len(set(solutions) - pair_sums))
    if k == 4:
        summary = {}
        for p in set(solutions) - pair_sums:
            key = tuple(p.count(i) for i in range(3))
            summary[key] = summary.get(key, 0) + 1
        print("non-pair summary", summary)
        for p in sorted(set(solutions) - pair_sums)[:10]:
            print("exception", p, solutions[p])
