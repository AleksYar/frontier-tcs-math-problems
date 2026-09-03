#!/usr/bin/env python3
"""Enumerate small fixed polyominoes and falsify-check all recurrence inequalities."""

from collections import defaultdict


PATTERN_ROWS = {
    "C": ("x.x", "xox", "xxx"),
    "D": ("x..", "xox", "xxx"),
    "E": ("xox", "xxx"),
    "F": (".o.", "xxx"),
    "G": ("xo.", "xxx"),
    "H": ("x..", "xo.", "xxx"),
    "P": ("oo.", "xxx"),
    "Q": ("xoo", "xxx"),
    "R": ("x...", "xoo.", "xxxx"),
    "S": ("x..", "xoo", "xxx"),
    "T": ("xoo.", "xxxx"),
    "U": (".oo.", "xxxx"),
    "V": ("xooo", "xxxx"),
    "W": ("x...", "xooo", "xxxx"),
    "X": ("xoox", "xxxx"),
    "Y": ("x...", "xoox", "xxxx"),
    "Z": ("x..x", "xoox", "xxxx"),
}


def parse_pattern(rows):
    height = len(rows)
    required, forbidden = [], []
    for row_number, row in enumerate(rows):
        y = height - 1 - row_number
        for x, symbol in enumerate(row):
            if symbol == "o":
                required.append((x, y))
            elif symbol == "x":
                forbidden.append((x, y))
    return tuple(required), tuple(forbidden)


PATTERNS = {name: parse_pattern(rows) for name, rows in PATTERN_ROWS.items()}
NEIGHBORS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def normalize(polyomino):
    min_x = min(x for x, _ in polyomino)
    min_y = min(y for _, y in polyomino)
    return frozenset((x - min_x, y - min_y) for x, y in polyomino)


def enumerate_polyominoes(max_n):
    levels = {1: {frozenset({(0, 0)})}}
    for n in range(2, max_n + 1):
        next_level = set()
        for polyomino in levels[n - 1]:
            boundary = set()
            for x, y in polyomino:
                for dx, dy in NEIGHBORS:
                    cell = (x + dx, y + dy)
                    if cell not in polyomino:
                        boundary.add(cell)
            for cell in boundary:
                next_level.add(normalize(polyomino | {cell}))
        levels[n] = next_level
    return levels


def occurrences(polyomino, pattern):
    required, forbidden = pattern
    anchor_x, anchor_y = required[0]
    total = 0
    for cell_x, cell_y in polyomino:
        dx, dy = cell_x - anchor_x, cell_y - anchor_y
        if all((x + dx, y + dy) in polyomino for x, y in required) and all(
            (x + dx, y + dy) not in polyomino for x, y in forbidden
        ):
            total += 1
    return total


def convolution2(values, left, right, total):
    return sum(values[left][i] * values[right][total - i] for i in range(1, total))


def convolution3(values, first, second, third, total):
    return sum(
        values[first][i] * values[second][j] * values[third][total - i - j]
        for i in range(1, total)
        for j in range(1, total - i)
    )


def value(values, name, n):
    return values[name].get(n, 0)


def recurrence_rhs(values, n):
    c2 = lambda a, b, total: convolution2(values, a, b, total)
    c3 = lambda a, b, c, total: convolution3(values, a, b, c, total)
    return {
        "C": value(values, "E", n - 1),
        "D": value(values, "G", n - 1),
        "E": value(values, "F", n - 1),
        "F": value(values, "G", n) + value(values, "P", n),
        "G": value(values, "E", n) + value(values, "Q", n),
        "H": value(values, "D", n) + value(values, "S", n),
        "U": c2("D", "H", n) + c2("S", "D", n) + c2("Y", "R", n)
             + c2("W", "Y", n) + c3("U", "Z", "Z", n),
        "T": value(values, "X", n) + value(values, "V", n),
        "P": c2("E", "H", n) + c2("Q", "D", n) + c2("X", "R", n)
             + c2("V", "Y", n) + c3("U", "Y", "Z", n),
        "Q": value(values, "G", n - 1) + c2("G", "E", n - 1)
             + value(values, "U", n - 2) + c2("T", "G", n - 2)
             + c2("R", "U", n - 2),
        "R": value(values, "Y", n) + value(values, "W", n),
        "S": value(values, "G", n - 1) + c2("E", "E", n - 1)
             + value(values, "T", n - 2) + c2("X", "G", n - 2)
             + c2("Y", "U", n - 2),
        "V": value(values, "S", n - 1) + c2("G", "G", n - 2)
             + c2("T", "E", n - 2) + c2("R", "T", n - 2),
        "W": value(values, "S", n - 1) + c2("E", "G", n - 2)
             + c2("X", "E", n - 2) + c2("Y", "T", n - 2),
        "X": value(values, "D", n - 1) + value(values, "G", n - 2)
             + value(values, "U", n - 2),
        "Y": value(values, "C", n - 1) + value(values, "G", n - 2)
             + value(values, "T", n - 2),
        "Z": value(values, "C", n - 1) + value(values, "E", n - 2)
             + value(values, "X", n - 2),
    }


def main():
    max_n = 10
    levels = enumerate_polyominoes(max_n)
    expected = (1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446)
    observed = tuple(len(levels[n]) for n in range(1, max_n + 1))
    assert observed == expected, (observed, expected)
    values = {name: defaultdict(int) for name in PATTERNS}
    for n, polyominoes in levels.items():
        for polyomino in polyominoes:
            for name, pattern in PATTERNS.items():
                values[name][n] += occurrences(polyomino, pattern)
        assert len(polyominoes) <= values["G"][n] <= n * len(polyominoes)
    for n in range(2, max_n + 1):
        rhs = recurrence_rhs(values, n)
        for name in PATTERNS:
            assert values[name][n] <= rhs[name], (
                name, n, values[name][n], rhs[name]
            )
    print(f"PASS: A(1..{max_n})={observed}")
    print("PASS: A(n) <= G(n) <= n A(n) for every tested n")
    print(f"PASS: all 17 recurrence inequalities for every 2 <= n <= {max_n}")


if __name__ == "__main__":
    main()
