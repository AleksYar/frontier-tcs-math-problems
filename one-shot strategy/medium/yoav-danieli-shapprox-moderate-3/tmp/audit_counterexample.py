"""Independent certificates for the F* counterexample in WORKLOG.md."""

from collections import deque

F = {"aa", "aaa", "aaab", "aaba", "ab", "abab", "abba", "b", "bbab"}
SIGMA = "ab"


def in_f_star(word: str) -> bool:
    """Direct word-break recurrence, independent of the trie subset code."""
    cut = [False] * (len(word) + 1)
    cut[0] = True
    for j in range(1, len(word) + 1):
        cut[j] = any(cut[j - len(x)] and word[j - len(x):j] == x
                     for x in F if len(x) <= j)
    return cut[-1]


T = (
    (6, 0),
    (6, 5),
    (4, 5),
    (3, 2),
    (3, 1),
    (4, 0),
    (2, 1),
)
FINAL = set(range(6))


def run(word: str) -> int:
    q = 0
    for letter in word:
        q = T[q][SIGMA.index(letter)]
    return q


def main() -> None:
    # Reachability representatives.
    rep = {0: ""}
    todo = deque([0])
    while todo:
        q = todo.popleft()
        for i, a in enumerate(SIGMA):
            r = T[q][i]
            if r not in rep:
                rep[r] = rep[q] + a
                todo.append(r)

    # Shortest distinguishing suffix for each unordered state pair.
    witness = {}
    pair_todo = deque()
    for p in range(7):
        for q in range(p + 1, 7):
            if (p in FINAL) != (q in FINAL):
                witness[p, q] = ""
                pair_todo.append((p, q))
    predecessors = {(p, q): [] for p in range(7) for q in range(p + 1, 7)}
    for p in range(7):
        for q in range(p + 1, 7):
            for i, a in enumerate(SIGMA):
                x, y = sorted((T[p][i], T[q][i]))
                if x != y:
                    predecessors[x, y].append(((p, q), a))
    while pair_todo:
        pair = pair_todo.popleft()
        for prior, a in predecessors[pair]:
            if prior not in witness:
                witness[prior] = a + witness[pair]
                pair_todo.append(prior)

    assert len(rep) == 7
    assert len(witness) == 21
    # Check the proposed DFA and F* independently through length 18.  This is
    # not the proof of equality; equality follows from the standard residual
    # subset construction.  It is an adversarial implementation cross-check.
    words = [""]
    for _ in range(18):
        words += [w + a for w in words.copy() if len(w) == _ for a in SIGMA]
    assert all((run(w) in FINAL) == in_f_star(w) for w in words)

    print("reachable representatives")
    for q in range(7):
        print(q, repr(rep[q]))
    print("distinguishing suffixes")
    for pair in sorted(witness):
        suffix = witness[pair]
        p, q = pair
        assert ((run(rep[p] + suffix) in FINAL) !=
                (run(rep[q] + suffix) in FINAL))
        print(pair, repr(suffix))


if __name__ == "__main__":
    main()
