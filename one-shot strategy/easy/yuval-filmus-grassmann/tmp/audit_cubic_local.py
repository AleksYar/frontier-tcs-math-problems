#!/usr/bin/env python3
"""Check the exact local cubic identity on all 3-spaces of F_2^8."""

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


def gaussian_two(m):
    return ((2 ** m - 1) * (2 ** (m - 1) - 1)) // 3


def local_cubic(T, c, k):
    points = tuple(x for x in T if x)
    lines = set()
    for a, b in combinations(points, 2):
        lines.add(tuple(sorted((a, b, a ^ b))))

    point_cubes = {p: c[p] ** 3 for p in points}
    B = {}
    D = {}
    for line in lines:
        s = sum(c[p] for p in line)
        B[line] = s ** 3 - sum(point_cubes[p] for p in line)
        D[line] = s ** 2 - sum(c[p] ** 2 for p in line)

    total = sum(c[p] for p in points)
    top = total ** 3 - sum(B.values()) - sum(point_cubes.values())
    line_lift = sum(B[line] - 3 * D[line] for line in lines) / (2 ** (k - 2) - 1)
    point_lift = sum(
        c[p] ** 3 - 3 * c[p] ** 2 + 2 * c[p] for p in points
    ) / gaussian_two(k - 1)
    return top + line_lift + point_lift


def main():
    n, k = 8, 4
    # The affine codimension-two core A(x)=(x_0,x_1)=(1,1).
    c = [Fraction(0) for _ in range(1 << n)]
    for x in range(1, 1 << n):
        if (x & 3) == 3:
            c[x] = Fraction(1, 4)
    spaces = list(rref_subspaces(n, 3))
    bad = [(T, local_cubic(T, c, k)) for T in spaces if local_cubic(T, c, k)]
    print('3-spaces', len(spaces), 'bad core identities', len(bad), bad[:1])

    # A deliberately invalid coefficient vector must be rejected locally.
    c_bad = list(c)
    c_bad[1] += Fraction(1, 7)
    bad2 = sum(bool(local_cubic(T, c_bad, k)) for T in spaces)
    print('bad identities after perturbing one coefficient', bad2)


if __name__ == '__main__':
    main()
