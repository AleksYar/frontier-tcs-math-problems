"""Audit the strongly-connected height-one/exponential-reversal family."""

from collections import deque


def reset_dfa(m):
    # State (ell, bit): ell is length clipped at 2m+1; bit is the symbol at
    # position m once seen.  Before position m use bit=-1.
    states = []
    for ell in range(m):
        states.append((ell, -1))
    for ell in range(m, 2 * m + 1):
        states.extend([(ell, 0), (ell, 1)])
    states.append((2 * m + 1, 0))  # overlength dead before the next reset
    pos = {s: i for i, s in enumerate(states)}
    q0 = pos[0, -1]
    rows = []
    for ell, bit in states:
        row = []
        for x in (0, 1):
            if ell == 2 * m + 1:
                target = (2 * m + 1, 0)
            elif ell + 1 == m:
                target = (m, x)
            elif ell + 1 > 2 * m:
                target = (2 * m + 1, 0)
            else:
                target = (ell + 1, bit)
            row.append(pos[target])
        row.append(q0)  # reset letter c
        rows.append(tuple(row))
    finals = {pos[ell, 1] for ell in range(m, 2 * m + 1)}
    return tuple(rows), q0, finals


def reverse_subset_count(rows, finals):
    start = frozenset(finals)
    seen = {start}
    todo = deque([start])
    while todo:
        S = todo.popleft()
        for a in range(3):
            P = frozenset(q for q, row in enumerate(rows) if row[a] in S)
            if P not in seen:
                seen.add(P)
                todo.append(P)
    return len(seen)


def strongly_connected(rows):
    n = len(rows)
    for source in range(n):
        seen = {source}
        todo = [source]
        while todo:
            q = todo.pop()
            for p in rows[q]:
                if p not in seen:
                    seen.add(p)
                    todo.append(p)
        if len(seen) != n:
            return False
    return True


def main():
    for m in range(1, 9):
        rows, q0, finals = reset_dfa(m)
        print(m, "forward", len(rows), "SC", strongly_connected(rows),
              "reverse subsets", reverse_subset_count(rows, finals),
              "lower bound", 2 ** m)


if __name__ == "__main__":
    main()
