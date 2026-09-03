from __future__ import annotations

from collections import defaultdict, deque
from functools import lru_cache
from itertools import product
import random


ALPHABET = "ab"


def dictionary_star_dfa(words: tuple[str, ...]):
    """Subset construction for the epsilon-NFA recognizing words*."""
    # Trie vertices; root is both initial/final, and every terminal epsilon-jumps to root.
    nxt: list[dict[str, int]] = [dict()]
    terminals: set[int] = set()
    for word in words:
        q = 0
        for a in word:
            if a not in nxt[q]:
                nxt[q][a] = len(nxt)
                nxt.append({})
            q = nxt[q][a]
        terminals.add(q)

    def close(states):
        states = set(states)
        if states & terminals:
            states.add(0)
        return frozenset(states)

    start = close({0})
    states = [start]
    index = {start: 0}
    transitions = []
    for S in states:
        row = []
        for a in ALPHABET:
            T = close(nxt[q][a] for q in S if a in nxt[q])
            if T not in index:
                index[T] = len(states)
                states.append(T)
            row.append(index[T])
        transitions.append(tuple(row))
    finals = {i for i, S in enumerate(states) if 0 in S}
    return tuple(transitions), 0, finals


def minimize(transitions, start, finals):
    n = len(transitions)
    # Remove the empty/dead state when taking the trim transition graph.
    reverse = [[] for _ in range(n)]
    for q, row in enumerate(transitions):
        for r in row:
            reverse[r].append(q)
    useful = set(finals)
    todo = list(finals)
    while todo:
        q = todo.pop()
        for p in reverse[q]:
            if p not in useful:
                useful.add(p)
                todo.append(p)
    ordered = sorted(useful)
    pos = {q: i for i, q in enumerate(ordered)}
    trans = tuple(tuple(pos.get(r, -1) for r in transitions[q]) for q in ordered)
    finals2 = {pos[q] for q in finals & useful}
    start2 = pos[start]

    partition = [finals2, set(range(len(ordered))) - finals2]
    partition = [b for b in partition if b]
    changed = True
    while changed:
        block_of = {q: i for i, b in enumerate(partition) for q in b}
        refined = []
        for block in partition:
            groups = defaultdict(set)
            for q in block:
                signature = tuple(-1 if r < 0 else block_of[r] for r in trans[q])
                groups[signature].add(q)
            refined.extend(groups.values())
        changed = len(refined) != len(partition)
        partition = refined
    block_of = {q: i for i, b in enumerate(partition) for q in b}
    out = []
    for block in partition:
        q = next(iter(block))
        out.append(tuple(-1 if r < 0 else block_of[r] for r in trans[q]))
    return tuple(out), block_of[start2], {block_of[q] for q in finals2}


def sccs(vertices: frozenset[int], adj):
    vertices_set = set(vertices)
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    low = {}
    answer = []

    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj[v]:
            if w not in vertices_set:
                continue
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.add(w)
                if w == v:
                    break
            answer.append(frozenset(comp))

    for v in vertices:
        if v not in indices:
            visit(v)
    return answer


def cycle_rank(transitions):
    adj = [set(r for r in row if r >= 0) for row in transitions]

    @lru_cache(None)
    def rank(vertices: frozenset[int]):
        if not vertices:
            return 0
        comps = sccs(vertices, adj)
        cyclic = []
        for c in comps:
            if len(c) > 1 or any(v in adj[v] for v in c):
                cyclic.append(c)
        if not cyclic:
            return 0
        if len(comps) > 1:
            return max(rank(c) for c in cyclic)
        return 1 + min(rank(vertices - {v}) for v in vertices)

    return rank(frozenset(range(len(transitions))))


def main():
    candidates = ["".join(x) for length in range(1, 6) for x in product(ALPHABET, repeat=length)]
    rng = random.Random(20260828)
    best = (0, None, None)
    for iteration in range(30000):
        size = rng.randint(2, 12)
        words = tuple(sorted(rng.sample(candidates, size)))
        dfa = minimize(*dictionary_star_dfa(words))
        n = len(dfa[0])
        if n > 22:
            continue
        rank = cycle_rank(dfa[0])
        if rank > best[0]:
            best = (rank, words, dfa)
            print("BEST", rank, "states", n, "words", words, "trans", dfa[0], flush=True)
        if rank >= 4:
            break
    print("FINAL", best)

    # A second pass minimizes the number of trim minimal-DFA states among rank-3 examples.
    candidates2 = ["".join(x) for length in range(1, 5) for x in product(ALPHABET, repeat=length)]
    best3 = (10**9, None, None)
    for iteration in range(200000):
        size = rng.randint(2, 10)
        words = tuple(sorted(rng.sample(candidates2, size)))
        dfa = minimize(*dictionary_star_dfa(words))
        n = len(dfa[0])
        if n >= best3[0] or n > 18:
            continue
        rank = cycle_rank(dfa[0])
        if rank >= 3:
            best3 = (n, words, dfa)
            print("SMALL-RANK3", n, words, dfa[0], flush=True)
    print("FINAL-SMALL-RANK3", best3)


if __name__ == "__main__":
    main()
