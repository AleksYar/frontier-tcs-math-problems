from fractions import Fraction
from itertools import product, combinations


def projective_lines(nonzero_vectors):
    lines = set()
    vectors = set(nonzero_vectors)
    for a, b in combinations(sorted(vectors), 2):
        c = a ^ b
        if c in vectors:
            lines.add(tuple(sorted((a, b, c))))
    return sorted(lines)


points3 = list(range(1, 8))
lines3 = projective_lines(points3)
points4 = list(range(1, 16))
lines4 = projective_lines(points4)


def fano_coefficients_scaled6(values):
    """Return six times the coefficients (thereby using integers only)."""
    total = sum(values)
    return {
        p: 3 * sum(values[i] for i, line in enumerate(lines3) if p in line) - total
        for p in points3
    }


def enumerate_ternary_degree_one():
    functions = set()
    extension_count = 0
    remaining_pairs = [pair for pair in combinations(points3, 2) if pair != (1, 2)]
    ternary_scaled12 = {0, 12, 24}

    for inner_values in product(range(3), repeat=7):
        inner_coeffs6 = fano_coefficients_scaled6(inner_values)
        for through_zero in product(range(3), repeat=7):
            t = (0,) + through_zero
            for anchor_value in range(3):
                # Z is 12*c_8.  The anchor line {8^1,8^2,3}
                # has the prescribed value anchor_value.
                z12 = (
                    6 * (t[1] + t[2] - anchor_value)
                    - inner_coeffs6[1]
                    - inner_coeffs6[2]
                    + inner_coeffs6[3]
                )
                outer12 = [z12] + [
                    12 * t[a] - z12 - 2 * inner_coeffs6[a]
                    for a in points3
                ]
                good = True
                for a, b in remaining_pairs:
                    value12 = outer12[a] + outer12[b] + 2 * inner_coeffs6[a ^ b]
                    if value12 not in ternary_scaled12:
                        good = False
                        break
                if good:
                    extension_count += 1
                    coeffs12 = {p: 2 * inner_coeffs6[p] for p in points3}
                    coeffs12.update({8 ^ a: outer12[a] for a in range(8)})
                    vals = tuple(sum(coeffs12[p] for p in line) // 12 for line in lines4)
                    assert set(vals) <= {0, 1, 2}
                    functions.add(vals)
    return functions, extension_count


def dot(a, b):
    return bin(a & b).count("1") % 2


def boolean_trivial_functions():
    funcs = set()
    zero = (0,) * len(lines4)
    one = (1,) * len(lines4)
    funcs.update((zero, one))
    for p in points4:
        xp = tuple(int(p in line) for line in lines4)
        funcs.add(xp)
        funcs.add(tuple(1 - x for x in xp))
    for r in points4:
        yr = tuple(int(all(dot(r, p) == 0 for p in line)) for line in lines4)
        funcs.add(yr)
        funcs.add(tuple(1 - y for y in yr))
        for p in points4:
            if dot(p, r) == 1:
                xp = tuple(int(p in line) for line in lines4)
                plus = tuple(x + y for x, y in zip(xp, yr))
                assert set(plus) <= {0, 1}
                funcs.add(plus)
                funcs.add(tuple(1 - v for v in plus))
    return funcs


def linear_generators():
    def apply_swap(x, i, j):
        bi, bj = (x >> i) & 1, (x >> j) & 1
        if bi != bj:
            x ^= (1 << i) | (1 << j)
        return x

    def apply_transvection(x, target, source):
        if (x >> source) & 1:
            x ^= 1 << target
        return x

    maps = []
    for i in range(3):
        maps.append({x: apply_swap(x, i, i + 1) for x in range(16)})
    for target in range(4):
        for source in range(4):
            if target != source:
                maps.append({x: apply_transvection(x, target, source) for x in range(16)})
    return maps


def function_permutations():
    line_index = {line: i for i, line in enumerate(lines4)}
    permutations = []
    for point_map in linear_generators():
        permutations.append(tuple(
            line_index[tuple(sorted(point_map[p] for p in line))]
            for line in lines4
        ))
    return permutations


def orbit_summaries(functions, pair_sums):
    unseen = set(functions)
    permutations = function_permutations()
    summaries = []
    while unseen:
        representative = min(unseen)
        orbit = {representative}
        frontier = [representative]
        while frontier:
            f = frontier.pop()
            neighbors = [tuple(2 - x for x in f)]
            neighbors.extend(tuple(f[permutation[i]] for i in range(35)) for permutation in permutations)
            for g in neighbors:
                if g not in orbit:
                    orbit.add(g)
                    frontier.append(g)
        unseen.difference_update(orbit)
        total = sum(representative)
        coeffs = tuple(sorted(
            Fraction(sum(representative[i] for i, line in enumerate(lines4) if p in line), 6)
            - Fraction(total, 42)
            for p in points4
        ))
        summaries.append((
            len(orbit),
            representative in pair_sums,
            tuple(representative.count(i) for i in range(3)),
            coeffs,
        ))
    return sorted(summaries, key=lambda row: (not row[1], row[2], row[3]))


if __name__ == "__main__":
    ternary, extension_count = enumerate_ternary_degree_one()
    boolean = boolean_trivial_functions()
    pair_sums = {
        tuple(x + y for x, y in zip(f, g))
        for f in boolean
        for g in boolean
    }
    print("lines3", len(lines3), "lines4", len(lines4))
    print("valid extensions before deduplication", extension_count)
    print("ternary degree-one functions", len(ternary))
    print("Boolean trivial functions", len(boolean))
    print("distinct pair sums", len(pair_sums))
    print("ternary not pair sums", len(ternary - pair_sums))
    print("pair sums not ternary", len(pair_sums - ternary))
    if ternary - pair_sums:
        counterexample = min(ternary - pair_sums)
        total = sum(counterexample)
        sums_at_point = {
            p: sum(counterexample[i] for i, line in enumerate(lines4) if p in line)
            for p in points4
        }
        coefficients = {
            p: Fraction(sums_at_point[p], 6) - Fraction(total, 42)
            for p in points4
        }
        print("counterexample", counterexample)
        print("counterexample level counts", tuple(counterexample.count(i) for i in range(3)))
        print("counterexample coefficients", coefficients)
        print("line order", lines4)
    summaries = orbit_summaries(ternary, pair_sums)
    print("orbits under GL(4,2) and value-complement", len(summaries))
    print("pair-sum orbits", sum(row[1] for row in summaries))
    print("non-pair-sum orbits", sum(not row[1] for row in summaries))
    for i, summary in enumerate(summaries):
        print("orbit", i, summary)
