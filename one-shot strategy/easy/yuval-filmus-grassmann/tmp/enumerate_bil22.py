from fractions import Fraction
from itertools import product


def rank2x2(x):
    # Bits are entries (00, 01, 10, 11), packed row-major.
    a, b, c, d = ((x >> i) & 1 for i in range(4))
    if x == 0:
        return 0
    return 2 if (a * d ^ b * c) else 1


frequencies = [x for x in range(16) if rank2x2(x) <= 1]
assert len(frequencies) == 10


def parity(x):
    return bin(x).count("1") & 1


evaluation = [
    [Fraction((-1) ** parity(a & m)) for m in frequencies]
    for a in range(16)
]


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


# Greedily select ten evaluation points giving independent rows.
basis_points = []
basis_rows = []
rank = 0
for a, row in enumerate(evaluation):
    candidate = basis_rows + [row]
    # Rational row reduction solely to get the rank.
    work = [r[:] for r in candidate]
    pivots = 0
    for col in range(10):
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
    if pivots > rank:
        basis_points.append(a)
        basis_rows.append(row)
        rank = pivots
    if rank == 10:
        break

inverse = invert(basis_rows)
reconstruction = []
for row in evaluation:
    reconstruction.append([
        sum(row[j] * inverse[j][i] for j in range(10))
        for i in range(10)
    ])

functions = []
for values in product(range(3), repeat=10):
    f = tuple(sum(reconstruction[a][i] * values[i] for i in range(10)) for a in range(16))
    if all(x.denominator == 1 and 0 <= x <= 2 for x in f):
        functions.append(tuple(int(x) for x in f))

booleans = [f for f in functions if set(f) <= {0, 1}]
pair_sums = {tuple(a + b for a, b in zip(f, g)) for f in booleans for g in booleans}

print("frequencies", frequencies)
print("basis points", basis_points)
print("ternary", len(functions))
print("boolean", len(booleans))
print("pair sums", len(pair_sums))
print("non-pair", len(set(functions) - pair_sums))

# Tabulate Fourier-support sizes and value distributions for the exceptional functions.
def fourier(f):
    return tuple(sum(f[a] * (-1) ** parity(a & m) for a in range(16)) for m in frequencies)

summary = {}
for f in set(functions) - pair_sums:
    key = (tuple(f.count(i) for i in range(3)), sum(x != 0 for x in fourier(f)[1:]))
    summary[key] = summary.get(key, 0) + 1
print("exception summary", sorted(summary.items()))
if set(functions) - pair_sums:
    representative = min(set(functions) - pair_sums)
    print("representative", representative)
    print("representative Fourier numerators", fourier(representative))

# Spectral catalogs used for extending a 2-by-2 slice by one more column.
def left_vector(m):
    columns = (((m >> 0) & 1) | (((m >> 2) & 1) << 1),
               ((m >> 1) & 1) | (((m >> 3) & 1) << 1))
    return next(x for x in columns if x)

groups = {r: tuple(i for i, m in enumerate(frequencies[1:], start=1) if left_vector(m) == r)
          for r in (1, 2, 3)}
spectra = {f: fourier(f) for f in functions}
print("left groups", groups)
for r, indices in groups.items():
    triples = {tuple(spectra[f][i] for i in indices) for f in functions}
    print("group", r, "distinct triples", len(triples))

def grouped_spectrum(f):
    spectrum = spectra[f]
    return tuple(tuple(spectrum[i] for i in groups[r]) for r in (1, 2, 3))

C = {grouped_spectrum(f) for f in functions}
by_first = {}
by_second = {}
for row in C:
    by_first.setdefault(row[0], []).append(row)
    by_second.setdefault(row[1], []).append(row)

box_count = 0
boxes_touching_exception = 0
exception_spectra = {grouped_spectrum(f) for f in set(functions) - pair_sums}
example_box = None
for A in C:
    # S1=(B1,A2,B3), S2=(A1,B2,B3), S3=(B1,B2,A3).
    for S1 in by_second[A[1]]:
        for S2 in by_first[A[0]]:
            if S1[2] != S2[2]:
                continue
            S3 = (S1[0], S2[1], A[2])
            if S3 in C:
                box_count += 1
                if any(x in exception_spectra for x in (A, S1, S2, S3)):
                    boxes_touching_exception += 1
                    if example_box is None:
                        example_box = (A, S1, S2, S3)
print("nonconstant spectra", len(C))
print("spectral boxes", box_count)
print("boxes touching exceptional 2x2 slice", boxes_touching_exception)
print("example exceptional box", example_box)
