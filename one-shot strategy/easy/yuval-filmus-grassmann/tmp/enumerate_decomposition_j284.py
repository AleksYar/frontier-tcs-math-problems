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


spaces = list(rref_subspaces(8, 4))
U = set(range(1, 16))
W = {x << 4 for x in range(1, 16)}
distributions = sorted({
    (sum(x in U for x in L), sum(x in W for x in L),
     sum(bool(x) and x not in U and x not in W for x in L))
    for L in spaces
})

basis = []
for row in distributions:
    determinant = (row[0] * (basis[0][1] * basis[1][2] - basis[0][2] * basis[1][1])
                   - row[1] * (basis[0][0] * basis[1][2] - basis[0][2] * basis[1][0])
                   + row[2] * (basis[0][0] * basis[1][1] - basis[0][1] * basis[1][0])) if len(basis) == 2 else None
    if len(basis) < 2 or determinant:
        basis.append(row)
    if len(basis) == 3:
        break
inverse = invert(basis)

solutions = set()
for values in product(range(3), repeat=3):
    coefficients = tuple(sum(inverse[i][j] * values[j] for j in range(3)) for i in range(3))
    attained = tuple(sum(c * x for c, x in zip(coefficients, row)) for row in distributions)
    if all(x.denominator == 1 and 0 <= x <= 2 for x in attained):
        solutions.add((coefficients, tuple(sorted(set(int(x) for x in attained)))))

print("distribution count", len(distributions), "distributions", distributions)
print("basis", basis)
print("solutions", len(solutions))
for solution in sorted(solutions, key=str):
    print(solution)
