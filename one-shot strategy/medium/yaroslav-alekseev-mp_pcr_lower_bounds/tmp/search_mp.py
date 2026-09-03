#!/usr/bin/env python3
"""Bounded saturation experiments for one-variable MP-PCR.

This is not a proof search over the unbounded calculus.  It is used only to
falsify proposed small-step simulations and invariants.  Polynomials are
canonical tuples (coefficient, exponent_x, exponent_xbar), with tropical
duplicates merged by taking the least coefficient.
"""

from collections import defaultdict, deque
from itertools import combinations_with_replacement, product
import argparse
import time

INF = 10**9


def poly(terms):
    best = {}
    for c, a, b in terms:
        key = (a, b)
        if c < best.get(key, INF):
            best[key] = c
    return tuple(sorted((c, a, b) for (a, b), c in best.items()))


def pmin(p, q):
    return poly(p + q)


def pmul(p, term):
    c, a, b = term
    return poly((d + c, i + a, j + b) for d, i, j in p)


def admissible(p, max_terms, max_degree, coeff_bound):
    return (
        len(p) <= max_terms
        and all(a + b <= max_degree for _, a, b in p)
        and all(abs(c) <= coeff_bound for c, _, _ in p)
    )


def fmt(p):
    if not p:
        return "inf"
    out = []
    for c, a, b in p:
        factors = []
        if c:
            factors.append(str(c))
        if a:
            factors.append("x" if a == 1 else f"x^{a}")
        if b:
            factors.append("X" if b == 1 else f"X^{b}")
        out.append("+".join(factors) if factors else "0")
    return " min ".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=int, default=900)
    ap.add_argument("--terms", type=int, default=3)
    ap.add_argument("--degree", type=int, default=5)
    ap.add_argument("--coeff", type=int, default=4)
    ap.add_argument("--max-lines", type=int, default=300000)
    args = ap.parse_args()

    zero, one = poly([(0, 0, 0)]), poly([(1, 0, 0)])
    x, xb = poly([(0, 1, 0)]), poly([(0, 0, 1)])
    xx = poly([(0, 2, 0)])
    # Premise used in the paper's non-deducibility example.
    premise = (pmin(xx, x), zero)
    initial = [
        premise,
        (poly([(0, 1, 1)]), one),
        (one, poly([(0, 1, 1)])),
        (pmin(x, xb), zero),
        (zero, pmin(x, xb)),
        (zero, zero),
    ]
    targets = {
        (xx, zero): "tropical-resolution target x^2 <= 0",
        (one, zero): "contradiction 1 <= 0",
    }
    multipliers = [
        (c, a, b)
        for c in range(-args.coeff, args.coeff + 1)
        for a in range(args.degree + 1)
        for b in range(args.degree + 1 - a)
    ]

    lines = []
    line_set = set()
    parents = {}
    left_index, right_index = defaultdict(list), defaultdict(list)
    frontier = deque()

    def add(line, why):
        if line in line_set:
            return False
        p, q = line
        if not (admissible(p, args.terms, args.degree, args.coeff)
                and admissible(q, args.terms, args.degree, args.coeff)):
            return False
        idx = len(lines)
        lines.append(line)
        line_set.add(line)
        parents[line] = why
        left_index[p].append(idx)
        right_index[q].append(idx)
        frontier.append(idx)
        if line in targets:
            print(f"FOUND {targets[line]} at line {idx}: {fmt(p)} <= {fmt(q)}", flush=True)
        return True

    for line in initial:
        add(line, ("axiom",))

    start = time.time()
    last_report = start
    while frontier and len(lines) < args.max_lines and time.time() - start < args.seconds:
        i = frontier.popleft()
        p, q = lines[i]

        for t in multipliers:
            add((pmul(p, t), pmul(q, t)), ("mul", i, t))

        # Exact transitivity, both orientations involving the new line.
        for j in list(left_index.get(q, ())):
            add((p, lines[j][1]), ("trans", i, j))
        for j in list(right_index.get(p, ())):
            add((lines[j][0], q), ("trans", j, i))

        # Minimum with older lines.  Limit the partner sampling if saturation
        # gets large; this remains a falsification search only.
        partner_count = min(i + 1, 5000)
        stride = max(1, (i + 1) // partner_count)
        for j in range(0, i + 1, stride):
            r, s = lines[j]
            add((pmin(p, r), pmin(q, s)), ("min", i, j))

        now = time.time()
        if now - last_report >= 30:
            print(
                f"elapsed={now-start:.1f}s lines={len(lines)} frontier={len(frontier)}",
                flush=True,
            )
            last_report = now

    print(
        f"DONE elapsed={time.time()-start:.1f}s lines={len(lines)} "
        f"frontier={len(frontier)} target={((xx, zero) in line_set)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
