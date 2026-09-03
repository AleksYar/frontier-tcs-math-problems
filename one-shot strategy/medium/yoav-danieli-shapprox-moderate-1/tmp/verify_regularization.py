#!/usr/bin/env python3
"""Verify loop-padding and perfect-matching regularization on small graphs."""

from itertools import combinations
import random

from directed_reduction import cycle_rank, strongly_connected
from search_graphs import invariants


def connected(adj):
    n = len(adj)
    seen = 1
    todo = 1
    while todo:
        b = todo & -todo
        todo ^= b
        u = b.bit_length() - 1
        new = adj[u] & ~seen
        seen |= new
        todo |= new
    return seen == (1 << n) - 1


def perfect_matching(counts):
    """One matching in a positive-support bipartite multigraph."""
    n = len(counts)
    right_to_left = [-1] * n

    def augment(u, seen):
        for v in range(n):
            if counts[u][v] == 0 or seen[v]:
                continue
            seen[v] = True
            if right_to_left[v] < 0 or augment(right_to_left[v], seen):
                right_to_left[v] = u
                return True
        return False

    for u in range(n):
        assert augment(u, [False] * n)
    perm = [-1] * n
    for v, u in enumerate(right_to_left):
        perm[u] = v
    return perm


def regularize(adj):
    n = len(adj)
    popcount = lambda x: bin(x).count("1")
    delta = max(popcount(a) for a in adj)
    degree = delta + 1
    counts = [[0] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if (adj[u] >> v) & 1:
                counts[u][v] += 1
        counts[u][u] += degree - popcount(adj[u])

    perms = []
    for _ in range(degree):
        p = perfect_matching(counts)
        assert sorted(p) == list(range(n))
        perms.append(p)
        for u, v in enumerate(p):
            counts[u][v] -= 1
            assert counts[u][v] >= 0
    assert not any(any(row) for row in counts)

    digraph = [0] * n
    for p in perms:
        for u, v in enumerate(p):
            digraph[u] |= 1 << v
    return perms, digraph


def expected_digraph(adj):
    n = len(adj)
    return [adj[u] | (1 << u) for u in range(n)]


if __name__ == "__main__":
    rng = random.Random(2718)
    checked = 0
    for n in range(2, 8):
        pairs = list(combinations(range(n), 2))
        for _ in range(40):
            while True:
                adj = [0] * n
                for u, v in pairs:
                    if rng.random() < 0.4:
                        adj[u] |= 1 << v
                        adj[v] |= 1 << u
                if connected(adj):
                    break
            perms, digraph = regularize(adj)
            assert digraph == expected_digraph(adj)
            assert strongly_connected(digraph)
            td = invariants(adj)[0]
            assert cycle_rank(digraph) == td
            # Every word in the letters is a permutation, so for any target f
            # a word taking p to f cannot also take a distinct q to f.
            for p in perms:
                assert len(set(p)) == n
            checked += 1
    print({"verified_instances": checked})
