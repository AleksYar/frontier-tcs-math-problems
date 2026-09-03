import itertools
import math
import random

def triangle_area(a, b, c):
    return abs((b[0] - a[0]) * (c[1] - a[1])
               - (b[1] - a[1]) * (c[0] - a[0])) / 2


def min_area(points):
    return min(triangle_area(points[i], points[j], points[k])
               for i, j, k in itertools.combinations(range(len(points)), 3))


def onion_depth(points):
    def hull_positions(subpoints):
        indexed = sorted(enumerate(subpoints), key=lambda x: (x[1][0], x[1][1]))
        def cross(o, a, b):
            return ((a[0] - o[0]) * (b[1] - o[1])
                    - (a[1] - o[1]) * (b[0] - o[0]))
        lower = []
        for item in indexed:
            while len(lower) >= 2 and cross(lower[-2][1], lower[-1][1], item[1]) <= 0:
                lower.pop()
            lower.append(item)
        upper = []
        for item in reversed(indexed):
            while len(upper) >= 2 and cross(upper[-2][1], upper[-1][1], item[1]) <= 0:
                upper.pop()
            upper.append(item)
        return {i for i, _ in lower[:-1] + upper[:-1]}

    indices = list(range(len(points)))
    depth = 0
    sizes = []
    while len(indices) >= 3:
        layer_positions = hull_positions([points[i] for i in indices])
        layer = [indices[i] for i in layer_positions]
        sizes.append(len(layer))
        indices = [idx for pos, idx in enumerate(indices) if pos not in layer_positions]
        depth += 1
    if indices:
        sizes.append(len(indices))
        depth += 1
    return depth, sizes


def optimize(n, steps=120000):
    p = [[random.random(), random.random()] for _ in range(n)]
    score = min_area(p)
    best_p = [x[:] for x in p]
    best = score
    for step in range(steps):
        i = random.randrange(n)
        old = p[i][:]
        scale = 0.08 * (1 - step / steps) + 0.0005
        p[i] = [min(1, max(0, old[j] + random.gauss(0, scale))) for j in range(2)]
        new = min_area(p)
        temp = max(best * 0.02 * (1 - step / steps), 1e-10)
        if new >= score or random.random() < math.exp((new - score) / temp):
            score = new
            if new > best:
                best = new
                best_p = [x[:] for x in p]
        else:
            p[i] = old
    return best, best_p


random.seed(981237)
for n in (8, 10, 12, 14, 16, 18):
    score, pts = optimize(n, 12000)
    depth, sizes = onion_depth(pts)
    print(n, score, depth, sizes, score * depth**2, score * n**(7/6))
