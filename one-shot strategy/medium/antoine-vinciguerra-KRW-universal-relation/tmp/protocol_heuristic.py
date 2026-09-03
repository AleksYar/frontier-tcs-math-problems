#!/usr/bin/env python3
"""Heuristic tiny protocol synthesis using coordinate/g-value predicates only."""
from functools import lru_cache
import sys

n, m, table, start = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3], 0), int(sys.argv[4])
N = 1 << (n*m)

def grow(x, r):
    return (table >> ((x >> (r*n)) & ((1 << n)-1))) & 1

def gv(x):
    return sum(grow(x,r) << r for r in range(m))

out = {}
for x in range(N):
    for y in range(N):
        out[x,y] = (x ^ y) if gv(x) != gv(y) else 0

predicates = []
for bit in range(n*m):
    predicates.append(frozenset(x for x in range(N) if (x >> bit) & 1))
for r in range(m):
    predicates.append(frozenset(x for x in range(N) if grow(x,r)))
for v in range(1 << m):
    predicates.append(frozenset(x for x in range(N) if gv(x) == v))
# Add predicates for exact row values and simple parity of matrix coordinates.
for r in range(m):
    for v in range(1 << n):
        predicates.append(frozenset(x for x in range(N) if ((x >> (r*n)) & ((1<<n)-1)) == v))
# For n <= 3, include every row-local predicate.  This contains every split
# used by an optimal protocol for one copy of KW_g, so the ordinary two-stage
# protocol is available to the synthesizer (while NO answers remain heuristic).
if n <= 3:
    for r in range(m):
        for row_set in range(1, (1 << (1 << n)) - 1):
            predicates.append(frozenset(
                x for x in range(N)
                if (row_set >> ((x >> (r*n)) & ((1 << n)-1))) & 1))
predicates = list(dict.fromkeys(predicates))

def mono(A,B):
    common = (1 << (n*m)) - 1
    any_valid = False
    for x in A:
        for y in B:
            mask = out[x,y]
            if mask:
                any_valid = True
                common &= mask
                if not common:
                    return False
    return True

@lru_cache(None)
def can(A,B,d):
    A, B = frozenset(A), frozenset(B)
    if mono(A,B): return True
    if d == 0: return False
    for swap in (False, True):
        P,Q = (B,A) if swap else (A,B)
        for H in predicates:
            S = P & H
            if S and len(S) != len(P):
                if can(S,Q,d-1) and can(P-S,Q,d-1): return True
    return False

all_inputs = frozenset(range(N))
for d in range(start, n*m+5):
    ok = can(all_inputs,all_inputs,d)
    print(f"depth {d}: {'YES' if ok else 'NO'} states={can.cache_info().currsize}", flush=True)
    if ok: break
