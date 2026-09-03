# Search Report: Moderate IV

## Status

No complete proof of Conjecture 1 has been found. This report records only claims that survived the final audit; it is not a proof of the conjecture.

The active search ran from Unix time `1787935676` through `1787942877`, an elapsed interval of `7201` seconds. No candidate proof survived to the end of that interval.

## Target

For an `n`-state DFA `A`, compute in polynomial time an elimination strategy and an equivalent polynomial-size regular-expression circuit `C` such that

```text
h(C) = O(r(A) log n).
```

## Verified structural lemma

Let `H` be a cyclic strongly connected digraph on `m` vertices with cycle rank `rho`. There is a set `S` of at most `rho` vertices such that every SCC of `H-S` has at most `m/2` vertices. (Acyclic SCCs are base cases and need no separator.)

Proof. Take an optimal recursive elimination tree for `H`. At its root, inspect the SCCs after deleting the root. If none has more than `m/2` original vertices, stop. Otherwise there is a unique such SCC; follow its child and repeat, always measuring size against the original `m`. Put each traversed root in `S`. Every side SCC created along the path has size at most `m/2`. After at most `rho` cyclic roots, the residual subproblem is acyclic, hence all its SCCs are singletons. Deleting all of `S` from the original graph can only split the side SCCs and the final residual SCCs further. Thus every resulting SCC has size at most `m/2`. QED.

Consequently, a polynomial constant-factor approximation for Directed Balanced Separator would prove the target: recursively take such a separator, put its vertices in a chain above the recursive SCC strategies, and note that a root-to-leaf path crosses `O(log n)` recursion levels and pays `O(r(A))` vertices per level.

## Elimination strategy to circuit

An elimination strategy of cyclic height `H` yields a polynomial-size equivalent regular-expression circuit of star height at most `H`.

For a non-strong subproblem, recursively compute all-pairs path circuits inside its SCCs and combine them by star-free dynamic programming on the condensation DAG; an acyclic subproblem is the base instance of the same construction. For a strongly connected cyclic subproblem with chosen root `v`, recursively compute all-pairs path circuits inside the SCCs of `G-v`. Their condensation is acyclic, so it gives, without any new star, circuits for root-avoiding prefixes and suffixes and for the nonempty first-return excursions from `v` to `v`. Every path that visits `v` has the unique form “root-avoiding prefix, a sequence of first-return excursions, root-avoiding suffix.” Applying one Kleene star to the union of excursions therefore accounts for all repetitions through `v`. Thus exactly one new star level is added at each cyclic ancestor. Sharing the all-pairs subcircuits at every recursive node gives polynomial size; even a crude `O(n^4+n|Sigma|)` upper bound suffices.

## Strongest algorithmic partial results

The 2025 randomized approximation for Directed Balanced Separator returns `O(k sqrt(log(2+k)))` vertices whenever a constant-balanced separator of size `k` exists. Applying the structural lemma recursively, and stopping when a component has at most a dyadic guess `R` vertices, gives (with high probability)

```text
O(r(A) sqrt(log(2+r(A))) log(2n/r(A)) + r(A))
```

height. The run with `r(A) <= R < 2r(A)` has this guarantee, and the shallowest circuit among all dyadic runs can be selected syntactically.
The formula concerns `r(A)>=1`; the acyclic case `r(A)=0` is handled exactly by the star-free DAG construction.

The exact bicriteria separator routine runs in `2^{O(k)}(m+n)` time for fixed balance slack. Therefore, for every fixed constant `c`, under the promise `r(A) <= c log n`, trying every `k=1,...,ceil(c log n)` with enough repetitions yields the desired `O(r(A) log n)` strategy in randomized polynomial time with high probability; every returned separator is checked directly, and trivial elimination is a correctness-preserving fallback on the failure event. The middle regime remains uncovered.

At the opposite extreme, ordinary state elimination has height at most `n`, so it already meets the target whenever `r(A) >= n/log n`. Thus a particularly clear unresolved range is

```text
c log n < r(A) < n/log n.
```

## Fixed-alphabet total-DFA reduction from treedepth

The conjecture would imply a polynomial `O(log n)` value approximation for general undirected treedepth, even if the DFA alphabet is fixed to three letters.

Let `G` be a connected undirected graph. First form the total permutation DFA `P_G` with state set `V(G)`, one letter for every edge acting as that edge's transposition and fixing all other vertices, and an identity letter. Choose one state `q_0` as both initial and sole final state. Connectivity makes the generated action transitive, so the DFA is trim. If `p != q`, a permutation word sending `p` to `q_0` cannot also send `q` there, so it is minimal. It is bideterministic. Its transition graph is the symmetric graph `G` with a loop at every vertex, and hence

