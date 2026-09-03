"""Explore the formal-concept 'Core' automaton for delimiter languages."""

from collections import deque
from itertools import combinations

from search_rank import cycle_rank, minimize


def symmetric_path_closed_walks_then_delimiter(n):
    """Partial DFA for K c Sigma*, where K is closed walks at path vertex 0."""
    # Alternating edge colours give a bideterministic path automaton.
    # States 0..n-1 are before c, n is the accepting post-c sink, n+1 dead.
    sigma = ("a", "b", "c")
    dead, sink = n + 1, n
    rows = []
    for q in range(n):
        row = []
        for a in sigma[:2]:
            target = dead
            if q > 0 and sigma[(q - 1) % 2] == a:
                target = q - 1
            if q + 1 < n and sigma[q % 2] == a:
                target = q + 1
            row.append(target)
        row.append(sink if q == 0 else dead)
        rows.append(tuple(row))
    rows.append((sink, sink, sink))
    rows.append((dead, dead, dead))
    return minimize(tuple(rows), 0, {sink})


def kirsten_wrapper_with_epsilon(n):
    """DFA for Sigma* c {epsilon} union K c Sigma*, K=closed path walks."""
    # 0..n-1: before c and tracking K; n: prefix was in K, hence accepting
    # sink after c; n+1: prefix not in K, accepts only immediately after c;
    # n+2: dead.  All words have exactly one c.
    sigma = ("a", "b", "c")
    good, eps_only, dead = n, n + 1, n + 2
    rows = []
    for q in range(n):
        row = []
        for a in sigma[:2]:
            target = dead
            if q > 0 and sigma[(q - 1) % 2] == a:
                target = q - 1
            if q + 1 < n and sigma[q % 2] == a:
                target = q + 1
            row.append(target)
        row.append(good if q == 0 else eps_only)
        rows.append(tuple(row))
    rows.append((good, good, dead))
    rows.append((dead, dead, dead))
    rows.append((dead, dead, dead))
    return minimize(tuple(rows), 0, {good, eps_only})


def reverse_columns(transitions, finals):
    """Reachable right-context columns as subsets of forward states."""
    start = frozenset(finals)
    cols = [start]
    index = {start: 0}
    for col in cols:
        for letter in range(len(transitions[0])):
            pred = frozenset(p for p, row in enumerate(transitions)
                             if row[letter] >= 0 and row[letter] in col)
            if pred not in index:
                index[pred] = len(cols)
                cols.append(pred)
    return cols


def core(transitions, finals):
    """Intersection of canonical forward/backward images in the concept automaton."""
    cols = reverse_columns(transitions, finals)
    all_col_ids = frozenset(range(len(cols)))

    def up(rows):
        return frozenset(i for i, col in enumerate(cols) if rows <= col)

    def down(col_ids):
        if not col_ids:
            return frozenset(range(len(transitions)))
        return frozenset.intersection(*(cols[i] for i in col_ids))

    fwd = []
    for p in range(len(transitions)):
        intent = up(frozenset({p}))
        fwd.append((down(intent), intent))
    back = [(col, up(col)) for col in cols]

    # Common labelled transitions, first represented by concept-pairs.
    ft = set()
    for p, row in enumerate(transitions):
        for a, target in enumerate(row):
            if target >= 0:
                ft.add((fwd[p], a, fwd[target]))
    bt = set()
    for j, col in enumerate(cols):
        for a in range(len(transitions[0])):
            pred = frozenset(p for p, row in enumerate(transitions)
                             if row[a] >= 0 and row[a] in col)
            i = cols.index(pred)
            bt.add((back[i], a, back[j]))
    common = ft & bt
    concepts = sorted({x for x, _, _ in common} | {y for _, _, y in common},
                      key=repr)
    pos = {x: i for i, x in enumerate(concepts)}
    adjacency = [set() for _ in concepts]
    for x, _, y in common:
        adjacency[pos[x]].add(pos[y])
    # cycle_rank expects a tuple of rows; duplicate destinations are harmless.
    return len(cols), len(concepts), cycle_rank(tuple(tuple(x) for x in adjacency)), common


def main():
    for constructor in (symmetric_path_closed_walks_then_delimiter,
                        kirsten_wrapper_with_epsilon):
        print(constructor.__name__)
        for n in range(2, 17):
            transitions, start, finals = constructor(n)
            rev, cstates, rank, _ = core(transitions, finals)
            print(n, "dfa", len(transitions), "reverse", rev,
                  "core-states", cstates, "core-rank", rank)


if __name__ == "__main__":
    main()
