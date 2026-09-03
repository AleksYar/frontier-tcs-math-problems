from __future__ import annotations

from functools import lru_cache
from itertools import combinations
import random


def sccs(mask: int, out: tuple[int, ...]) -> list[int]:
    """Tarjan SCC masks for the subgraph induced by mask."""
    n = len(out)
    index = 0
    indices = [-1] * n
    low = [0] * n
    stack: list[int] = []
    onstack = [False] * n
    ans: list[int] = []

    def dfs(v: int) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        onstack[v] = True
        nbrs = out[v] & mask
        while nbrs:
            bit = nbrs & -nbrs
            nbrs -= bit
            w = bit.bit_length() - 1
            if indices[w] == -1:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif onstack[w]:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp = 0
            while True:
                w = stack.pop()
                onstack[w] = False
                comp |= 1 << w
                if w == v:
                    break
            ans.append(comp)

    todo = mask
    while todo:
        bit = todo & -todo
        todo -= bit
        v = bit.bit_length() - 1
        if indices[v] == -1:
            dfs(v)
    return ans


def has_cycle(comp: int, out: tuple[int, ...]) -> bool:
    if comp & (comp - 1):
        return True
    v = comp.bit_length() - 1
    return bool(out[v] & comp)


def cycle_rank(out: tuple[int, ...]) -> int:
    @lru_cache(None)
    def rank(mask: int) -> int:
        cyclic = [c for c in sccs(mask, out) if has_cycle(c, out)]
        if not cyclic:
            return 0
        if len(cyclic) != 1 or cyclic[0] != mask:
            return max(rank(c) for c in cyclic)
        return 1 + min(rank(mask & ~(1 << v)) for v in range(len(out)) if mask >> v & 1)

    return rank((1 << len(out)) - 1)


