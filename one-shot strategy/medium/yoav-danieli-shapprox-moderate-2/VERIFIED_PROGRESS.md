# Verified progress on the logarithmic star-height conjecture

This note contains only statements checked during the proof search. It is not a
proof of the conjecture.

## 1. The precise problem

For a minimal bideterministic total DFA (A) with (n) states over a fixed
finite alphabet, McNaughton's theorem gives

\[
  h(L(A))=r(A),
\]

where (r(A)) is the cycle rank of its transition digraph. The requested
algorithm must output, in polynomial time, a polynomial-size regular-expression
circuit of height (O(r(A)\log n)).

## 2. Permutation and Eulerian structure

Let (d=|\Sigma|). Reverse determinism says that, for each letter (a), every
state has at most one incoming (a)-transition. Total forward determinism gives
exactly (n) outgoing (a)-transitions. Hence the map
(q\mapsto\delta(q,a)) is an injection of an (n)-element set into itself and
is therefore a permutation. Consequently the transition multigraph is
(d)-in/(d)-out regular and Eulerian. Trimness makes it strongly connected.

For an ordering of its vertices and a prefix (L), let (X^-) be the prefix
vertices receiving an arc from the suffix, and let (X) be the prefix boundary
in the underlying undirected graph. Eulerian cut balance gives

\[
 |A(L,V\setminus L)|=|A(V\setminus L,L)|\le d|X^-|.
\]

Every member of (X\setminus X^-) is the tail of an arc from (L) to its
suffix. Thus

\[
 |X|\le (d+1)|X^-|.
\]

Using the vertex-separation characterizations of pathwidth and directed
pathwidth, and (\operatorname{dpw}(D)\le r(D)+O(1)), this proves

\[
 \operatorname{tw}(\operatorname{und}D)
 \le \operatorname{pw}(\operatorname{und}D)
 \le (d+1)(r(D)+O(1)).
\]

Since the alphabet is fixed, the factor (d+1) is constant.

## 3. What a tree decomposition would give

Given a tree decomposition of the underlying graph of width (w), assign each
graph vertex to one bag containing it and choose a weighted centroid bag. Its
deletion leaves components of size at most half the current vertex set. Put the
at most (w+1) vertices of that bag in a chain and recurse in parallel on the
components. The resulting treedepth forest has height at most

\[
  (w+1)(\lceil\log_2 n\rceil+1).
\]

It is also a valid directed elimination hierarchy, because every directed edge
is an underlying undirected edge. Shared all-pairs state elimination along this
hierarchy gives a polynomial-size equivalent expression circuit with no greater
star height. Therefore a polynomial-time constant-factor treewidth
decomposition would prove the conjecture. It also proves the conjecture for
subclasses where such a decomposition is available or supplied.

Single-exponential fixed-parameter treewidth algorithms give the desired result
when the underlying treewidth is `O(log n)`. The height-`n` Kleene circuit gives
it when `r(A)=Omega(n/log n)`. The general intermediate regime remains.

Using the current optimum-sensitive treewidth approximation, one can compute a
decomposition of width `O(t sqrt(log(t+2)))`, where
`t=tw(und(D))`. Hence this route also proves the desired bound whenever
`r(A)=Omega(t sqrt(log(t+2)))`. Together with `t=O(r(A))`, this narrows its hard
structural regime to cases in which cycle rank and treewidth are within a
square-root logarithm, in particular recursively weighted cores with
`r=Theta(t)`.

## 4. Polynomial circuit size is not an existential obstruction

Suppose a directed elimination hierarchy of height (h) is supplied. For an
acyclic subgraph, compute all path languages by topological dynamic programming,
using no star. For several SCCs, combine their recursively computed all-pairs
circuits along the condensation DAG, again with only union and product. For a
strongly connected subgraph with chosen root (v), first compute path languages
whose internal vertices avoid (v), then use

\[
 R_{ij}\;\cup\;R_{iv}(R_{vv})^*R_{vj}.
\]

This adds one nested star. Memoizing all pairs at every recursive node gives a
coarse polynomial bound (O(n^4+|\Sigma|n^2)) on circuit size. Thus an optimal
height-(r(A)) hierarchy yields a polynomial-size circuit of height (r(A)).
For the bideterministic input this height is exactly (h(L(A))). Optimal-height
polynomial-size circuits therefore exist; finding an adequate hierarchy or
direct circuit in polynomial time is the unresolved part.

## 5. Approximation-preserving embedding of treedepth

Let (G) be a connected undirected graph of maximum degree (\Delta). Replace
every edge by its two directed orientations and put
(\Delta+1-\deg_G(v)) loops at every vertex (v). The resulting multigraph is
(d)-in/(d)-out regular for (d=\Delta+1), and every vertex has a loop.

Make a bipartite multigraph with a tail and head copy of each vertex and one
edge per directed arc. It is (d)-regular. Hall's theorem gives a perfect
matching; removing it preserves regularity, so repeated matching decomposes all
arcs into (d) perfect matchings. Label them by (d) letters. Each letter is a
permutation, hence this is a total bideterministic transition structure.

Choose any initial state and one final state (f). The graph is strongly
connected. For distinct states (p,q), choose a word (w) sending (p) to
(f). Since (w) acts bijectively, it does not send (q) to (f). All states
are therefore pairwise distinguishable, and the DFA is trim and minimal.

For every induced vertex set, SCCs are exactly the connected components of the
corresponding induced subgraph of (G), and every nonempty singleton is cyclic
because it has a loop. The cycle-rank recurrence is therefore exactly the
treedepth recurrence:

\[
 r(A_G)=\operatorname{td}(G).
\]

McNaughton's equality then gives

\[
 h(L(A_G))=\operatorname{td}(G).
\]

