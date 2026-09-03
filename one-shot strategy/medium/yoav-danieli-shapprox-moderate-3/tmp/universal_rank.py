"""Compute the formal-concept universal automaton of a small minimal DFA.

For a DFA state set Q and the family C of reachable reverse columns, the
closed extents are S'' = intersection{C in C : S subseteq C}.  The saturated
transition relation has X -a-> Y iff delta(X,a) subseteq Y.  We trim from all
closed extents containing the initial state to all extents contained in F.
This is only intended for small counterexample exploration.
"""

from collections import deque
from itertools import combinations

from core_explore import reverse_columns
from search_rank import cycle_rank, minimize
from bounded_subset_rank import rank_at_most


F_WORDS = {"aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab"}


def trie_star(words):
    """Subset/minimize the usual reset-to-root trie NFA for F*."""
    # NFA trie, state 0 root; terminal states epsilon-jump to root.
    children = [{}]
    terminal = set()
    for word in words:
        q = 0
        for ch in word:
            a = ord(ch) - ord("a")
            if a not in children[q]:
                children[q][a] = len(children)
                children.append({})
            q = children[q][a]
        terminal.add(q)

    def closure(S):
        return frozenset(set(S) | ({0} if set(S) & terminal else set()))

    start = closure({0})
    subsets = [start]
    index = {start: 0}
    rows = []
    for S in subsets:
        row = []
        for a in range(2):
            T = closure({children[q][a] for q in S if a in children[q]})
            if T not in index:
                index[T] = len(subsets)
                subsets.append(T)
            row.append(index[T])
        rows.append(tuple(row))
    accepting = {i for i, S in enumerate(subsets) if 0 in S}
    return minimize(tuple(rows), 0, accepting)


def closed_extents(transitions, finals):
    cols = reverse_columns(transitions, finals)
    allq = frozenset(range(len(transitions)))

    def close(S):
        containing = [C for C in cols if S <= C]
        return frozenset.intersection(*containing) if containing else allq

    return sorted({close(frozenset(S))
                   for r in range(len(transitions) + 1)
                   for S in combinations(range(len(transitions)), r)},
                  key=lambda X: (len(X), tuple(X)))


def universal_graph(transitions, start, finals):
    extents = closed_extents(transitions, finals)
    initial = {i for i, X in enumerate(extents) if start in X}
    final = {i for i, X in enumerate(extents) if X <= finals}
    rows = [set() for _ in extents]
    reverse = [set() for _ in extents]
    for i, X in enumerate(extents):
        for a in range(len(transitions[0])):
            image = {transitions[q][a] for q in X}
            for j, Y in enumerate(extents):
                if image <= Y:
                    rows[i].add(j)
                    reverse[j].add(i)

    reachable = set(initial)
    todo = list(initial)
    while todo:
        i = todo.pop()
        for j in rows[i]:
            if j not in reachable:
                reachable.add(j)
                todo.append(j)
    coacc = set(final)
    todo = list(final)
    while todo:
        j = todo.pop()
        for i in reverse[j]:
            if i not in coacc:
                coacc.add(i)
                todo.append(i)
    keep = sorted(reachable & coacc)
    pos = {old: new for new, old in enumerate(keep)}
    trimmed = tuple(tuple(pos[j] for j in rows[i] if j in pos) for i in keep)
    return extents, keep, trimmed


def main():
    trans, start, finals = trie_star(F_WORDS)
    extents, keep, graph = universal_graph(trans, start, finals)
    print("DFA", len(trans), "concepts", len(extents), "trim", len(keep))
    print("rank", cycle_rank(graph))
    print("graph", graph)
    print("delete ranks", [cycle_rank(tuple(tuple((w - (1 if w > v else 0))
                                                   for w in row if w != v)
                                             for i, row in enumerate(graph) if i != v))
                           for v in range(len(graph))])
    for i in keep:
        print(i, sorted(extents[i]))

    # Canonical morphic image of the rank-one reset-trie NFA.  A trie state
    # maps to the least closed extent containing all minimal-DFA states reached
    # by prefixes in its past.  Keep only the image of actual trie edges.
    children = [{}]
    terminal = set()
    for word in F_WORDS:
        q = 0
        for ch in word:
            a = ord(ch) - ord("a")
            if a not in children[q]:
                children[q][a] = len(children)
                children.append({})
            q = children[q][a]
        terminal.add(q)
    pairs = {(start, 0)}
    todo = list(pairs)
    while todo:
        p, b = todo.pop()
        generated = []
        if b in terminal:
            generated.append((p, 0))
        for a, c in children[b].items():
            generated.append((trans[p][a], c))
        for pair in generated:
            if pair not in pairs:
                pairs.add(pair)
                todo.append(pair)
    P = [{p for p, c in pairs if c == b} for b in range(len(children))]
    extent_pos = {X: i for i, X in enumerate(extents)}
    cols = reverse_columns(trans, finals)
    allq = frozenset(range(len(trans)))

    def close(S):
        containing = [C for C in cols if set(S) <= C]
        return frozenset.intersection(*containing) if containing else allq

    phi = [extent_pos[close(S)] for S in P]
    image_states = sorted(set(phi))
    image_pos = {q: i for i, q in enumerate(image_states)}
    image_rows = [set() for _ in image_states]
    for b in range(len(children)):
        i = image_pos[phi[b]]
        if b in terminal:
            image_rows[i].add(image_pos[phi[0]])
        for c in children[b].values():
            image_rows[i].add(image_pos[phi[c]])
    image_graph = tuple(tuple(row) for row in image_rows)
    print("trie canonical image states", len(image_graph),
          "rank", cycle_rank(image_graph), "map", phi)


if __name__ == "__main__":
    main()
