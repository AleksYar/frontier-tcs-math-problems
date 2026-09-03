#!/usr/bin/env python3
"""Search for symmetric cell-transfer failures between rooted animals."""

from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def connected(cells):
    if not cells:
        return False
    seen = {next(iter(cells))}
    queue = deque(seen)
    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRS:
            z = x + dx, y + dy
            if z in cells and z not in seen:
                seen.add(z)
                queue.append(z)
    return len(seen) == len(cells)


def extensions(poly):
    return {
        frozenset(set(poly) | {(x + dx, y + dy)})
        for x, y in poly
        for dx, dy in DIRS
        if (x + dx, y + dy) not in poly
    }


levels = {1: {frozenset({(0, 0)})}}
for n in range(1, 8):
    levels[n + 1] = set().union(*(extensions(poly) for poly in levels[n]))
    print(n + 1, len(levels[n + 1]))

for n in range(2, 9):
    witness = None
    for xset in levels[n]:
        removable = {
            x for x in xset if x != (0, 0) and connected(set(xset) - {x})
        }
        for yset in levels[n]:
            if xset == yset:
                continue
            if not any(
                x in removable
                and any((x[0] + dx, x[1] + dy) in yset for dx, dy in DIRS)
                for x in xset - yset
            ):
                witness = xset, yset
                break
        if witness:
            break
    print("symmetric-transfer", n, witness is None, witness)
    if witness:
        break