Thus the conjectured circuit algorithm would yield an (O(\log n)) value
approximation for treedepth, simply by reading the syntactic height of its
output. For subcubic (G), this reduction uses the fixed alphabet size four.

## 6. Exact remaining obstruction

The best verified general route computes balanced separators/pathwidth or
treewidth only with a nonconstant square-root-logarithmic loss. Chaining those
separators through (O(\log n)) size scales gives the published
(O((\log n)^{3/2})) factor. Removing that loss requires either:

1. a progress-sensitive separator hierarchy whose total maximum root-path cost
   is (O(r\log n)), despite approximate separators; or
2. a direct expression-circuit composition theorem that avoids the clique
   torso created on component boundaries.

There is a precise amortization refinement.  For a recursive component `H`,
write `r_H` for its rank, `m_H` for its order, and
`Phi(H)=r_H log m_H`.  If a balanced cut leaves a child `C` of order at most
`rho m_H`, for fixed `rho<1`, monotonicity gives

\[
 \Phi(H)-\Phi(C)\ge r_H\log(1/\rho).
\]

Hence every approximate separator whose size is `O(r_H)` telescopes safely to
`O(r log n)` along a branch.  If `s(H)` is the optimum balanced-separator size
and the available approximation factor is `alpha`, the only uncharged nodes
are therefore those with `alpha s(H)>Theta(r_H)`.  Since `s(H)<=r_H` and a
width-`t` decomposition has a balanced bag of size at most `t+1`, these are
exactly persistent high-separator/high-treewidth cores, up to the factor
`alpha`.  No verified theorem forces rank progress on such nodes.

One positive existential lemma supports the first route. A directed
vertex-separation layout of width at most `r+O(1)` yields, for any vertex weight,
a weak separator of size `r+O(1)` balancing that weight: cut just before the
cumulative weight crosses one half, include the crossing vertex, and include
all prefix vertices receiving an arc from the suffix. No residual SCC crosses
the cut. The union of the separators for two weights simultaneously balances
both at size `2r+O(1)`. What is not known is how to compute/round such
simultaneously progressive cuts without the nonconstant layout/separator loss,
and how to telescope that loss globally.

The worklog contains explicit counterexamples to the naive versions of both
possibilities. In particular, induced separator depth is not enough because a
residual component can complete its boundary to a clique, and minimum balanced
separators need not decrease treedepth locally.

### Representative falsified claims

- **Small rank does not imply a small feedback vertex set.** The two letters
  consisting of an `n`-cycle and the identity give a minimal permutation DFA of
  rank 2, while every state has a loop and every feedback vertex set has size
  `n`.
- **A minimum balanced separator need not lower depth.** On vertices `0,...,5`
  with edges `{01,02,05,12,13,14,23,24,34}`, treedepth is 4 and the unique
  size-one 3/4-balanced separator is `{0}`, but its residual `K_4` still has
  depth 4.
- **Random pivots fail inside the target class.** Symmetric looped full binary
  trees can be regularized into four permutation letters, have rank `h`, and
  give expected random-pivot height `Omega(2^h/h)`.
- **Component contraction overcounts interfaces.** Two `K_k` graphs joined by
  one bridge have treedepth at most `k+1`, while contracting them to two
  weight-`k` endpoints yields weighted depth `2k`.
- **One-vertex local scores fail.** The worklog gives explicit six- and
  seven-vertex graphs refuting largest-component profiles and maximum-degree
  selection even with optimal tie-breaking.

## 7. Primary references checked

- H. Gruber, *Digraph Complexity Measures and Applications in Formal Language
  Theory*, DMTCS 14(2), 2012, <https://doi.org/10.46298/dmtcs.583>.
- É. Bonnet, D. Neuen, and M. Sokołowski, *Treedepth Inapproximability and
  Exponential ETH Lower Bound*, IPEC 2025,
  <https://doi.org/10.4230/LIPIcs.IPEC.2025.17>.
- É. Bonnet, *Treewidth Inapproximability and Tight ETH Lower Bound*, JACM,
  2026, <https://doi.org/10.1145/3833387>.

## 8. Search outcome and route inventory

The search began at Unix time `1787928278`.  At Unix time `1787935502`, the
active-goal clock recorded `7207` seconds.  No complete proof survived the
separate adversarial audit, so no proof file was created.

The attempted routes, recorded chronologically and with explicit failures in
`WORKLOG.md`, comprise: treewidth/pathwidth conversion; balanced, weighted,
multiweight, spectral, min-cut, and expander separators; exact-small-parameter
and FPT/trivial win--wins; feedback vertex sets; block/core/dominator peeling;
random and deterministic pivot rules; DFS, spanning-tree, interval/chordal,
and torso decompositions; group actions and stabilizer chains; matrix-star and
fixed-point identities; all-pairs circuit composition; centered colorings and
random restrictions; global LP/metric rounding; lookahead, sampling, and
minor-obstruction schemes; and progress potentials based on treewidth,
well-linked terminals, or brambles.  Failed universal claims were retained
only when accompanied by a proof of failure or an explicit counterexample;
purely experimental observations are labeled as such.

The strongest next target is now precise.  Let `alpha` be the available
separator/layout approximation loss.  Low-separator recursive nodes with
`alpha s(H)=O(r(H))` already telescope.  One needs a polynomially constructible
hierarchy, or a persistent core invariant, proving that successive nodes with
`s(H)=Omega(r(H)/alpha)` make enough progress in rank or in a deletion-robust
core potential that their total maximum root-path charge is `O(r log n)`.
Neither ordinary well-linked terminal counts nor locally minimal bags have
this persistence property.  Establishing it, or a direct port-aware circuit
composition avoiding torso fill, is the most promising remaining route.