```text
r(P_G) = td(G) = h(L(P_G)).
```

Gruber's binary encoding replaces each alphabet letter `a_i` by `a^i b^(s+1-i)`. It produces a polynomial-size partial binary bideterministic automaton and preserves star height; take its trim part `B` (delete every state that is not both reachable and co-reachable). Trimming preserves the accepted language and bideterminism. Such a trim, one-final-state bideterministic automaton is minimal: a word taking one state to the final state can take no other state there, by reverse determinism. McNaughton's theorem therefore gives `r(B)=h(L(B))=td(G)`.

Make `B` total as follows. If it has a missing binary move, add a rejecting state `d`, send every missing `a`- or `b`-transition to `d`, and loop `d` on `a,b`. In every case, introduce a third letter `#` sending every state (including `d`, when present) to the sole final state `f`. Call the resulting ternary DFA `A_G`.

This DFA is trim. It is also minimal: distinct old states retain a distinguishing binary suffix, since an undefined partial run now ends at rejecting `d`; an old state is distinguished from `d` by a binary suffix taking it to `f`. Moreover,

```text
L(A_G) intersect {a,b}* = L(B).
```

Replacing `#` by the empty-language expression in any expression for `L(A_G)` computes this intersection without increasing star height. Hence `h(L(A_G)) >= h(L(B))`. On the other hand, the universal inequality `r(X) <= 1+r(X-v)` and deletion of `f` show

```text
r(A_G) <= 1 + r(A_G-f) <= 1 + max(r(B-f),1) <= r(B)+1,
```

where the harmless `1` term is omitted when no dead state is needed.

For completeness, the universal inequality follows SCC by SCC: a component not containing `v` is an induced subgraph of `X-v`, while in the component containing `v` one may choose `v` as the first elimination root, paying one plus the maximum rank left after its deletion.

Thus

```text
td(G) <= h(L(A_G)) <= r(A_G) <= td(G)+1.
```

The number of states of `A_G` is polynomial in `|V(G)|`, so its logarithm is `O(log |V(G)|)`. The conjectured circuit height, which is syntactically computable and is at least the language star height, would therefore be an `O(log |V(G)|)` estimate of `td(G)`.
For a disconnected input graph, apply this construction to each connected component and take the maximum returned estimate, since treedepth is the maximum over components. Thus the implication covers general undirected graphs.

## Exact obstruction

Known recursive balanced-separator methods lose `sqrt(log r)` in the size of every separator. A rank-`r` graph can retain rank `r` through `Theta(log n)` balanced recursive levels, so this factor cannot be charged to a decrease of rank. The directed layered family in the worklog realizes this plateau exactly. Conversely, processing an approximate separator in parallel or through a torso can retain its full excess: `K_{r,m}` with `m` on the order of `r sqrt(log r)` makes the wrong separator torso a clique of order `m`.

These plateau/torso families are counterexamples to black-box analyses claimed for all digraphs; they are not asserted to have bounded out-degree. The separate fixed-ternary reduction above is what shows that restricting the original DFA problem to a fixed alphabet still contains the unresolved general-treedepth consequence.

Therefore the exact missing step in the separator-hierarchy program developed here is either:

1. a constant-factor polynomial approximation for the relevant directed balanced separators; or
2. a genuinely global separator-hierarchy rounding theorem that pays approximation loss once across the hierarchy, rather than independently at every level.

This is an exact description of where the verified program stops, not a claim that every possible proof must use one of these two routes.

## Main falsified routes

- Uniform random elimination: a symmetric star has constant rank but expected linear nesting if its center is eliminated early.
- Local degree or one-vertex balance: constant-depth pendant-star and pendant-`K_{2,m}` families force linear height.
- Bottom-up maximum safe layers: the once-subdivided star has constant rank, but its unique maximum independent layer fills the remaining middle vertices into a clique.
- Fixed balanced block partitions: a crossed double-star of rank two makes both top-level block orientations create a linear clique.
- Rank-decrease amortization: the layered directed graph has exact rank `p` at every one of logarithmically many balanced prefix scales.
- Feedback-vertex-set fallback: attaching arbitrarily many private directed 2-cycles keeps cycle rank at most `p+1` while making every feedback vertex set arbitrarily large.
- Separator-torso preservation: a graph formed by joining a four-vertex star to `K_1 disjoint_union K_3` has treedepth six and a unique minimum separator, but its retained `K_3` torso is `K_7`.
- Ordinary decision-tree or submodular greedy analysis: connectivity partitions have deletion synergy; on a cycle the disconnected-pair objective is not submodular.
- Balanced matrix-star recursion: the two Schur-complement half-stars nest sequentially, and the crossed double-star defeats both block orientations.

### Explicit counterexamples used in the audit

