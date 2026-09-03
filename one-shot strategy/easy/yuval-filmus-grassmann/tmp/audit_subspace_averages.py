#!/usr/bin/env python3
"""Exhaustively audit the auxiliary subspace-average lemma over F_2^d."""

from collections import Counter, defaultdict


def span(vs):
    basis = {}
    for x in vs:
        y = x
        while y:
            p = y.bit_length() - 1
            if p in basis:
                y ^= basis[p]
            else:
                basis[p] = y
                break
    out = [0]
    for b in basis.values():
        out += [x ^ b for x in out]
    return frozenset(out)


def all_subspaces(d):
    seen = {frozenset({0})}
    frontier = [frozenset({0})]
    while frontier:
        r = frontier.pop()
        for x in range(1, 1 << d):
            if x not in r:
                s = span(tuple(r) + (x,))
                if s not in seen:
                    seen.add(s)
                    frontier.append(s)
    return sorted(seen, key=lambda r: (len(r), tuple(r)))


def dot(a, x):
    return bin(a & x).count("1") & 1


def valid(phi, subs):
    return all(sum(phi[x] for x in r) in (0, len(r), 2 * len(r)) for r in subs)


def main(d=4):
    subs = all_subspaces(d)
    n = 1 << d
    counts = Counter()
    examples = defaultdict(list)

    # phi(0)=0.  Plane parity forces t=phi/2 to have parity ell.
    for ell in range(n):
        kernel = [x for x in range(1, n) if dot(ell, x) == 0]
        odd = [x for x in range(1, n) if dot(ell, x) == 1]
        for mask in range(1 << len(kernel)):
            phi = [0] * n
            for x in odd:
                phi[x] = 2
            for i, x in enumerate(kernel):
                if (mask >> i) & 1:
                    phi[x] = 4
            if valid(phi, subs):
                T = frozenset(x for x in kernel if phi[x] == 4)
                key = (ell == 0, len(T), len(span(T)))
                counts[key] += 1
                if len(examples[key]) < 3:
                    examples[key].append((ell, tuple(sorted(T)), tuple(phi)))

    print('d', d, 'subspaces', len(subs), 'valid phi0=0', sum(counts.values()))
    for key in sorted(counts):
        print(key, counts[key], examples[key][:2])

    odd_counts = Counter()
    for ell in range(n):
        support = [x for x in range(1, n) if dot(ell, x) == 1]
        if ell == 0:
            candidates = [0]
        else:
            candidates = range(1 << len(support))
        for mask in candidates:
            phi = [1] * n
            phi[0] = 1
            for i, x in enumerate(support):
                phi[x] = 3 if (mask >> i) & 1 else -1
            if valid(phi, subs):
                # Count distinct sign tables; an affine character should have
                # all second derivatives zero on the support hyperplane.
                plus = sum(phi[x] == 3 for x in support)
                odd_counts[(ell == 0, plus)] += 1
    print('valid phi0=1', sum(odd_counts.values()))
    for key in sorted(odd_counts):
        print(key, odd_counts[key])


if __name__ == '__main__':
    main()
