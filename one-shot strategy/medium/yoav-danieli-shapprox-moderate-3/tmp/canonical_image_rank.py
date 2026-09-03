"""Stress-test ranks of canonical images of reset-trie NFAs for F*."""

from collections import deque
from itertools import product
import random

from core_explore import reverse_columns
from search_rank import dictionary_star_dfa, minimize, cycle_rank


CASES = {
    "rank3": ("aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab"),
    "rank4": ("aab", "aabb", "abb", "abba", "b", "baaab", "baaba", "bab", "baba", "bbaa", "bbaaa", "bbbaa"),
}


def canonical_image(words, bouquet=False, details=False):
    dfa, start, finals = minimize(*dictionary_star_dfa(words))
    if bouquet:
        # Letter-only rank-one NFA: one common accepting hub, and a disjoint
        # directed cycle spelling each generator word.  Edges are relations.
        children = [dict()]
        for word in words:
            q = 0
            for i, ch in enumerate(word):
                target = 0 if i + 1 == len(word) else len(children)
                if target != 0:
                    children.append({})
                children[q].setdefault(ch, set()).add(target)
                q = target
        terminal = set()
    else:
        # Shared reset trie with epsilon edges, used only as the earlier
        # diagnostic; bouquet=True is the ordinary letter-NFA construction.
        children = [{}]
        terminal = set()
        for word in words:
            q = 0
            for ch in word:
                if ch not in children[q]:
                    children[q][ch] = len(children)
                    children.append({})
                q = children[q][ch]
            terminal.add(q)

    # Reachable pairs (minimal-DFA state, trie-NFA state), with epsilon resets.
    pairs = {(start, 0)}
    todo = list(pairs)
    while todo:
        p, b = todo.pop()
        successors = []
        if b in terminal:
            successors.append((p, 0))
        for ch, targets in children[b].items():
            if not bouquet:
                targets = {targets}
            for c in targets:
                successors.append((dfa[p][ord(ch) - ord("a")], c))
        for pair in successors:
            if pair not in pairs:
                pairs.add(pair)
                todo.append(pair)
    past_sets = [frozenset(p for p, c in pairs if c == b)
                 for b in range(len(children))]

    cols = reverse_columns(dfa, finals)
    allq = frozenset(range(len(dfa)))

    def close(S):
        containing = [C for C in cols if S <= C]
        return frozenset.intersection(*containing) if containing else allq

    phi = [close(S) for S in past_sets]
    states = sorted(set(phi), key=lambda X: (len(X), tuple(X)))
    pos = {X: i for i, X in enumerate(states)}
    rows = [set() for _ in states]
    for b, X in enumerate(phi):
        i = pos[X]
        if b in terminal:
            rows[i].add(pos[phi[0]])
        for targets in children[b].values():
            if not bouquet:
                targets = {targets}
            for c in targets:
                rows[i].add(pos[phi[c]])
    graph = tuple(tuple(row) for row in rows)
    stats = (len(dfa), cycle_rank(dfa), len(children), len(cols),
             len(states), cycle_rank(graph))
    return (stats, graph, states, phi) if details else stats


def induced(graph, omitted):
    keep = [v for v in range(len(graph)) if v not in omitted]
    pos = {v: i for i, v in enumerate(keep)}
    return tuple(tuple(pos[w] for w in graph[v] if w in pos) for v in keep)


def main():
    for name, words in CASES.items():
        print(name, "epsilon-trie", canonical_image(words), flush=True)
        print(name, "bouquet", canonical_image(words, bouquet=True), flush=True)

    candidates = ["".join(x) for length in range(1, 8)
                  for x in product("ab", repeat=length)]
    rng = random.Random(9282026)
    best = (0, None, None)
    for iteration in range(100000):
        words = tuple(sorted(rng.sample(candidates, rng.randint(2, 20))))
        dfa = minimize(*dictionary_star_dfa(words))[0]
        if len(dfa) > 18:
            continue
        stats = canonical_image(words, bouquet=True)
        if stats[-1] > best[0]:
            best = (stats[-1], words, stats)
            print("BEST", best, "iteration", iteration, flush=True)
        if stats[-1] >= 4:
            _, graph, states, phi = canonical_image(words, bouquet=True, details=True)
            print("GRAPH", graph)
            print("DELETE-RANKS", [cycle_rank(induced(graph, {v}))
                                   for v in range(len(graph))])
            break
    if best[0] >= 3:
        _, graph, states, phi = canonical_image(best[1], bouquet=True, details=True)
        print("BEST-GRAPH", graph)
        print("BEST-DELETE-RANKS", [cycle_rank(induced(graph, {v}))
                                    for v in range(len(graph))])
    print("FINAL", best)


if __name__ == "__main__":
    main()
