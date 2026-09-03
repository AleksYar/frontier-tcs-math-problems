"""Map the rank-one trie NFA for F* into subsets of the minimal DFA."""

from collections import deque

from search_rank import dictionary_star_dfa, minimize
from bounded_subset_rank import rank_at_most

F = ("aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab")
SIGMA = "ab"


def trie():
    edges = [dict()]
    terminal = set()
    for word in F:
        q = 0
        for a in word:
            if a not in edges[q]:
                edges[q][a] = len(edges)
                edges.append({})
            q = edges[q][a]
        terminal.add(q)
    return edges, terminal


def main():
    dfa, start, finals = minimize(*dictionary_star_dfa(F))
    edges, terminal = trie()

    def epsilon_close(configs):
        configs = set(configs)
        for p, b in list(configs):
            if b in terminal:
                configs.add((p, 0))
        return configs

    pairs = epsilon_close({(start, 0)})
    todo = deque(pairs)
    while todo:
        p, b = todo.popleft()
        for i, a in enumerate(SIGMA):
            if a not in edges[b]:
                continue
            generated = epsilon_close({(dfa[p][i], edges[b][a])})
            for pair in generated:
                if pair not in pairs:
                    pairs.add(pair)
                    todo.append(pair)
    subsets = [{p for p, c in pairs if c == b} for b in range(len(edges))]
    print("DFA states", len(dfa), "NFA trie states", len(edges))
    print("accepting DFA states", sorted(finals))
    for b, subset in enumerate(subsets):
        print(b, len(subset), sorted(subset))
    print("maximum subset size", max(map(len, subsets)))

    # Transition graph of the singleton-splitting product NFA.
    ordered = sorted(pairs)
    pos = {pair: i for i, pair in enumerate(ordered)}
    adjacency = [set() for _ in ordered]
    for p, b in ordered:
        source = pos[p, b]
        if b in terminal:
            adjacency[source].add(pos[p, 0])
        for i, a in enumerate(SIGMA):
            if a in edges[b]:
                target = (dfa[p][i], edges[b][a])
                adjacency[source].add(pos[target])
    adjacency = tuple(tuple(row) for row in adjacency)
    product_rank = None
    for budget in range(8):
        if rank_at_most(frozenset(range(len(adjacency))), adjacency, budget, {}):
            product_rank = budget
            break
    print("singleton-splitting product states", len(adjacency), "rank", product_rank)


if __name__ == "__main__":
    main()
