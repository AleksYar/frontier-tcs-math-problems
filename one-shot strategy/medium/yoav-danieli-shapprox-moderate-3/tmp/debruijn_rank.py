"""Compute small cycle ranks for the minimal DFA core of Sigma*1Sigma^(m-1)."""

from search_rank import cycle_rank


def graph(m):
    mask = (1 << m) - 1
    return tuple((((v << 1) & mask), ((v << 1) & mask) | 1)
                 for v in range(1 << m))


def main():
    for m in range(1, 6):
        g = graph(m)
        print(m, len(g), cycle_rank(g), flush=True)


if __name__ == "__main__":
    main()
