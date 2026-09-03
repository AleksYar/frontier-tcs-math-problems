from fractions import Fraction
from itertools import product


def classify(k):
    h = 2 ** (k - 1)
    q = 2 ** (k - 2)
    s = 2 ** k - 1
    solutions = set()
    # Prescribe the value at image rank zero and at each of the three image lines.
    for t0, t1, t2, t3 in product(range(3), repeat=4):
        w0 = Fraction(t0, s)
        weights = tuple(Fraction(t - (h - 1) * w0, h) for t in (t1, t2, t3))
        full = (q - 1) * w0 + q * sum(weights)
        if full.denominator == 1 and 0 <= full <= 2:
            solutions.add(((w0,) + weights, (t0, t1, t2, t3, int(full))))
    return sorted(solutions, key=str)


for k in (2, 3, 4, 5, 6):
    solutions = classify(k)
    print("k", k, "solutions", len(solutions))
    if k == 4:
        patterns = {solution[1] for solution in solutions}
        booleans = {p for p in patterns if set(p) <= {0, 1}}
        pair_sums = {tuple(a + b for a, b in zip(f, g)) for f in booleans for g in booleans}
        print("quotient Boolean patterns", len(booleans), "pair sums", len(pair_sums),
              "non-pair patterns", sorted(patterns - pair_sums))
        for solution in solutions:
            print(solution)
