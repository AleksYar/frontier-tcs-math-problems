#!/usr/bin/env python3
"""Exact-arithmetic checker for the rational supersolution certificate."""

from fractions import Fraction as Q


VALUES = {
    "c": Q(871, 2500),
    "d": Q(2157, 5000),
    "e": Q(2879, 5000),
    "f": Q(1003, 625),
    "g": Q(4757, 5000),
    "h": Q(1851, 2500),
    "p": Q(3267, 5000),
    "q": Q(939, 2500),
    "r": Q(599, 2500),
    "s": Q(309, 1000),
    "t": Q(727, 2500),
    "u": Q(633, 1250),
    "v": Q(621, 5000),
    "w": Q(509, 5000),
    "x": Q(833, 5000),
    "y": Q(689, 5000),
    "z": Q(567, 5000),
}

SHARP_VALUES = {
    "c": Q(1387, 4000),
    "d": Q(42799, 100000),
    "e": Q(7107, 12500),
    "f": Q(157199, 100000),
    "g": Q(11701, 12500),
    "h": Q(18279, 25000),
    "p": Q(63591, 100000),
    "q": Q(2297, 6250),
    "r": Q(23587, 100000),
    "s": Q(30317, 100000),
    "t": Q(357, 1250),
    "u": Q(12367, 25000),
    "v": Q(12107, 100000),
    "w": Q(9951, 100000),
    "x": Q(16453, 100000),
    "y": Q(3409, 25000),
    "z": Q(703, 6250),
}

BEST_VALUES = {
    "c": Q(1740517, 5000000),
    "d": Q(1077131, 2500000),
    "e": Q(5746453, 10000000),
    "f": Q(99963, 62500),
    "g": Q(1186201, 1250000),
    "h": Q(1477811, 2000000),
    "p": Q(813059, 1250000),
    "q": Q(748631, 2000000),
    "r": Q(1194337, 5000000),
    "s": Q(3080531, 10000000),
    "t": Q(22649, 78125),
    "u": Q(1260813, 2500000),
    "v": Q(1236361, 10000000),
    "w": Q(1013683, 10000000),
    "x": Q(1662711, 10000000),
    "y": Q(1374991, 10000000),
    "z": Q(565819, 5000000),
}


def margins(mu_numerator: int, mu_denominator: int = 10_000, values=VALUES):
    """Return lhs-rhs for all 17 certificate inequalities at zeta=1/mu."""
    a = values
    c, d, e, f, g, h = (a[k] for k in "cdefgh")
    p, q, r, s, t, u, v, w, x, y, z = (a[k] for k in "pqrstuvwxyz")
    zz = Q(mu_denominator, mu_numerator)
    rhs = {
        "c": zz + zz * e,
        "d": zz + zz * g,
        "e": zz + zz * f,
        "f": g + p,
        "g": e + q,
        "h": d + s,
        "p": e * h + q * d + x * r + v * y + u * y * z,
        "q": zz * g + zz * (g * e) + zz**2 * (u + t * g + r * u),
        "r": y + w,
        "s": zz * g + zz * e**2 + zz**2 * t + zz**2 * x * g + zz**2 * y * u,
        "t": x + v,
        "u": d * h + s * d + y * r + w * y + u * z**2,
        "v": zz * s + zz**2 * (g**2 + t * e + r * t),
        "w": zz * s + zz**2 * (e * g + x * e + y * t),
        "x": zz * d + zz**2 * (g + u),
        "y": zz * c + zz**2 * (g + t),
        "z": zz * c + zz**2 * (e + x),
    }
    return {name: a[name] - value for name, value in rhs.items()}


def main():
    for mu_numerator in (45_238, 45_237, 45_236, 45_230, 45_200):
        ms = margins(mu_numerator)
        worst_name, worst = min(ms.items(), key=lambda item: item[1])
        print(
            f"mu={mu_numerator / 10_000:.4f}: "
            f"minimum margin {worst_name} = {float(worst):.12g} "
            f"({'PASS' if worst >= 0 else 'FAIL'})"
        )
    print("\nExact margins at mu=4.5238:")
    for name, margin in margins(45_238).items():
        print(f"{name}: {margin} = {float(margin):.12g}")
    print("\nExact margins for the sharper certificate at mu=4.5237:")
    sharp = margins(45_237, values=SHARP_VALUES)
    for name, margin in sharp.items():
        print(f"{name}: {margin} = {float(margin):.12g}")
    assert all(margin >= 0 for margin in sharp.values())
    print("\nExact margins for the best certificate at mu=4.5235:")
    best = margins(45_235, values=BEST_VALUES)
    for name, margin in best.items():
        print(f"{name}: {margin} = {float(margin):.12g}")
    assert all(margin >= 0 for margin in best.values())


if __name__ == "__main__":
    main()
