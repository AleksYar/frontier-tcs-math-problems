#!/usr/bin/env python3
"""Exhaustively test normalized matching for the small polyomino cover levels."""

from collections import deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def canon(cells):
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def extensions(poly):
    cells = set(poly)
    return {
        canon(cells | {(x + dx, y + dy)})
        for x, y in cells
        for dx, dy in DIRS
        if (x + dx, y + dy) not in cells
    }


levels = {1: {((0, 0),)}}
for n in range(1, 10):
    levels[n + 1] = set().union(*(extensions(p) for p in levels[n]))

for n in range(1, 5):
    lower = sorted(levels[n])
    upper = sorted(levels[n + 1])
    upper_index = {p: i for i, p in enumerate(upper)}
    neighborhoods = []
    for poly in lower:
        mask = 0
        for child in extensions(poly):
            mask |= 1 << upper_index[child]
        neighborhoods.append(mask)

    # Dynamic programming over all subsets: union_mask[S] is the upper shadow.
    union_mask = [0] * (1 << len(lower))
    worst = None
    for subset in range(1, 1 << len(lower)):
        bit = subset & -subset
        i = bit.bit_length() - 1
        union_mask[subset] = union_mask[subset ^ bit] | neighborhoods[i]
        s = bin(subset).count("1")
        g = bin(union_mask[subset]).count("1")
        # NMP is g/|upper| >= s/|lower|, i.e. g*L >= s*U.
        defect = g * len(lower) - s * len(upper)
        key = (defect, g, -s)
        if worst is None or key < worst[0]:
            worst = (key, subset, g, s)
    key, subset, g, s = worst
    witness = [lower[i] for i in range(len(lower)) if subset >> i & 1]
    print(
        n,
        "sizes",
        (len(lower), len(upper)),
        "min-defect",
        key[0],
        "subset-size",
        s,
        "shadow-size",
        g,
        "witness",
        witness if key[0] < 0 else None,
    )


class Dinic:
    def __init__(self, n):
        self.g = [[] for _ in range(n)]

    def edge(self, u, v, cap):
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def flow(self, source, sink):
        total = 0
        while True:
            level = [-1] * len(self.g)
            level[source] = 0
            queue = deque([source])
            while queue:
                u = queue.popleft()
                for v, cap, _ in self.g[u]:
                    if cap and level[v] < 0:
                        level[v] = level[u] + 1
                        queue.append(v)
            if level[sink] < 0:
                return total, level
            cursor = [0] * len(self.g)

            def send(u, amount):
                if u == sink:
                    return amount
                while cursor[u] < len(self.g[u]):
                    edge = self.g[u][cursor[u]]
                    v, cap, reverse = edge
                    if cap and level[v] == level[u] + 1:
                        pushed = send(v, min(amount, cap))
                        if pushed:
                            edge[1] -= pushed
                            self.g[v][reverse][1] += pushed
                            return pushed
                    cursor[u] += 1
                return 0

            while True:
                pushed = send(source, 10 ** 30)
                if not pushed:
                    break
                total += pushed


for n in range(1, 10):
    lower = sorted(levels[n])
    upper = sorted(levels[n + 1])
    upper_index = {p: i for i, p in enumerate(upper)}
    source = 0
    lower_start = 1
    upper_start = lower_start + len(lower)
    sink = upper_start + len(upper)
    network = Dinic(sink + 1)
    for i, poly in enumerate(lower):
        network.edge(source, lower_start + i, len(upper))
        for child in extensions(poly):
            network.edge(lower_start + i, upper_start + upper_index[child], 10 ** 30)
    for j in range(len(upper)):
        network.edge(upper_start + j, sink, len(lower))
    value, reachable_levels = network.flow(source, sink)
    target = len(lower) * len(upper)
    if value == target:
        print("flow", n, "sizes", (len(lower), len(upper)), "NMP", True)
    else:
        witness = [
            lower[i]
            for i in range(len(lower))
            if reachable_levels[lower_start + i] >= 0
        ]
        shadow = set().union(*(extensions(poly) for poly in witness))
        defect = len(shadow) * len(lower) - len(witness) * len(upper)
        print(
            "flow", n, "sizes", (len(lower), len(upper)), "NMP", False,
            "defect", defect, "subset-size", len(witness), "shadow-size", len(shadow),
            "witness", witness,
        )
