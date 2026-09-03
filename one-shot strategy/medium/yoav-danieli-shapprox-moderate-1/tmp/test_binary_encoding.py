#!/usr/bin/env python3
"""Exact small tests for the two-permutation alphabet-control encoding."""

from itertools import combinations
import random

from directed_reduction import cycle_rank, strongly_connected
from search_graphs import invariants
from verify_regularization import connected, regularize


def binary_encode(perms):
    degree = len(perms)
    n = len(perms[0])
    size = degree * n
    digraph = [0] * size

    def state(v, layer):
        return degree * v + layer

    for v in range(n):
        for layer in range(degree):
            # Control-cycle permutation a.
            digraph[state(v, layer)] |= 1 << state(v, (layer + 1) % degree)
            # Parallel data permutation b.
            digraph[state(v, layer)] |= 1 << state(perms[layer][v], layer)
    return digraph


def main():
    rng = random.Random(9901)
    results = []
    for n in range(2, 5):
        pairs = list(combinations(range(n), 2))
        for _ in range(30):
            while True:
                adj = [0] * n
                for u, v in pairs:
                    if rng.random() < 0.45:
                        adj[u] |= 1 << v
                        adj[v] |= 1 << u
                if connected(adj):
                    break
            perms, _ = regularize(adj)
            encoded = binary_encode(perms)
            assert strongly_connected(encoded)
            td = invariants(adj)[0]
            rank = cycle_rank(encoded)
            results.append((n, len(perms), td, rank))
    print(results)
    print({"max_rank_minus_td": max(rank - td for _, _, td, rank in results),
           "max_ratio": max(rank / td for _, _, td, rank in results)})


if __name__ == "__main__":
    main()
