#!/usr/bin/env python3
"""Exhaustive checks of candidate treedepth recurrences on small graphs."""

from functools import lru_cache
from itertools import combinations
import argparse
import random


def popcount(mask):
    return bin(mask).count("1")


def components(adj, mask):
    out = []
    unseen = mask
    while unseen:
        bit = unseen & -unseen
        unseen ^= bit
        comp = bit
        frontier = bit
        while frontier:
            vbit = frontier & -frontier
            frontier ^= vbit
            v = vbit.bit_length() - 1
            nbr = adj[v] & unseen
            unseen ^= nbr
            frontier |= nbr
            comp |= nbr
        out.append(comp)
    return out


def connected(adj, mask):
    return len(components(adj, mask)) <= 1


def invariants(adj):
    n = len(adj)
    full = (1 << n) - 1

    @lru_cache(None)
    def td(mask):
        if not mask:
            return 0
        cs = components(adj, mask)
        if len(cs) > 1:
            return max(td(c) for c in cs)
        return 1 + min(td(mask ^ (1 << v)) for v in range(n) if mask >> v & 1)

    @lru_cache(None)
    def centroid_best(mask):
        """Among minimum-largest-component vertices, take best recursive tie."""
        if not mask:
            return 0
        cs = components(adj, mask)
        if len(cs) > 1:
            return max(centroid_best(c) for c in cs)
        scores = []
        for v in range(n):
            if not (mask >> v & 1):
                continue
            rest = mask ^ (1 << v)
            parts = components(adj, rest)
            largest = max((popcount(p) for p in parts), default=0)
            height = 1 + max((centroid_best(p) for p in parts), default=0)
            scores.append((largest, height, v))
        min_largest = min(x[0] for x in scores)
        return min(x[1] for x in scores if x[0] == min_largest)

    @lru_cache(None)
    def centroid_worst(mask):
        """Among minimum-largest-component vertices, take worst recursive tie."""
        if not mask:
            return 0
        cs = components(adj, mask)
        if len(cs) > 1:
            return max(centroid_worst(c) for c in cs)
        scores = []
        for v in range(n):
            if not (mask >> v & 1):
                continue
            rest = mask ^ (1 << v)
            parts = components(adj, rest)
            largest = max((popcount(p) for p in parts), default=0)
            height = 1 + max((centroid_worst(p) for p in parts), default=0)
            scores.append((largest, height, v))
        min_largest = min(x[0] for x in scores)
        return max(x[1] for x in scores if x[0] == min_largest)

    @lru_cache(None)
    def balanced_cost(mask):
        """Best recursive cost using arbitrary 1/2-balanced vertex separators."""
        if not mask:
            return 0
        cs = components(adj, mask)
        if len(cs) > 1:
            return max(balanced_cost(c) for c in cs)
        size = popcount(mask)
        best = size
        sub = mask
        while sub:
            remain = mask ^ sub
            parts = components(adj, remain)
            if all(2 * popcount(p) <= size for p in parts):
                cost = popcount(sub) + max((balanced_cost(p) for p in parts), default=0)
                best = min(best, cost)
            sub = (sub - 1) & mask
        return best

    return td(full), centroid_best(full), centroid_worst(full), balanced_cost(full)


def graph6ish(adj):
    return ";".join(f"{v}:" + ",".join(str(w) for w in range(len(adj)) if adj[v] >> w & 1)
                    for v in range(len(adj)))


def exhaustive(n):
    pairs = list(combinations(range(n), 2))
    maxima = {"centroid_best": (0.0, None), "centroid_worst": (0.0, None),
              "balanced_cost": (0.0, None)}
    connected_count = 0
    for edge_mask in range(1 << len(pairs)):
        adj = [0] * n
        for i, (u, v) in enumerate(pairs):
            if edge_mask >> i & 1:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        if not connected(adj, (1 << n) - 1):
            continue
        connected_count += 1
        vals = invariants(adj)
        opt = vals[0]
        for name, val in zip(list(maxima), vals[1:]):
            ratio = val / opt
            if ratio > maxima[name][0]:
                maxima[name] = (ratio, (vals, graph6ish(adj)))
    print({"n": n, "connected_graphs": connected_count, "maxima": maxima})


def random_search(n, trials, seed):
    random.seed(seed)
    maxima = {"centroid_best": (0.0, None), "centroid_worst": (0.0, None),
              "balanced_cost": (0.0, None)}
    for _ in range(trials):
        while True:
            p = random.random()
            adj = [0] * n
            for u, v in combinations(range(n), 2):
                if random.random() < p:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
            if connected(adj, (1 << n) - 1):
                break
        vals = invariants(adj)
        opt = vals[0]
        for name, val in zip(list(maxima), vals[1:]):
            ratio = val / opt
            if ratio > maxima[name][0]:
                maxima[name] = (ratio, (vals, graph6ish(adj)))
    print({"n": n, "trials": trials, "seed": seed, "maxima": maxima})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--random", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    if args.random:
        random_search(args.n, args.random, args.seed)
    else:
        exhaustive(args.n)
