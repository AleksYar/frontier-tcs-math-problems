import itertools
import math
import random


def area(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) / 2


def points_from(params, sides=3):
    pts = []
    layers = len(params)
    for j, phi in enumerate(params):
        radius = 0.95 - 0.75 * j / max(1, layers - 1)
        for k in range(sides):
            t = phi + 2 * math.pi * k / sides
            pts.append((0.5 + 0.48 * radius * math.cos(t), 0.5 + 0.48 * radius * math.sin(t)))
    return pts


def minimum_area(params, sides=3):
    pts = points_from(params, sides)
    return min(area(pts[i], pts[j], pts[k]) for i, j, k in itertools.combinations(range(len(pts)), 3))


def anneal(layers, sides, trials=30000):
    period = 2 * math.pi / sides
    params = [random.random() * period for _ in range(layers)]
    score = minimum_area(params, sides)
    best = score
    for step in range(trials):
        idx = random.randrange(layers)
        old = params[idx]
        scale = period * (0.15 * (1 - step / trials) + 0.002)
        params[idx] = (old + random.gauss(0, scale)) % period
        new = minimum_area(params, sides)
        temp = max(1e-9, best * 0.05 * (1 - step / trials))
        if new >= score or random.random() < math.exp((new - score) / temp):
            score = new
            best = max(best, new)
        else:
            params[idx] = old
    return best


random.seed(20260828)
for sides in (3, 4, 5):
    for layers in (3, 4, 5, 6, 8, 10):
        best = max(anneal(layers, sides, 3000) for _ in range(2))
        print(sides, layers, best, best * layers**2, best * (sides * layers) ** (7 / 6))
