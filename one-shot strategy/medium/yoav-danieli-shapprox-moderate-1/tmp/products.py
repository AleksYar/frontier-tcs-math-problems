#!/usr/bin/env python3
"""Check whether standard graph products give controlled treedepth amplification."""

from search_graphs import invariants


def make(n, edges):
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def product(a, b, kind):
    n, m = len(a), len(b)
    out = [0] * (n * m)
    for u in range(n):
        for x in range(m):
            i = u * m + x
            for v in range(n):
                for y in range(m):
                    if i == v * m + y:
                        continue
                    guv = bool(a[u] >> v & 1)
                    hxy = bool(b[x] >> y & 1)
                    if kind == "lex":
                        edge = guv or (u == v and hxy)
                    elif kind == "strong":
                        edge = ((u == v or guv) and (x == y or hxy))
                    elif kind == "cartesian":
                        edge = (u == v and hxy) or (x == y and guv)
                    elif kind == "tensor":
                        edge = guv and hxy
                    else:
                        raise ValueError(kind)
                    if edge:
                        out[i] |= 1 << (v * m + y)
    return out


graphs = {
    "K2": make(2, [(0, 1)]),
    "I2": make(2, []),
    "P3": make(3, [(0, 1), (1, 2)]),
    "K3": make(3, [(0, 1), (1, 2), (0, 2)]),
    "S3": make(4, [(0, 1), (0, 2), (0, 3)]),
}

for aname, a in graphs.items():
    for bname, b in graphs.items():
        if len(a) * len(b) > 12:
            continue
        ta = invariants(a)[0]
        tb = invariants(b)[0]
        vals = []
        for kind in ("lex", "strong", "cartesian", "tensor"):
            p = product(a, b, kind)
            vals.append((kind, invariants(p)[0]))
        print(aname, ta, bname, tb, "product", ta * tb, vals)