def elimination_height(out: tuple[int, ...], order: list[int]) -> int:
    """Boolean support plus maximum regex star height on each current edge."""
    n = len(out)
    edge: list[list[int | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        nbrs = out[i]
        while nbrs:
            bit = nbrs & -nbrs
            nbrs -= bit
            edge[i][bit.bit_length() - 1] = 0
    alive = set(range(n))
    answer = 0
    for v in order:
        loop = edge[v][v]
        loop_star = 0 if loop is None else loop + 1
        answer = max(answer, loop_star)
        incoming = [i for i in alive if i != v and edge[i][v] is not None]
        outgoing = [j for j in alive if j != v and edge[v][j] is not None]
        for i in incoming:
            for j in outgoing:
                candidate = max(edge[i][v] or 0, loop_star, edge[v][j] or 0)
                old = edge[i][j]
                edge[i][j] = candidate if old is None else max(old, candidate)
        alive.remove(v)
    return answer


def choose_order(out: tuple[int, ...], rule: str) -> list[int]:
    n = len(out)
    support = [list(row) for row in [[bool(out[i] >> j & 1) for j in range(n)] for i in range(n)]]
    alive = set(range(n))
    order: list[int] = []
    while alive:
        def score(v: int):
            indeg = sum(support[i][v] for i in alive if i != v)
            outdeg = sum(support[v][j] for j in alive if j != v)
            if rule == "min_product":
                return (indeg * outdeg, indeg + outdeg, v)
            if rule == "min_degree":
                return (indeg + outdeg, v)
            if rule == "max_degree":
                return (-(indeg + outdeg), v)
            raise ValueError(rule)
        v = min(alive, key=score)
        incoming = [i for i in alive if i != v and support[i][v]]
        outgoing = [j for j in alive if j != v and support[v][j]]
        for i in incoming:
            for j in outgoing:
                support[i][j] = True
        alive.remove(v)
        order.append(v)
    return order


def symmetric_out(n: int, edges: list[tuple[int, int]]) -> tuple[int, ...]:
    out = [0] * n
    for u, v in edges:
        out[u] |= 1 << v
        out[v] |= 1 << u
    return tuple(out)


def path(n: int) -> tuple[int, ...]:
    return symmetric_out(n, [(i, i + 1) for i in range(n - 1)])


def star(n: int) -> tuple[int, ...]:
    return symmetric_out(n, [(0, i) for i in range(1, n)])


def random_connected(n: int, p: float) -> tuple[int, ...]:
    edges = [(i, i + 1) for i in range(n - 1)]
    present = set(edges)
    for i, j in combinations(range(n), 2):
        if (i, j) not in present and random.random() < p:
            edges.append((i, j))
    random.shuffle(edges)
    return symmetric_out(n, edges)


@lru_cache(None)
def separable_orders(vertices: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """All leaf orders obtained by swapping children in a fixed balanced tree."""
    if len(vertices) <= 1:
        return (vertices,)
    cut = len(vertices) // 2
    left = separable_orders(vertices[:cut])
    right = separable_orders(vertices[cut:])
    ans = set()
    for a in left:
        for b in right:
            ans.add(a + b)
            ans.add(b + a)
    return tuple(ans)


def relabel(out: tuple[int, ...], permutation: list[int]) -> tuple[int, ...]:
    """New label i is old vertex permutation[i]."""
    n = len(out)
    old_to_new = {old: new for new, old in enumerate(permutation)}
    ans = [0] * n
    for new, old in enumerate(permutation):
        nbrs = out[old]
        while nbrs:
            bit = nbrs & -nbrs
            nbrs -= bit
            ans[new] |= 1 << old_to_new[bit.bit_length() - 1]
    return tuple(ans)


def min_separable_height(out: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    best = len(out) + 1
    best_order: tuple[int, ...] = ()
    for order in separable_orders(tuple(range(len(out)))):
        h = elimination_height(out, list(order))
        if h < best:
            best, best_order = h, order
    return best, best_order


def induced_relabel(out: tuple[int, ...], vertices: list[int]) -> tuple[int, ...]:
    old_to_new = {old: new for new, old in enumerate(vertices)}
    ans = [0] * len(vertices)
    kept = set(vertices)
    for new, old in enumerate(vertices):
        nbrs = out[old]
        while nbrs:
            bit = nbrs & -nbrs
            nbrs -= bit
            old_j = bit.bit_length() - 1
            if old_j in kept:
                ans[new] |= 1 << old_to_new[old_j]
    return tuple(ans)


def torso_after(out: tuple[int, ...], eliminated: set[int], survivors: list[int]) -> tuple[int, ...]:
    """Boolean Schur complement support on survivors after eliminating a set."""
    n = len(out)
    edge = [[bool(out[i] >> j & 1) for j in range(n)] for i in range(n)]
    alive = set(range(n))
    for v in eliminated:
        incoming = [i for i in alive if i != v and edge[i][v]]
        outgoing = [j for j in alive if j != v and edge[v][j]]
        loop = edge[v][v]
        # Boolean support is unchanged by whether the loop exists: one passage suffices.
        for i in incoming:
            for j in outgoing:
                edge[i][j] = True
        alive.remove(v)
    ans = [0] * len(survivors)
    for i, old_i in enumerate(survivors):
        for j, old_j in enumerate(survivors):
            if edge[old_i][old_j]:
                ans[i] |= 1 << j
    return tuple(ans)


def split_rank_sums(out: tuple[int, ...]) -> tuple[int, int]:
    n = len(out)
    cut = n // 2
    a, b = list(range(cut)), list(range(cut, n))
    a_first = cycle_rank(induced_relabel(out, a)) + cycle_rank(torso_after(out, set(a), b))
    b_first = cycle_rank(induced_relabel(out, b)) + cycle_rank(torso_after(out, set(b), a))
    return a_first, b_first


def layered_with_cycles(p: int, layers: int, branches_per_layer: int = 1) -> tuple[tuple[int, ...], list[list[int]], list[list[tuple[int, int]]]]:
    """Directed layered core, with private directed 2-cycles returning to layer zero."""
    total_layer_vertices = p * layers
    total = total_layer_vertices + 2 * branches_per_layer * layers
    out = [0] * total
    layer_sets = [list(range(i * p, (i + 1) * p)) for i in range(layers)]
    branches: list[list[tuple[int, int]]] = []
    nxt = total_layer_vertices
    for i in range(layers - 1):
        for u in layer_sets[i]:
            for v in layer_sets[i + 1]:
                out[u] |= 1 << v
    for i in range(1, layers):
        for u in layer_sets[i]:
            for v in layer_sets[0]:
                out[u] |= 1 << v
    for i in range(layers):
        here = []
        for _ in range(branches_per_layer):
            x, y = nxt, nxt + 1
            nxt += 2
            out[x] |= 1 << y
            out[y] |= 1 << x
            for u in layer_sets[i]:
                out[u] |= 1 << x
            for v in layer_sets[0]:
                out[y] |= 1 << v
            here.append((x, y))
        branches.append(here)
    return tuple(out), layer_sets, branches


def feedback_vertex_number(out: tuple[int, ...]) -> int:
    n = len(out)
    full = (1 << n) - 1
    for k in range(n + 1):
        for chosen in combinations(range(n), k):
            mask = full
            for v in chosen:
                mask &= ~(1 << v)
            if not any(has_cycle(c, out) for c in sccs(mask, out)):
                return k
    raise AssertionError


def undirected_components(mask: int, out: tuple[int, ...]) -> list[int]:
    comps = []
    todo = mask
    while todo:
        seed = todo & -todo
        seen = seed
        frontier = seed
        while frontier:
            bit = frontier & -frontier
            frontier -= bit
            v = bit.bit_length() - 1
            add = out[v] & mask & ~seen
            seen |= add
            frontier |= add
        comps.append(seen)
        todo &= ~seen
    return comps


def order_tree_height(mask: int, order: tuple[int, ...], out: tuple[int, ...]) -> int:
    if not mask:
        return 0
    position = {v: i for i, v in enumerate(order)}

    @lru_cache(None)
    def rec(cur: int) -> int:
        if not cur:
            return 0
        comps = undirected_components(cur, out)
        if len(comps) > 1:
            return max(rec(c) for c in comps)
        root = max((v for v in range(len(out)) if cur >> v & 1), key=position.get)
        return 1 + rec(cur & ~(1 << root))
    return rec(mask)


def root_local_search(out: tuple[int, ...], initial: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Coordinate descent: change the root of any current recursive subproblem, preserving other priorities."""
    n = len(out)
    order = list(initial)
    full = (1 << n) - 1
    changed = True
    while changed:
        changed = False
        # Try promoting each vertex to be globally last; this is weaker than all subtree moves
        # but suffices to look for obvious traps.
        current_h = order_tree_height(full, tuple(order), out)
        best = (current_h, tuple(order))
        for v in range(n):
            candidate = tuple(x for x in order if x != v) + (v,)
            h = order_tree_height(full, candidate, out)
            if h < best[0]:
                best = (h, candidate)
        if best[0] < current_h:
            order = list(best[1])
            changed = True
    return order_tree_height(full, tuple(order), out), tuple(order)


def single_vertex_balance_height(out: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Recursively choose a root minimizing the largest residual component.

    Ties prefer larger current degree, then the sum of squared component sizes.
    This is a polynomial heuristic whose possible approximation behavior is being tested.
    """
    order: list[int] = []

    def rec(mask: int) -> int:
        if not mask:
            return 0
        comps = undirected_components(mask, out)
        if len(comps) > 1:
            return max(rec(c) for c in comps)

        def score(v: int) -> tuple[int, int, int, int]:
            residual = mask & ~(1 << v)
            sizes = sorted((bin(c).count("1") for c in undirected_components(residual, out)), reverse=True)
            largest = sizes[0] if sizes else 0
            degree = bin(out[v] & mask).count("1")
            return largest, -degree, sum(s * s for s in sizes), v

        root = min((v for v in range(len(out)) if mask >> v & 1), key=score)
        child_height = rec(mask & ~(1 << root))
        order.append(root)
        return 1 + child_height

    height = rec((1 << len(out)) - 1)
    return height, tuple(order)


def exhaustive_balance_probe(n: int) -> tuple[float, object]:
    """Enumerate all labeled undirected graphs on n vertices (n <= 6 is practical)."""
    pairs = list(combinations(range(n), 2))
    worst: tuple[float, object] = (0.0, None)
    for bits in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if bits >> i & 1]
        graph = symmetric_out(n, edges)
        td = cycle_rank(graph) + (1 if n else 0)
        h, order = single_vertex_balance_height(graph)
        ratio = h / max(td, 1)
        if ratio > worst[0]:
            worst = ratio, (graph, td, h, order)
    return worst


def clique_separator_torso(out: tuple[int, ...], separator: int, component: int) -> tuple[int, ...]:
    vertices = [v for v in range(len(out)) if (separator | component) >> v & 1]
    torso = list(induced_relabel(out, vertices))
    positions = [i for i, v in enumerate(vertices) if separator >> v & 1]
    for i in positions:
        for j in positions:
            if i != j:
                torso[i] |= 1 << j
    return tuple(torso)


def minimal_global_separator(mask: int, full: int, out: tuple[int, ...]) -> bool:
    if mask == 0 or len(undirected_components(full & ~mask, out)) <= 1:
        return False
    bits = mask
    while bits:
        bit = bits & -bits
        bits -= bit
        if len(undirected_components(full & ~(mask & ~bit), out)) > 1:
            return False
    return True


def exhaustive_torso_probe(n: int, minimum_cardinality_only: bool = False) -> object:
    pairs = list(combinations(range(n), 2))
    full = (1 << n) - 1
    for edge_bits in range(1 << len(pairs)):
        edges = [pairs[i] for i in range(len(pairs)) if edge_bits >> i & 1]
        graph = symmetric_out(n, edges)
        if len(undirected_components(full, graph)) != 1:
            continue
        td = cycle_rank(graph) + 1
        separators = [separator for separator in range(1, full)
                      if minimal_global_separator(separator, full, graph)]
        if minimum_cardinality_only and separators:
            minimum_size = min(bin(separator).count("1") for separator in separators)
            separators = [separator for separator in separators
                          if bin(separator).count("1") == minimum_size]
        for separator in separators:
            for component in undirected_components(full & ~separator, graph):
                torso = clique_separator_torso(graph, separator, component)
                torso_td = cycle_rank(torso) + 1
                if torso_td > td:
                    return graph, td, separator, component, torso, torso_td
    return None


def exhaustive_no_good_minimum_separator(n: int) -> object:
    pairs = list(combinations(range(n), 2))
    full = (1 << n) - 1
    for edge_bits in range(1 << len(pairs)):
        graph = symmetric_out(n, [pairs[i] for i in range(len(pairs)) if edge_bits >> i & 1])
        if len(undirected_components(full, graph)) != 1:
            continue
        separators = [s for s in range(1, full) if minimal_global_separator(s, full, graph)]
        if not separators:
            continue
        minimum_size = min(bin(s).count("1") for s in separators)
        separators = [s for s in separators if bin(s).count("1") == minimum_size]
        td = cycle_rank(graph) + 1
        good = False
        bad_details = []
        for separator in separators:
            torso_tds = [cycle_rank(clique_separator_torso(graph, separator, component)) + 1
                         for component in undirected_components(full & ~separator, graph)]
            bad_details.append((separator, torso_tds))
            if max(torso_tds) <= td:
                good = True
                break
        if not good:
            return graph, td, minimum_size, bad_details
    return None


def random_no_good_minimum_separator(n: int, trials: int) -> object:
    full = (1 << n) - 1
    for _ in range(trials):
        graph = random_connected(n, random.random())
        separators = [s for s in range(1, full) if minimal_global_separator(s, full, graph)]
        if not separators:
            continue
        minimum_size = min(bin(s).count("1") for s in separators)
        separators = [s for s in separators if bin(s).count("1") == minimum_size]
        td = cycle_rank(graph) + 1
        details = []
        for separator in separators:
            torso_tds = [cycle_rank(clique_separator_torso(graph, separator, component)) + 1
                         for component in undirected_components(full & ~separator, graph)]
            details.append((separator, torso_tds))
            if max(torso_tds) <= td:
                break
        else:
            return graph, td, minimum_size, details
    return None


def gruber_binary_encoding(permutations: list[list[int]]) -> tuple[list[list[int | None]], int, int]:
    """Return the partial binary DFA transition table, start, and sole final state.

    States are the original states followed by all plus and all minus gadget states.
    """
    alphabet_size = len(permutations)
    original_size = len(permutations[0])
    next_state = original_size
    plus = [[0] * alphabet_size for _ in range(original_size)]
    minus = [[0] * alphabet_size for _ in range(original_size)]
    for q in range(original_size):
        for i in range(alphabet_size):
            plus[q][i] = next_state
            next_state += 1
        for i in range(alphabet_size):
            minus[q][i] = next_state
            next_state += 1
    transitions: list[list[int | None]] = [[None, None] for _ in range(next_state)]
    for q in range(original_size):
        transitions[q][0] = plus[q][0]
        for i in range(alphabet_size - 1):
            transitions[plus[q][i]][0] = plus[q][i + 1]
        for j in range(1, alphabet_size):
            transitions[minus[q][j]][1] = minus[q][j - 1]
        transitions[minus[q][0]][1] = q
    for symbol, permutation in enumerate(permutations):
        for p, q in enumerate(permutation):
            target = q if alphabet_size - symbol - 1 == 0 else minus[q][alphabet_size - symbol - 2]
            transitions[plus[p][symbol]][1] = target
    return transitions, 0, 0


def complete_with_reset(partial: list[list[int | None]], final: int) -> tuple[list[list[int]], int]:
    dead = len(partial)
    complete: list[list[int]] = []
    for row in partial:
        complete.append([dead if target is None else target for target in row] + [final])
    complete.append([dead, dead, final])
    return complete, dead


def trim_reachable_partial(partial: list[list[int | None]], start: int, final: int) -> tuple[list[list[int | None]], int, int]:
    reachable = {start}
    frontier = [start]
    while frontier:
        state = frontier.pop()
        for target in partial[state]:
            if target is not None and target not in reachable:
                reachable.add(target)
                frontier.append(target)
    vertices = sorted(reachable)
    remap = {old: new for new, old in enumerate(vertices)}
    trimmed = [[None if target is None else remap[target] for target in partial[old]] for old in vertices]
    return trimmed, remap[start], remap[final]


def transition_graph(table: list[list[int | None]]) -> tuple[int, ...]:
    out = []
    for row in table:
        mask = 0
        for target in row:
            if target is not None:
                mask |= 1 << target
        out.append(mask)
    return tuple(out)


def small_totalization_probe() -> object:
    # Two-state edge transposition plus identity; the looped graph has treedepth/rank 2.
    partial, start, final = gruber_binary_encoding([[1, 0], [0, 1]])
    partial, start, final = trim_reachable_partial(partial, start, final)
    complete, dead = complete_with_reset(partial, final)
    reachable = {start}
    frontier = [start]
    while frontier:
        state = frontier.pop()
        for target in complete[state]:
            if target not in reachable:
                reachable.add(target)
                frontier.append(target)
    distinguishable = {(p, q) for p in range(len(complete)) for q in range(p + 1, len(complete))
                       if (p == final) != (q == final)}
    changed = True
    while changed:
        changed = False
        for p in range(len(complete)):
            for q in range(p + 1, len(complete)):
                if (p, q) in distinguishable:
                    continue
                for symbol in range(3):
                    x, y = sorted((complete[p][symbol], complete[q][symbol]))
                    if x != y and (x, y) in distinguishable:
                        distinguishable.add((p, q))
                        changed = True
                        break
    minimal = len(distinguishable) == len(complete) * (len(complete) - 1) // 2
    indistinguishable = [(p, q) for p in range(len(complete)) for q in range(p + 1, len(complete))
                         if (p, q) not in distinguishable]
    return (len(partial), cycle_rank(transition_graph(partial)), len(complete), dead,
            cycle_rank(transition_graph(complete)), len(reachable), minimal, indistinguishable)


def main() -> None:
    for name, graph in [("path8", path(8)), ("star8", star(8))]:
        r = cycle_rank(graph)
        vals = []
        for rule in ("min_product", "min_degree", "max_degree"):
            order = choose_order(graph, rule)
            vals.append((rule, elimination_height(graph, order), order))
        print(name, "rank", r, vals)

    worst = {rule: (0.0, None) for rule in ("min_product", "min_degree", "max_degree")}
    for _ in range(1000):
        graph = random_connected(8, random.random())
        r = cycle_rank(graph)
        for rule in worst:
            order = choose_order(graph, rule)
            h = elimination_height(graph, order)
            ratio = h / max(r, 1)
            if ratio > worst[rule][0]:
                worst[rule] = (ratio, (graph, r, h, order))
    print("worst", worst)

    sep_worst = (0.0, None)
    for n in range(2, 10):
        for _ in range(300):
            graph = random_connected(n, random.random())
            graph = relabel(graph, random.sample(range(n), n))
            r = cycle_rank(graph)
            h, order = min_separable_height(graph)
            ratio = h / max(r, 1)
            if ratio > sep_worst[0]:
                sep_worst = (ratio, (n, graph, r, h, order))
        print("separable through", n, "worst", sep_worst)

    split_worst = (0.0, None)
    for n in range(2, 11):
        for _ in range(1000):
            graph = relabel(random_connected(n, random.random()), random.sample(range(n), n))
            r = cycle_rank(graph)
            sums = split_rank_sums(graph)
            ratio = min(sums) / max(r, 1)
            if ratio > split_worst[0]:
                split_worst = (ratio, (n, graph, r, sums))
        print("split through", n, "worst", split_worst)

    for p in (1, 2):
        for layers in (2, 3):
            graph, layer_sets, branches = layered_with_cycles(p, layers)
            print("layercycles", p, layers, len(graph), "rank", cycle_rank(graph), "fvs", feedback_vertex_number(graph))

    local_worst = (0.0, None)
    for n in range(4, 11):
        for _ in range(1000):
            graph = relabel(random_connected(n, random.random()), random.sample(range(n), n))
            initial = tuple(range(n))
            h, order = root_local_search(graph, initial)
            # Standard treedepth is loop-free symmetric cycle-rank + 1.
            td = cycle_rank(graph) + 1
            ratio = h / td
            if ratio > local_worst[0]:
                local_worst = (ratio, (n, graph, td, h, order))
        print("root-local through", n, "worst", local_worst)


if __name__ == "__main__":
    main()
