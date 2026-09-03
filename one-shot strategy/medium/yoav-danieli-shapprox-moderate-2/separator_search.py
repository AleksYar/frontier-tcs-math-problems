#!/usr/bin/env python3
"""Exhaustive small-graph falsification for treedepth separator heuristics."""

from functools import lru_cache
from itertools import combinations


def popcount(x: int) -> int:
    return bin(x).count("1")


def analyze(n: int, edge_bits: int):
    adj = [0] * n
    pairs = list(combinations(range(n), 2))
    for i, (u, v) in enumerate(pairs):
        if edge_bits >> i & 1:
            adj[u] |= 1 << v
            adj[v] |= 1 << u

    @lru_cache(None)
    def comps(mask: int):
        out = []
        unseen = mask
        while unseen:
            bit = unseen & -unseen
            todo = bit
            seen = 0
            while todo:
                xbit = todo & -todo
                todo -= xbit
                x = xbit.bit_length() - 1
                seen |= xbit
                todo |= adj[x] & unseen & ~seen
            out.append(seen)
            unseen &= ~seen
        return tuple(out)

    @lru_cache(None)
    def td(mask: int):
        if not mask:
            return 0
        cc = comps(mask)
        if len(cc) > 1:
            return max(td(c) for c in cc)
        return 1 + min(td(mask ^ (1 << v)) for v in range(n) if mask >> v & 1)

    def balanced(mask: int, sep: int):
        remain = mask & ~sep
        # The proof search uses the 3/4-balanced convention.
        return all(4 * popcount(c) <= 3 * popcount(mask) for c in comps(remain))

    @lru_cache(None)
    def minsep_height(mask: int):
        if not mask:
            return 0
        if len(comps(mask)) > 1:
            return max(minsep_height(c) for c in comps(mask))
        subsets = []
        sub = mask
        best_size = n + 1
        while sub:
            size = popcount(sub)
            if size <= best_size and balanced(mask, sub):
                if size < best_size:
                    best_size = size
                    subsets = []
                subsets.append(sub)
            sub = (sub - 1) & mask
        return min(
            best_size + max((minsep_height(c) for c in comps(mask & ~s)), default=0)
            for s in subsets
        )

    @lru_cache(None)
    def lex_greedy_height(mask: int):
        if not mask:
            return 0
        if len(comps(mask)) > 1:
            return max(lex_greedy_height(c) for c in comps(mask))
        profiles = {}
        for v in range(n):
            if mask >> v & 1:
                cc = comps(mask ^ (1 << v))
                profile = tuple(sorted((popcount(c) for c in cc), reverse=True))
                profiles.setdefault(profile, []).append((v, cc))
        best_profile = min(profiles)
        return 1 + min(
            max((lex_greedy_height(c) for c in cc), default=0)
            for _, cc in profiles[best_profile]
        )

    @lru_cache(None)
    def max_degree_height(mask: int):
        if not mask:
            return 0
        if len(comps(mask)) > 1:
            return max(max_degree_height(c) for c in comps(mask))
        degrees = {
            v: popcount(adj[v] & mask)
            for v in range(n)
            if mask >> v & 1
        }
        best_degree = max(degrees.values())
        return 1 + min(
            max((max_degree_height(c) for c in comps(mask ^ (1 << v))), default=0)
            for v, degree in degrees.items()
            if degree == best_degree
        )

    whole = (1 << n) - 1
    if len(comps(whole)) != 1:
        return None
    return (
        td(whole),
        minsep_height(whole),
        lex_greedy_height(whole),
        max_degree_height(whole),
        pairs,
    )


def main():
    for n in range(2, 7):
        worst_sep = (0.0, None)
        worst_lex = (0.0, None)
        worst_degree = (0.0, None)
        for bits in range(1 << (n * (n - 1) // 2)):
            result = analyze(n, bits)
            if result is None:
                continue
            depth, sep_h, lex_h, degree_h, pairs = result
            edges = [p for i, p in enumerate(pairs) if bits >> i & 1]
            if sep_h / depth > worst_sep[0]:
                worst_sep = (sep_h / depth, (depth, sep_h, edges))
            if lex_h / depth > worst_lex[0]:
                worst_lex = (lex_h / depth, (depth, lex_h, edges))
            if degree_h / depth > worst_degree[0]:
                worst_degree = (degree_h / depth, (depth, degree_h, edges))
        print(
            "n", n,
            "minimum-separator", worst_sep,
            "lex-greedy", worst_lex,
            "max-degree", worst_degree,
        )


if __name__ == "__main__":
    main()
