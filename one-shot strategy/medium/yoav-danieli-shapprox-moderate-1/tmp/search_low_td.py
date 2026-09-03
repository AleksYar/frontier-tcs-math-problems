#!/usr/bin/env python3
"""Search low-treedepth graphs for bad centroid-decomposition behavior."""

from functools import lru_cache
import argparse
import random


def components(adj, mask):
    result = []
    unseen = mask
    while unseen:
        seed = unseen & -unseen
        unseen ^= seed
        comp = seed
        frontier = seed
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            v = bit.bit_length() - 1
            nbrs = adj[v] & unseen
            unseen ^= nbrs
            frontier |= nbrs
            comp |= nbrs
        result.append(comp)
    return result


def heights(adj):
    n = len(adj)

    @lru_cache(None)
    def td(mask):
        if not mask:
            return 0
        parts = components(adj, mask)
        if len(parts) > 1:
            return max(td(part) for part in parts)
        return 1 + min(td(mask ^ (1 << v)) for v in range(n) if mask & (1 << v))

    @lru_cache(None)
    def centroid(mask):
        if not mask:
            return 0
        parts = components(adj, mask)
        if len(parts) > 1:
            return max(centroid(part) for part in parts)
        best_balance = n + 1
        best_height = n + 1
        for v in range(n):
            if not mask & (1 << v):
                continue
            rest = components(adj, mask ^ (1 << v))
            balance = max((bin(part).count("1") for part in rest), default=0)
            height = 1 + max((centroid(part) for part in rest), default=0)
            if balance < best_balance or (balance == best_balance and height < best_height):
                best_balance, best_height = balance, height
        return best_height

    full = (1 << n) - 1
    return td(full), centroid(full)


def random_forest(n, height):
    parent = [-1] * n
    depth = [0] * n
    for v in range(1, n):
        eligible = [u for u in range(v) if depth[u] + 1 < height]
        if eligible:
            parent[v] = random.choice(eligible)
            depth[v] = depth[parent[v]] + 1
    return parent


def random_subgraph_of_closure(parent, probability):
    n = len(parent)
    ancestors = [set() for _ in range(n)]
    for v in range(n):
        u = parent[v]
        while u >= 0:
            ancestors[v].add(u)
            u = parent[u]
    adj = [0] * n
    for v in range(n):
        for u in ancestors[v]:
            if random.random() < probability:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    return adj


def connected(adj):
    return len(components(adj, (1 << len(adj)) - 1)) == 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("height", type=int)
    parser.add_argument("trials", type=int)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    random.seed(args.seed)
    best = (0.0, None)
    checked = 0
    for _ in range(args.trials):
        parent = random_forest(args.n, args.height)
        adj = random_subgraph_of_closure(parent, random.uniform(0.15, 1.0))
        if not connected(adj):
            continue
        checked += 1
        exact, cent = heights(adj)
        ratio = cent / exact
        if ratio > best[0]:
            best = (ratio, (exact, cent, parent, adj))
    print({"checked": checked, "best": best})


if __name__ == "__main__":
    main()
