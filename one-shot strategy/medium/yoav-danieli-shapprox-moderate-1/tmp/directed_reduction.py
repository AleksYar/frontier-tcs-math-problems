#!/usr/bin/env python3
"""Exact checks for the two-copy hub reduction to permutation digraphs."""

from functools import lru_cache
from itertools import product
import random


def sccs(adj, mask):
    n = len(adj)
    rev = [0] * n
    for u in range(n):
        for v in range(n):
            if (adj[u] >> v) & 1:
                rev[v] |= 1 << u

    def reach(start, edges):
        seen = 0
        todo = 1 << start
        while todo:
            b = todo & -todo
            todo ^= b
            if seen & b:
                continue
            seen |= b
            v = b.bit_length() - 1
            todo |= edges[v] & mask & ~seen
        return seen

    out = []
    unseen = mask
    while unseen:
        b = unseen & -unseen
        v = b.bit_length() - 1
        comp = reach(v, adj) & reach(v, rev)
        out.append(comp)
        unseen &= ~comp
    return out


def cycle_rank(adj):
    n = len(adj)

    @lru_cache(None)
    def rank(mask):
        if not mask:
            return 0
        cs = sccs(adj, mask)
        if len(cs) > 1:
            return max(rank(c) for c in cs)
        # A singleton SCC is nontrivial exactly when its vertex has a loop.
        if mask & (mask - 1) == 0:
            v = mask.bit_length() - 1
            return int(bool(adj[v] & mask))
        return 1 + min(rank(mask ^ (1 << v)) for v in range(n) if mask >> v & 1)

    return rank((1 << n) - 1)


def hub_reduction(adj):
    """Underlying simple digraph of identity plus all 3-cycle permutations."""
    n = len(adj)
    h = 2 * n
    out = [0] * (2 * n + 1)
    for v in range(2 * n + 1):
        out[v] |= 1 << v  # the identity permutation letter
    for copy in range(2):
        off = copy * n
        for u in range(n):
            for v in range(n):
                if u != v and (adj[u] >> v) & 1:
                    uu, vv = off + u, off + v
                    out[uu] |= 1 << vv
                    out[vv] |= 1 << h
                    out[h] |= 1 << uu
                    # Every other state is fixed by this particular letter;
                    # those arcs are already represented by the identity loops.
    return out


def strongly_connected(adj):
    return len(sccs(adj, (1 << len(adj)) - 1)) == 1


def random_strong(n, rng):
    # Start with a directed n-cycle, then add arbitrary arcs.
    adj = [0] * n
    for u in range(n):
        adj[u] |= 1 << ((u + 1) % n)
    for u, v in product(range(n), repeat=2):
        if u != v and rng.random() < 0.3:
            adj[u] |= 1 << v
    return adj


if __name__ == "__main__":
    rng = random.Random(193)
    for n in range(2, 5):
        for trial in range(20):
            g = random_strong(n, rng)
            h = hub_reduction(g)
            rg, rh = cycle_rank(g), cycle_rank(h)
            assert strongly_connected(h)
            assert rh == rg + 2, (n, trial, rg, rh)
            print(n, trial, rg, rh)
