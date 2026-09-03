#!/usr/bin/env python3
"""Modular rank of the local-cubic Jacobian at the J_2(8,4) coset core."""

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


P = 1000003


def inv(x):
    return pow(x % P, P - 2, P)


def gradient(T, c):
    points = tuple(x for x in T if x)
    point_set = set(points)
    lines = set()
    for a, b in combinations(points, 2):
        lines.add(tuple(sorted((a, b, a ^ b))))
    total = sum(c[p] for p in points) % P
    out = {}
    a_inv = inv(3)  # 2^(k-2)-1 for k=4
    b_inv = inv(7)  # [k-1 choose 2]_2 for k=4
    for p in points:
        cp = c[p]
        d_top = 3 * total * total - 3 * cp * cp
        d_line_lift = 0
        for line in lines:
            if p in line:
                s = sum(c[q] for q in line) % P
                dB = 3 * s * s - 3 * cp * cp
                dD = 2 * s - 2 * cp
                d_top -= dB
                d_line_lift += dB - 3 * dD
        d_point = 3 * cp * cp - 6 * cp + 2
        out[p - 1] = (d_top + a_inv * d_line_lift + b_inv * d_point) % P
    assert len(point_set) == 7
    return out


def main():
    quarter = inv(4)
    c = [0] * 256
    for x in range(1, 256):
        if (x & 3) == 3:
            c[x] = quarter

    basis = {}
    checked = 0
    for T in rref_subspaces(8, 3):
        checked += 1
        sparse = gradient(T, c)
        row = [0] * 255
        for j, value in sparse.items():
            row[j] = value
        while True:
            pivot = next((j for j, value in enumerate(row) if value), None)
            if pivot is None:
                break
            if pivot not in basis:
                scale = inv(row[pivot])
                row = [(x * scale) % P for x in row]
                basis[pivot] = row
                break
            scale = row[pivot]
            old = basis[pivot]
            row = [(x - scale * y) % P for x, y in zip(row, old)]
        if len(basis) == 255:
            break
    print('prime', P, 'rows checked', checked, 'Jacobian rank', len(basis))


if __name__ == '__main__':
    main()
