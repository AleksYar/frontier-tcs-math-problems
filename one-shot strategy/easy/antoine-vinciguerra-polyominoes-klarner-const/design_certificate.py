#!/usr/bin/env python3
"""Design a strict floating-point supersolution, then rationalize it."""

from fractions import Fraction
import argparse
import math

from search_certificate import NAMES, iterate, transform


def gaussian_solve(matrix, vector):
    n = len(vector)
    a = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        if abs(scale) < 1e-15:
            raise ArithmeticError("singular matrix")
        for j in range(col, n + 1):
            a[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            scale = a[row][col]
            for j in range(col, n + 1):
                a[row][j] -= scale * a[col][j]
    return [a[i][n] for i in range(n)]


def jacobian(point, zz, epsilon=1e-7):
    base = transform(point, zz)
    result = [[0.0 for _ in NAMES] for _ in NAMES]
    for col, name in enumerate(NAMES):
        shifted = dict(point)
        shifted[name] += epsilon
        value = transform(shifted, zz)
        for row, out_name in enumerate(NAMES):
            result[row][col] = (value[out_name] - base[out_name]) / epsilon
    return result


def margin(point, zz):
    image = transform(point, zz)
    return {name: point[name] - image[name] for name in NAMES}


def rational_point(point, denominator):
    # Start with nearest grid values. A later local grid search repairs inequalities.
    return {
        name: Fraction(round(point[name] * denominator), denominator)
        for name in NAMES
    }


def transform_fraction(a, zz):
    return transform(a, zz)


def repair_grid(point, zz, denominator, limit=2_000_000):
    """Raise a violated lhs by one grid unit until all exact inequalities hold."""
    a = dict(point)
    unit = Fraction(1, denominator)
    for step in range(limit):
        image = transform_fraction(a, zz)
        bad = [name for name in NAMES if a[name] < image[name]]
        if not bad:
            return a, step
        # Repair the relatively worst violated left side. This monotone adjustment can
        # worsen downstream inequalities, so cycle until either success or limit.
        name = min(bad, key=lambda k: float(a[k] - image[k]))
        needed = image[name] - a[name]
        units = max(1, math.ceil(float(needed * denominator)))
        a[name] += units * unit
        if any(float(value) > 100 for value in a.values()):
            break
    return None, limit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mu_numerator", nargs="?", type=int, default=45_237)
    parser.add_argument("--mu-denominator", type=int, default=10_000)
    args = parser.parse_args()
    mu_num = args.mu_numerator
    mu_den = args.mu_denominator
    mu = mu_num / mu_den
    zz = 1.0 / mu
    ok, _, fixed, _ = iterate(mu)
    assert ok
    jac = jacobian(fixed, zz)
    matrix = [
        [(1.0 if i == j else 0.0) - jac[i][j] for j in range(len(NAMES))]
        for i in range(len(NAMES))
    ]
    direction_values = gaussian_solve(matrix, [1.0] * len(NAMES))
    direction = dict(zip(NAMES, direction_values))
    print("direction", " ".join(f"{k}={direction[k]:.8g}" for k in NAMES))
    candidates = []
    for alpha in (1e-9, 2e-9, 5e-9, 1e-8, 2e-8, 5e-8, 1e-7, 2e-7, 5e-7,
                  1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5):
        point = {k: fixed[k] + alpha * direction[k] for k in NAMES}
        ms = margin(point, zz)
        worst = min(ms.values())
        print(f"alpha={alpha:g} min_margin={worst:.12g}")
        if worst > 0:
            candidates.append((worst, point, alpha))
    if not candidates:
        raise SystemExit("no floating supersolution found")
    _, point, alpha = max(candidates, key=lambda item: item[0])
    print(f"selected alpha={alpha:g}")
    exact_zeta = Fraction(mu_den, mu_num)
    for denominator in (100_000, 1_000_000, 10_000_000, 100_000_000):
        rounded = rational_point(point, denominator)
        repaired, steps = repair_grid(rounded, exact_zeta, denominator)
        if repaired is not None:
            ms = {k: repaired[k] - transform_fraction(repaired, exact_zeta)[k] for k in NAMES}
            print(f"SUCCESS denominator={denominator} repairs={steps} min={min(float(v) for v in ms.values()):.12g}")
            print(" ".join(f"{k}={repaired[k]}" for k in NAMES))
            break
        print(f"failed denominator={denominator}")


if __name__ == "__main__":
    main()
