#!/usr/bin/env python3
"""Numerically search for sharper supersolutions of the 17-variable system."""

import argparse
import math


NAMES = tuple("cdefgh") + tuple("pqrstuvwxyz")


def transform(a, zz):
    c, d, e, f, g, h = (a[k] for k in "cdefgh")
    p, q, r, s, t, u, v, w, x, y, z = (a[k] for k in "pqrstuvwxyz")
    return {
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


def iterate(mu, max_steps=1_000_000, tolerance=1e-14):
    zz = 1.0 / mu
    a = {name: 0.0 for name in NAMES}
    for step in range(1, max_steps + 1):
        b = transform(a, zz)
        if not all(math.isfinite(value) and value < 1e100 for value in b.values()):
            return False, step, b, math.inf
        delta = max(abs(b[k] - a[k]) for k in NAMES)
        a = b
        if delta < tolerance:
            return True, step, a, delta
    return False, max_steps, a, delta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mu", nargs="*", type=float)
    args = parser.parse_args()
    candidates = args.mu or [4.5238, 4.5237, 4.5236, 4.5235, 4.523, 4.522]
    for mu in candidates:
        ok, steps, a, delta = iterate(mu)
        print(f"mu={mu:.10f}: {'converged' if ok else 'failed'} in {steps} steps; delta={delta:.4g}")
        if ok:
            print(" ".join(f"{k}={a[k]:.12g}" for k in NAMES))


if __name__ == "__main__":
    main()
