#!/usr/bin/env python3
"""Exhaustive small-polyomino diagnostics for proof-search hypotheses."""

from collections import Counter, defaultdict, deque

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def canon(cells):
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def connected(cells):
    cells = set(cells)
    if not cells:
        return False
    seen = {next(iter(cells))}
    queue = deque(seen)
    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRS:
            z = (x + dx, y + dy)
            if z in cells and z not in seen:
                seen.add(z)
                queue.append(z)
    return len(seen) == len(cells)


def extensions(poly):
    cells = set(poly)
    ans = set()
    for x, y in cells:
        for dx, dy in DIRS:
            z = (x + dx, y + dy)
            if z not in cells:
                ans.add(canon(cells | {z}))
    return ans


def boundary_sites(poly):
    cells = set(poly)
    return {
        (x + dx, y + dy)
        for x, y in cells
        for dx, dy in DIRS
        if (x + dx, y + dy) not in cells
    }


def hole_count(poly):
    cells = set(poly)
    min_x = min(x for x, _ in cells) - 1
    max_x = max(x for x, _ in cells) + 1
    min_y = min(y for _, y in cells) - 1
    max_y = max(y for _, y in cells) + 1
    empty = {
        (x, y)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
        if (x, y) not in cells
    }
    components = 0
    while empty:
        components += 1
        seen = {next(iter(empty))}
        queue = deque(seen)
        empty -= seen
        while queue:
            x, y = queue.popleft()
            for dx, dy in DIRS:
                z = x + dx, y + dy
                if z in empty:
                    empty.remove(z)
                    seen.add(z)
                    queue.append(z)
    return components - 1


def removable(poly):
    cells = set(poly)
    if len(cells) == 1:
        return []
    return [z for z in poly if connected(cells - {z})]


def parent(poly):
    """Delete the lexicographically greatest removable cell."""
    z = max(removable(poly))
    return canon(set(poly) - {z})


def distinct_parents(poly):
    return {canon(set(poly) - {z}) for z in removable(poly)}


def prime(poly):
    """No valid split under Klarner's vertical lexicographic concatenation."""
    cells = list(poly)
    for k in range(1, len(cells)):
        left, right = set(cells[:k]), set(cells[k:])
        if not connected(left) or not connected(right):
            continue
        x1, y1 = max(left)
        x2, y2 = min(right)
        if x1 == x2 and y2 == y1 + 1:
            return False
    return True


def concatenate(left, right):
    x1, y1 = max(left)
    x2, y2 = min(right)
    shift = (x1 - x2, y1 + 1 - y2)
    moved = {(x + shift[0], y + shift[1]) for x, y in right}
    return canon(set(left) | moved)


levels = {1: {((0, 0),)}}
for n in range(1, 11):
    levels[n + 1] = set().union(*(extensions(p) for p in levels[n]))

print("counts", [len(levels[n]) for n in levels])

boundary_polynomials = {
    n: Counter(len(boundary_sites(p)) for p in levels[n])
    for n in levels
}
for q in (0.01, 0.1, 0.25, 0.5, 0.75, 1.0):
    vals = {
        n: sum(count * q**power for power, count in poly.items())
        for n, poly in boundary_polynomials.items()
    }
    failures = [
        n for n in range(2, 10)
        if vals[n] ** 2 >= vals[n - 1] * vals[n + 1]
    ]
    print("boundary-weight", q, "strict-logconvex-fail-centers", failures)

hole_polynomials = {
    n: Counter(hole_count(p) for p in levels[n])
    for n in levels
}
for q in (0.01, 0.1, 1.0, 10.0, 100.0):
    vals = {
        n: sum(count * q**power for power, count in poly.items())
        for n, poly in hole_polynomials.items()
    }
    failures = [
        n for n in range(2, 10)
        if vals[n] ** 2 >= vals[n - 1] * vals[n + 1]
    ]
    print("hole-weight", q, "strict-logconvex-fail-centers", failures)

for n in range(2, 10):
    lhs = Counter()
    rhs = Counter()
    for i, ai in boundary_polynomials[n].items():
        for j, aj in boundary_polynomials[n].items():
            lhs[i + j] += ai * aj
    for i, ai in boundary_polynomials[n - 1].items():
        for j, aj in boundary_polynomials[n + 1].items():
            rhs[i + j] += ai * aj
    difference = rhs.copy()
    difference.subtract(lhs)
    print(
        "boundary-poly-center", n,
        "coefficientwise", all(value >= 0 for value in difference.values()),
        "negative-terms", sorted((power, value) for power, value in difference.items() if value < 0)[:5],
    )

