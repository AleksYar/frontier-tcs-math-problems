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


def rank(rows):
    work = [row[:] for row in rows]
    pivots = 0
    for col in range(len(rows[0])):
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


def invert(matrix):
    n = len(matrix)
    work = [row[:] + [Fraction(i == j) for j in range(n)] for i, row in enumerate(matrix)]
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


spaces = list(rref_subspaces(8, 4))
distributions = sorted({
    tuple(sum(1 for x in L if x and bin(x).count("1") == weight) for weight in range(1, 9))
    for L in spaces
})
assert len(distributions) == 98

basis = []
for distribution in distributions:
    candidate = basis + [[Fraction(x) for x in distribution]]
    if rank(candidate) > len(basis):
        basis = candidate
    if len(basis) == 8:
        break
inverse = invert(basis)

solutions = set()
for values in product(range(3), repeat=8):
    coefficients = tuple(sum(inverse[i][j] * values[j] for j in range(8)) for i in range(8))
    attained = tuple(sum(c * x for c, x in zip(coefficients, distribution)) for distribution in distributions)
    if all(x.denominator == 1 and 0 <= x <= 2 for x in attained):
        solutions.add((coefficients, tuple(sorted(set(int(x) for x in attained)))))

print("spaces", len(spaces))
print("distributions", len(distributions))
print("basis", basis)
print("solutions", len(solutions))
for solution in sorted(solutions, key=str):
    print(solution)