1. **One-vertex balance.** Start with `K_{2,m}`, with sides `{a_1,a_2}` and `{b_1,...,b_m}`, and attach a private leaf `l_i` to `b_i`. Its treedepth is at most four: put `a_1,a_2` above the disjoint edges `b_i l_i`. Deleting `b_i` isolates `l_i` and leaves a main component smaller by two, while deleting an `a_j` or a leaf leaves a component smaller by only one. Hence the rule that minimizes the largest immediate residual component chooses every `b_i` on the same branch and has height at least `m`.

2. **Rank plateau under balanced recursion.** Let `L_0,...,L_t` each contain `p` vertices. Put every arc from `L_i` to `L_{i+1}`, and every arc from `L_i` to `L_0` for `i>=1`. The graph is strong. Deleting all of `L_0` leaves a DAG, so its rank is at most `p`. After fewer than `p` arbitrary deletions every layer is still nonempty and the graph is still strong, so the recursive definition forces rank at least `p`. Thus its rank is exactly `p`. Deleting a middle layer is a balanced size-`p` separator, yet the prefix containing `L_0` is a smaller graph of the same rank `p`; this can repeat for logarithmically many scales.

3. **Fixed block partitions.** Take adjacent centers `c_A,c_B`, each with `m` private leaves. This double-star has treedepth three (loop-free symmetric cycle rank two). Partition the vertices so block `A` contains `c_A` and all leaves of `c_B`, while block `B` contains `c_B` and all leaves of `c_A`. If `A` is eliminated first, eliminating `c_A` fills `c_B` and the `m` leaves adjacent to `c_A` (all lying in `B`) into a clique. The reverse block order is symmetric. Every order respecting that top partition therefore has linear height.

4. **Minimum-separator torso preservation.** Let `S={c,l_1,l_2,l_3}` induce a star centered at `c`; let the outside induce `K_1 disjoint_union K_3`; and join every vertex of `S` to every outside vertex. The unique minimum vertex separator is `S`. The graph has treedepth exactly six: an explicit upper decomposition puts `c`, then the `K_1` vertex, over a depth-four decomposition of `I_3 join K_3`; a `K_6` minor gives the matching lower bound. Clique-completing `S` in the torso containing the `K_3` produces `K_7`, raising treedepth to seven.

5. **Largest safe bottom layer.** In the once-subdivided star with arms `c-a_i-b_i`, the unique maximum independent set is `{c,b_1,...,b_m}`. The graph has treedepth three. Eliminating that independent set as the lowest color fills all `a_i` pairwise through `c`, leaving a clique of order `m`. Thus even an exact largest safe layer can destroy a constant-depth continuation.

## Most promising next route

The most promising route is a global relaxation for the entire elimination hierarchy, with rounding charged to root-to-leaf paths and with persistent/common separators paid only once. The layered plateau family should be a mandatory test case. A constant-factor directed balanced-separator algorithm would be a simpler sufficient breakthrough, but current primary literature gives only `O(sqrt(log(2+k)))` in polynomial time.

## Final audit conclusions

- The supplied target is explicitly labeled a conjecture, and no source checked states the requested `O(log n)` guarantee.
- Every construction called “verified” above has both an upper-bound certificate (an explicit forest/circuit construction) and its needed lower-bound or parameter comparison checked separately.
- Randomized separator theorems are not reported as deterministic or Las Vegas algorithms.
- All rank-zero, singleton-loop, fixed-alphabet, totality, trimness, and minimality base cases used in the reductions were checked explicitly.
- The fixed-ternary reduction shows that a proof would improve the currently stated treedepth approximation frontier; it does not prove that the conjecture is impossible.
- None of the attempted separator, local-greedy, algebraic, coloring, game, or parameter-regime combinations attains `O(r(A) log n)` for all `A`.

## Primary sources checked

- Yoav Danieli, *Polynomial-Time Approximation of the Star Height of a DFA* (the supplied PDF).
- Hermann Gruber, [*Digraph Complexity Measures and Applications in Formal Language Theory*](https://dmtcs.episciences.org/583/pdf), especially the cycle-rank approximation and binary bideterministic encoding.
- Anand, Lee, Li, and Saranurak, [*All-Subsets Important Separators with Applications to Sample Sets, Balanced Separators and Vertex Sparsifiers in Directed Graphs*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2025.12), Theorems 6 and 7.
- Bonnet, Neuen, and Sokołowski, [*Treedepth Inapproximability and Exponential ETH Lower Bound*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.IPEC.2025.17), for the current treedepth approximation status.
- Kim, Kwon, and Lee, [*An FPT algorithm for cycle rank on semi-complete digraphs*](https://arxiv.org/abs/2606.29336), which still treats FPT recognition for general digraphs as open.