for n in range(1, 7):
    extension_witness = None
    parent_witness = None
    for p in levels[n]:
        for q in extensions(p):
            if len(extensions(q)) < len(extensions(p)) and extension_witness is None:
                extension_witness = p, q, len(extensions(p)), len(extensions(q))
            if len(distinct_parents(q)) < len(distinct_parents(p)) and parent_witness is None:
                parent_witness = p, q, len(distinct_parents(p)), len(distinct_parents(q))
    print("simple-cover-degree", n, "up-drop", extension_witness, "down-drop", parent_witness)
for width_bound in (1, 2, 3, 4):
    counts = [
        sum(max(x for x, _ in p) + 1 <= width_bound for p in levels[n])
        for n in levels
    ]
    bad = [
        n
        for n in range(2, len(counts))
        if counts[n - 1] * counts[n - 1] > counts[n - 2] * counts[n]
    ]
    print("width-bound", width_bound, counts, "logconvex-fail-centers", bad)
print("n min_ext max_ext avg_ext min_bdy max_bdy avg_bdy min_rem max_rem avg_rem primes")
for n, polys in levels.items():
    ex = [len(extensions(p)) for p in polys]
    bd = [len(boundary_sites(p)) for p in polys]
    rm = [len(removable(p)) for p in polys]
    print(
        n,
        min(ex), max(ex), sum(ex) / len(ex),
        min(bd), max(bd), sum(bd) / len(bd),
        min(rm), max(rm), sum(rm) / len(rm),
        sum(prime(p) for p in polys),
    )
    if n >= 2:
        count = len(polys)
        mean_bd = sum(b * d for b, d in zip(bd, rm)) / count
        covariance = mean_bd - (sum(bd) / count) * (sum(rm) / count)
        print("  boundary-removable covariance", covariance)

for n in range(1, 10):
    lhs = sum(len(boundary_sites(p)) for p in levels[n])
    rhs = sum(len(removable(q)) for q in levels[n + 1])
    changes = []
    removable_changes = []
    joint_changes = []
    for p in levels[n]:
        for z in boundary_sites(p):
            q = canon(set(p) | {z})
            changes.append(len(boundary_sites(q)) - len(boundary_sites(p)))
            removable_changes.append((len(removable(q)) - len(removable(p)), p, q))
            joint_changes.append(
                (
                    len(boundary_sites(q)) + len(removable(q))
                    - len(boundary_sites(p)) - len(removable(p)),
                    p,
                    q,
                )
            )
    lo = min(removable_changes, key=lambda item: item[0])
    hi = max(removable_changes, key=lambda item: item[0])
    print(
        "marked-incidence", n, lhs, rhs, "equal", lhs == rhs,
        "bdy-change-range", (min(changes), max(changes)),
        "rem-change-range", (lo[0], hi[0]), "rem-drop-witness", lo[1:],
        "joint-min", min(joint_changes, key=lambda item: item[0]),
    )

for n in range(2, 8):
    constructible = {
        concatenate(x, y)
        for k in range(1, n)
        for x in levels[k]
        for y in levels[n - k]
    }
    detected = {p for p in levels[n] if not prime(p)}
    if constructible != detected:
        print(
            "constructibility mismatch", n,
            "generated-only", constructible - detected,
            "detected-only", detected - constructible,
        )

    first_prime_factorizations = defaultdict(list)
    for k in range(1, n):
        for x in levels[k]:
            if prime(x):
                for y in levels[n - k]:
                    first_prime_factorizations[concatenate(x, y)].append((x, y))
    collisions = {p: fs for p, fs in first_prime_factorizations.items() if len(fs) > 1}
    if collisions:
        first_collision = next(iter(collisions.items()))
        print("prime-prefix factorization collision", n, first_collision)

associativity_witness = None
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            for x in levels[i]:
                for y in levels[j]:
                    for z in levels[k]:
                        left = concatenate(concatenate(x, y), z)
                        right = concatenate(x, concatenate(y, z))
                        if left != right:
                            associativity_witness = (i, j, k, x, y, z, left, right)
                            break
                    if associativity_witness:
                        break
                if associativity_witness:
                    break
            if associativity_witness:
                break
        if associativity_witness:
            break
    if associativity_witness:
        break
