"""Audit a reversal-invariant height-one language with DFA rank > 2."""

from collections import deque

from search_rank import dictionary_star_dfa, minimize, cycle_rank


F = ("aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab")


def reverse_dfa(rows, start, finals):
    S0 = frozenset(finals)
    subsets = [S0]
    pos = {S0: 0}
    out = []
    for S in subsets:
        row = []
        for a in range(len(rows[0])):
            P = frozenset(q for q, trans in enumerate(rows)
                          if trans[a] >= 0 and trans[a] in S)
            if P not in pos:
                pos[P] = len(subsets)
                subsets.append(P)
            row.append(pos[P])
        out.append(tuple(row))
    accepting = {i for i, S in enumerate(subsets) if start in S}
    return minimize(tuple(out), 0, accepting)


def tagged_union(A, AR):
    """Partial DFA for c L(A) d union d L(AR) c over a,b,c,d."""
    rows1, s1, f1 = A
    rows2, s2, f2 = AR
    start = 0
    off1 = 1
    off2 = off1 + len(rows1)
    final = off2 + len(rows2)
    rows = [(-1, -1, off1 + s1, off2 + s2)]
    for q, row in enumerate(rows1):
        rows.append((off1 + row[0] if row[0] >= 0 else -1,
                     off1 + row[1] if row[1] >= 0 else -1,
                     -1, final if q in f1 else -1))
    for q, row in enumerate(rows2):
        rows.append((off2 + row[0] if row[0] >= 0 else -1,
                     off2 + row[1] if row[1] >= 0 else -1,
                     final if q in f2 else -1, -1))
    rows.append((-1, -1, -1, -1))
    return minimize(tuple(rows), start, {final})


def main():
    A = minimize(*dictionary_star_dfa(F))
    AR = reverse_dfa(*A)
    C = tagged_union(A, AR)
    CR = reverse_dfa(*C)
    print("A states/rank", len(A[0]), cycle_rank(A[0]))
    print("AR states/rank", len(AR[0]), cycle_rank(AR[0]))
    print("tagged states/rank", len(C[0]), cycle_rank(C[0]))
    print("tagged reverse states/rank", len(CR[0]), cycle_rank(CR[0]))
    print("same minimized transition counts", len(C[0]) == len(CR[0]))


if __name__ == "__main__":
    main()
