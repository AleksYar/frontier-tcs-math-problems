"""Cycle-rank tests for canonical NFAs using bounded-size DFA-state subsets."""

from collections import deque
from itertools import combinations

from search_rank import dictionary_star_dfa, minimize, sccs


def bounded_subset_nfa(dfa, start, finals, bound):
    n = len(dfa)
    states = [frozenset(c) for size in range(1, bound + 1)
              for c in combinations(range(n), size)]
    pos = {s: i for i, s in enumerate(states)}
    adj = [set() for _ in states]
    labelled = [[] for _ in states]
    for i, source in enumerate(states):
        for a in range(len(dfa[0])):
            image = frozenset(dfa[q][a] for q in source if dfa[q][a] >= 0)
            targets = []
            if image:
                targets = [j for j, target in enumerate(states) if image <= target]
            labelled[i].append(targets)
            adj[i].update(targets)
    initials = {pos[frozenset({start})]}
    accepting = {i for i, state in enumerate(states) if state <= finals}

    reachable = set(initials)
    todo = list(initials)
    while todo:
        q = todo.pop()
        for r in adj[q]:
            if r not in reachable:
                reachable.add(r)
                todo.append(r)
    reverse = [[] for _ in states]
    for q in reachable:
        for r in adj[q]:
            reverse[r].append(q)
    useful = accepting & reachable
    todo = list(useful)
    while todo:
        q = todo.pop()
        for p in reverse[q]:
            if p not in useful:
                useful.add(p)
                todo.append(p)
    ordered = sorted(useful)
    rename = {q: i for i, q in enumerate(ordered)}
    trim_adj = tuple(tuple(rename[r] for r in adj[q] if r in useful) for q in ordered)
    return trim_adj


def is_acyclic(vertices, adj):
    colour = {}

    def visit(v):
        colour[v] = 1
        for w in adj[v]:
            if w not in vertices:
                continue
            if colour.get(w) == 1:
                return False
            if colour.get(w, 0) == 0 and not visit(w):
                return False
        colour[v] = 2
        return True

    return all(colour.get(v, 0) or visit(v) for v in vertices)


def rank_at_most(vertices, adj, budget, memo):
    key = (vertices, budget)
    if key in memo:
        return memo[key]
    if is_acyclic(vertices, adj):
        memo[key] = True
        return True
    if budget == 0:
        memo[key] = False
        return False
    components = sccs(vertices, adj)
    cyclic = [c for c in components if not is_acyclic(c, adj)]
    if len(components) > 1:
        result = all(rank_at_most(c, adj, budget, memo) for c in cyclic)
    else:
        result = any(rank_at_most(vertices - {v}, adj, budget - 1, memo)
                     for v in vertices)
    memo[key] = result
    return result


def test(words, max_bound=3, max_rank=4):
    dfa, start, finals = minimize(*dictionary_star_dfa(tuple(sorted(words))))
    print("F", sorted(words), "minimal DFA", len(dfa))
    for bound in range(1, max_bound + 1):
        adj = bounded_subset_nfa(dfa, start, finals, bound)
        values = []
        for rank in range(max_rank + 1):
            if rank_at_most(frozenset(range(len(adj))), adj, rank, {}):
                values.append(rank)
                break
        print(" subset bound", bound, "trim states", len(adj),
              "rank", values[0] if values else f">{max_rank}")


def main():
    test({"aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab"})
    test({"aab", "aabb", "abb", "abba", "b", "baaab", "baaba", "bab",
          "baba", "bbaa", "bbaaa", "bbbaa"}, max_bound=2)


if __name__ == "__main__":
    main()