print("concatenation-associative-through-4", associativity_witness is None, associativity_witness)

children = defaultdict(list)
for n in range(2, 11):
    for q in levels[n]:
        children[parent(q)].append(q)

print("canonical-parent max fibers", [max(map(len, (children[p] for p in levels[n]))) for n in range(1, 10)])
for n in range(1, 9):
    witness = None
    for p in levels[n]:
        dp = len(children[p])
        for q in children[p]:
            if len(children[q]) < dp:
                witness = (p, q, dp, len(children[q]))
                break
        if witness:
            break
    print("degree-monotone", n, witness is None, witness)


def oriented_horizontal_cuts(poly):
    """Cuts associated with the deliberately free horizontal product in Route 23."""
    cells = set(poly)
    answer = []
    min_y = min(y for _, y in cells)
    max_y = max(y for _, y in cells)
    for cut_y in range(min_y, max_y):
        lower = {(x, y) for x, y in cells if y <= cut_y}
        upper = cells - lower
        if not connected(lower) or not connected(upper):
            continue
        crossing = [
            x for x, y in lower
            if y == cut_y and (x, cut_y + 1) in upper
        ]
        if len(crossing) != 1:
            continue
        anchor = crossing[0]
        if anchor != max(x for x, y in lower if y == cut_y):
            continue
        if anchor != min(x for x, y in upper if y == cut_y + 1):
            continue
        answer.append(cut_y)
    return answer


cut_indec = {
    n: {poly for poly in levels[n] if not oriented_horizontal_cuts(poly)}
    for n in levels
}
print("oriented-cut-indecomposable counts", [len(cut_indec[n]) for n in levels])
for n in range(2, 11):
    no_parent = None
    for poly in cut_indec[n]:
        good = [
            z for z in removable(poly)
            if canon(set(poly) - {z}) in cut_indec[n - 1]
        ]
        if not good:
            no_parent = poly
            break
    bad_east_extension = None
    if n < 10:
        for poly in cut_indec[n]:
            max_x = max(x for x, _ in poly)
            for x, y in poly:
                if x == max_x:
                    child = canon(set(poly) | {(x + 1, y)})
                    if child not in cut_indec[n + 1]:
                        bad_east_extension = (poly, (x + 1, y), child)
                        break
            if bad_east_extension:
                break
    print(
        "cut-indec-accessibility", n, no_parent is None, no_parent,
        "east-extension-preserves", bad_east_extension is None, bad_east_extension,
    )

for n in range(1, 10):
    upward = {
        poly: len(extensions(poly) & cut_indec[n + 1])
        for poly in cut_indec[n]
    }
    downward = {
        poly: len(distinct_parents(poly) & cut_indec[n - 1])
        for poly in cut_indec[n]
    } if n >= 2 else {}
    print(
        "cut-indec-cover-degrees", n,
        "up-range", (min(upward.values()), max(upward.values())),
        "down-range", (min(downward.values()), max(downward.values())) if downward else None,
    )

for n in range(1, 9):
    up_degree_n = {p: len(extensions(p) & cut_indec[n + 1]) for p in cut_indec[n]}
    up_degree_next = {q: len(extensions(q) & cut_indec[n + 2]) for q in cut_indec[n + 1]}
    down_degree_n = {
        p: len(distinct_parents(p) & cut_indec[n - 1]) for p in cut_indec[n]
    } if n >= 2 else {}
    down_degree_next = {
        q: len(distinct_parents(q) & cut_indec[n]) for q in cut_indec[n + 1]
    }
    up_drop = down_drop = None
    for p in cut_indec[n]:
        for q in extensions(p) & cut_indec[n + 1]:
            if up_degree_next[q] < up_degree_n[p] and up_drop is None:
                up_drop = (p, q, up_degree_n[p], up_degree_next[q])
            if n >= 2 and down_degree_next[q] < down_degree_n[p] and down_drop is None:
                down_drop = (p, q, down_degree_n[p], down_degree_next[q])
    print("cut-indec-degree-monotone", n, "up-drop", up_drop, "down-drop", down_drop)
