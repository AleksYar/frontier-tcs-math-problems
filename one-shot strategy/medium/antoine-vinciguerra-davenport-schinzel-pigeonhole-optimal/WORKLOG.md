# Proof Search Worklog

- **Start:** Unix `1787871803` = 2026-08-28 01:03:23 CEST.
- **Source inspection (Unix `1787871875`):** The PDF has one page. The problem asks for the smallest growth of `s=s(n)` such that
  `lambda_s(n) ~ binom(n,2) s`, and specifically whether this is possible for some `s=o(sqrt(n))`.
- **Definitions transcribed:** `DS(n,s)` consists of sequences over `[n]` with no equal adjacent terms and no two-symbol alternating subsequence of length `s+2`; `lambda_s(n)` is the maximum length. The stated universal bound is `lambda_s(n) <= binom(n,2)(s+1)`.
- **Known input stated in the PDF:** asymptotic equality holds when `s/sqrt(n) -> infinity`.

## Status

Source extraction and visual verification are complete.  A fully audited proof of the sufficient condition
`s >= C(log n)^3/(log log n)^2` and the necessary condition `s/log n -> infinity`
is in `PROOF.md`; the exact threshold inside this window remains unresolved.

## 2026-08-28 01:14 CEST (Unix `1787872487`)

### Source verification and known construction

- Rendered the only PDF page to PNG and visually checked the statement against the extracted text. There is no missing qualifier in the last section.
- Located the primary source behind Section 2: Jesse Geneson, *Asymptotic Tightness of the Pigeonhole Bound for Large-Order Davenport-Schinzel Sequences*, arXiv:2602.15375 (2026).
- Verified its mechanism. For `n=q^2`, concatenate `q^2` inner sequences on the `q`-element row supports of the affine-plane incidence matrix. Any two columns occur together in at most one support; each column occurs in `q` supports. The resulting order is at most `hat{s}+2q-2` and length is `q^2 lambda_hat{s}(q)-O(q^2)`. With the Roselle--Stanton bound this gives the stated asymptotic only when `s/q -> infinity`, i.e. `s/sqrt(n) -> infinity`.
- Inspected the primary Wellman--Pettie construction (arXiv:1610.09774), including its exact recurrence `s_t <= (t-1)s_{t-1}+2(q-t+1)`. For `t>2`, worst-case repeated co-occurrence multiplies the inner alternation budget by `(t-1)`; the published construction therefore loses a factorial in the leading constant and does not directly settle the requested equivalence.

### Verified exact identities

Let `c_ab` be the number of changes (equivalently: number of runs minus one) in the projection of `U` to `{a,b}`, and let `e_ab` be the number of indices `i` with `{u_i,u_{i+1}}={a,b}`. Then:

1. `c_ab <= s` for every pair in a DS sequence of order `s`.
2. `e_ab <= c_ab`.
3. `|U|-1 = sum_{a<b} e_ab`, hence the sharper pigeonhole bound is `|U| <= binom(n,2)s+1`.
4. Defining `D(U)=sum_{a<b}(c_ab-e_ab)`, one has the exact equation
   `|U|-1 = sum c_ab - D(U) <= binom(n,2)s-D(U)`.
5. Gap formula: fix `a`, and split `U` at successive occurrences of `a`. If an internal `a`-gap contains `d` distinct other symbols, it contributes exactly `2(d-1)` to `sum_b(c_ab-e_ab)`; a nonempty prefix/suffix gap containing `d` distinct symbols contributes `d-1`. Summing over `a` counts each pair defect twice.
6. Reuse-distance formula: process occurrences left to right. An occurrence of `x` contributes to `sum c_ab` the number of distinct symbols seen since the preceding `x` (or in the whole earlier prefix if it is the first `x`). This is because precisely those pairwise projections change at this occurrence.

All six statements were checked on hand examples and by small exhaustive scripts.

### Routes attempted and current disposition

- **Universal lower bound `D=Omega(n^(5/2))`: not established and likely too crude.** The gap formula alone only gives `Omega(n^2)` for an edge-covering skeleton; its convex constraints allow one very large gap per symbol. A simultaneous obstruction would be needed.
- **Naive pair-block construction:** concatenate long alternating blocks for the `binom(n,2)` pairs. Its overhead is governed by an ordering of the edges of `K_n`; exhaustive search for `n=3,4,5` showed minimum worst pair-switch counts `1,2,3` in the unconstrained edge-order model, so this direct ordering does not yield sublinear overhead by itself.
- **Inflated Euler-tour skeleton:** contract every maximal backtracking run of a word. Inflating a skeleton edge-run increases `c_ab` and `e_ab` equally, so the defect `D` is invariant. Thus a skeleton covering pairs can be inflated to use the remaining pair budgets, and the length deficit is exactly skeleton defect plus unused capacities. Exhaustive Euler-tour checks gave minimum total defects `2` for `K_3`, `16` for `K_5`, and a found value `47` (not certified optimal) for `K_7`; the corresponding maximum projection changes were `2,4,5`. This suggests total defect might be near quadratic even though the maximum pair order grows, but no general construction or bound is yet proved.
- **Recursive/tensor application of the affine-plane construction:** applying the `S_2` operator to an already improved inner sequence does not reduce the outer additive cost `2sqrt(n)`; straightforward recursion therefore does not beat the exponent `1/2`.
- **Larger incidence blocks:** a linear pair-covering design with block size `k>sqrt(n)` cannot cover every pair, by Fisher's inequality (`b>=n` together with `b~n^2/k^2`). Allowing pair multiplicity in the polynomial construction creates a matching multiplicative loss in the order. This discards the simplest proposed `n^(1/3)` optimization.
- **Random thinning of a high-order optimal sequence:** independently sampling positions does not scale two-letter alternations, because a long monochromatic run in a two-letter projection survives with probability close to one, not the sampling probability. This route in its naive form is false.
- **Random alphabet restriction (verified monotonicity lemma):** for `2<=k<=n`, restricting a sequence to a uniformly random `k`-symbol subset retains every original adjacent transition whose endpoints are chosen. Hence
  `(lambda_s(n)-1)/binom(n,2) <= (lambda_s(k)-1)/binom(k,2)`.
  The normalized maximum transition density is nonincreasing in alphabet size. This is rigorous but needs a quantitative finite-`s` bound at a smaller alphabet to obstruct or construct the desired regime.
- **Low-alternation ordering of affine-plane rows:** reordering the `q^2` rows could only improve the additive `2q` term if every pair of `q`-point line supports had a low-alternation merge. No such ordering is known; grouping by vertical fibers still forces at least one internal change per fiber for each pair and does not improve the crude scale.

### Explicitly discarded claims / counterexamples

- Claim “sampling positions with probability `p` reduces every pair's order by about `p`” is false: if a projection has two very long constant runs `a...a b...b`, both runs survive with probability tending to one, so its one change does not scale by `p`.
- Claim “the gap formula alone forces average gap diversity `Omega(sqrt(n))` in an Euler tour” is false as a local optimization statement: for a fixed symbol, all edges among the other `n-1` vertices may be placed in one gap of diversity `n-1`, while the remaining gaps have diversity two; the resulting sum is only linear. Whether all symbols can realize this simultaneously remains a global question.
- The PDF's displayed upper bound is not the sharp transition count: the exact elementary bound is `binom(n,2)s+1`. This difference is asymptotically irrelevant when `s->infinity` but must be tracked in finite identities.

## 2026-08-28 01:19 CEST (Unix `1787872767`): amplification breakthrough

### Inflation lemma (verified)

- If a word `V` has pairwise projection-change counts `c_ab(V)<=H` and contains an adjacent occurrence of a pair `{a,b}`, replace one such transition by a longer alternating walk on `a,b` with the same endpoints (hence an odd number of transitions). This adds an even number of transitions to both `c_ab` and `e_ab` and adds **zero** projection changes for every pair involving a third symbol: after deleting the other endpoint, the inserted occurrences are merely repetitions of the endpoint already present at that location.
- Consequently, for every supported adjacent pair one may add at least `s-H-1` symbols while keeping every pairwise change count at most `s` (choose the largest allowable even increment). If the adjacent support has `(1-o(1))binom(n,2)` pairs and `H=o(s)`, this produces length `(1-o(1))binom(n,2)s`.

### Random-relabeling support amplifier (verified probabilistic argument)

- Let `W` be a DS word of order `h` on `N` symbols whose adjacent support has density at least a constant `alpha>0` among all unordered symbol pairs.
- Concatenate `r` independently uniformly relabeled copies. A fixed pair is absent from the union of the supports with probability at most `(1-alpha)^r`; hence there is a deterministic choice of relabelings leaving at most that fraction of pairs uncovered (expectation argument).
- The concatenation has pair order at most `H=r(h+1)-1` (sum the within-copy changes and at most one new change per copy boundary). Taking `r->infinity` but `rh=o(s)` gives support density `1-o(1)` and `H=o(s)`.
- Deleting equal symbols at copy boundaries can destroy at most two supported transition types per boundary, so if `r=o(N^2)` this does not affect support density. Alternatively, boundary-compatible relabelings can avoid the issue.

### Dense base at cube scale

- Take `n=q^3` and the Wellman--Pettie polynomial-incidence sequence `S_3(hat{s},q)` with `hat{s}=2q`.
- Exact alternation recurrence: `a_1=2q+1`, `a_2<=a_1+2(q-1)=4q-1`, `a_3<=2a_2+2(q-2)=10q-6`. Thus it is a DS word of order at most `10q-7`.
- Roselle--Stanton gives base length at least `binom(q,2)q+q=(q^3-q^2)/2+q`. Two incidence lifts multiply length by `q^2` each, apart from `O(q^4)` boundary deletions. Hence `|S_3| >= (1/2-o(1))q^7`.
- Every adjacent pair occurs at most `10q-7` times, so its adjacent support has size at least `(|S_3|-1)/(10q-7) >= (1/20-o(1))q^6`, a fixed positive fraction of the `~q^6/2` pairs.
- Apply the support amplifier with, for example,
  `r=min(floor(sqrt(s/q)), floor(log n))`. If `s/q->infinity`, then `r->infinity`, `rq=o(s)`, and `r=o(n^2)`. Inflation yields
  `lambda_s(q^3) >= (1-o(1))binom(q^3,2)s`.
- For arbitrary `n`, choose the largest prime `q<=n^(1/3)`. The prime number theorem gives `q^3=n(1-o(1))`; monotonicity in alphabet size transfers the lower bound. Therefore the pigeonhole asymptotic holds whenever `s/n^(1/3)->infinity`.
- This already answers the PDF's highlighted question affirmatively, e.g. `s=n^(2/5)`.

### Higher-degree extension under development

- For each fixed `t>=2`, `S_t(2q,q)` has alphabet `q^t`, length `Theta_t(q^(2t+1))`, and order `O_t(q)` (more explicitly at most `7q(t-1)!`). Thus its adjacent support has a positive density `alpha_t>0`. The same amplifier proves asymptotic equality whenever `s/n^(1/t)->infinity`.
- Allowing `t` to grow requires tracking `alpha_t`; the crude uniform support lower bound is `alpha_t=Omega(1/(t-1)!)`, so the deterministic amplifier needs `s >> q((t-1)!)^2`. Optimizing this gives a concrete subpolynomial sufficient scale near `exp((2+o(1))sqrt(log n log log n))`. A sharper randomized order audit may reduce one factorial, but this is not yet accepted.

## 2026-08-28 01:35 CEST (Unix `1787873708`): polylogarithmic construction

The previous fixed-degree argument admits a substantially stronger randomized recursion. The following route has survived the first internal derivation and is now the main candidate.

### Recursive binary incidence word

- Let the level-`d` alphabet be `F_2^d`, interpreted as coefficient vectors of polynomials of degree `<d` evaluated at `x in F_2`.
- There are four evaluation rows `(x,v)`. Every symbol belongs to exactly two row supports; every support has `2^(d-1)` symbols.
- Define `W_1=12121` (order 4, length 5). For `d>=2`, concatenate four independent copies of `W_(d-1)`, one on each row support, using an independent uniform bijection between the canonical level-`d-1` alphabet and that support. Delete at most three immediate repetitions at copy boundaries.
- The length recurrence is deterministic: `L_d>=4L_(d-1)-3`, hence `L_d>=4^d+1`. This is not itself the final lower bound; it guarantees many available transitions/support edges.

### Exact pair branching law

- For a uniformly random distinct pair in `F_2^d`, its difference is uniform on `F_2^d\{0}`. The pair co-occurs in one child block for each zero among the two evaluations of the difference at `0,1`.
- Put `A=2^(d-2)`. The number `X_d in {0,1,2}` of children has
  `P(X_d=2)=(A-1)/(4A-1)`, `P(X_d=1)=2A/(4A-1)`, `P(X_d=0)=A/(4A-1)`.
- For every `z>=1`,
  `E[z^X_d] <= ((1+z)/2)^2`;
  after clearing denominators the difference is proportional to `1+2z-3z^2<=0`. Thus the entire pair recursion tree is dominated in exponential moments by a critical binary Galton--Watson tree with offspring `Bin(2,1/2)`.
- The mean is `mu_d=1-1/(2^d-1)`. Therefore the expected population at the base level is the product of `mu_d` for `d=2,...,t`, bounded below by an absolute positive constant. The second moment grows at most linearly in `t`, so Paley--Zygmund gives base-level survival probability at least `beta/t` for an absolute `beta>0`.
- Survival implies that the original pair occurs adjacently in a base copy of `12121`.

### Alternation and exponential moment

- For a pair at a recursion node, if it has `r` common child blocks, it has `2-r` singleton blocks for each endpoint. Hence the number of runs in its projection is at most the sum of the child run counts plus `2(2-r)<=4`.
- If `T` is the total number of nodes in its recursion tree, the pair's alternating-subsequence length is at most `5T` (base contribution at most 5 and at most 4 at every internal node).
- For a depth-`t` critical binary Galton--Watson total progeny `T`, with `theta=1/(100t^2)`, the recursion
  `F_d=e^theta((1+F_(d-1))/2)^2`, `F_0=e^theta`,
  and the induction `F_d-1 <= (d+1)/(2t^2)` give `E exp(T/(100t^2))<=1+1/t`. Consequently
  `E exp(A/(500t^2))<=1+1/t` for a random pair's alternating length `A` in `W_t`.

### Simultaneous coverage/order and target theorem

- For arbitrary `n`, put `t=ceil(log_2 n)` and `N=2^t<2n`. In each of `r` independent copies, construct an independent random `W_t`, choose a uniform injection of `[n]` into its alphabet, restrict to those `n` symbols, and relabel back. Restriction cannot increase alternations and preserves every supported adjacent pair whose endpoints are retained.
- For every fixed pair of `[n]`, the copies are independent, its image is a uniform distinct pair, and therefore:
  - its probability of not being supported in any copy is at most `(1-beta/t)^r`;
  - the exponential moment of the sum of its within-copy alternating lengths is at most `(1+1/t)^r` at parameter `1/(500t^2)`.
- Set `R=s/t^3` and, under the target assumption `R->infinity`, choose
  `g=min(sqrt(R), sqrt(n)/t)` and `r=ceil(tg)`. Then `g->infinity` and `r<=sqrt(n)+1`.
- Expected uncovered fraction is at most `exp(-beta g+o(1))`; Markov makes it `o(1)` with probability tending to one.
- Chernoff plus a union bound over fewer than `n^2` pairs shows, with probability tending to one, that every pair has baseline change count
  `H=O(t^3+t^2g+r)`.
  Indeed the exponent is `-H/(500t^2)+r/t`, and taking the constant in the `t^3` term larger than `1000 log 2` beats the `n^2<=4^t` union factor.
- The choice of `g` gives `H/s->0`. Boundary-repeat deletions destroy at most `2r=o(n^2)` support types. Thus some deterministic concatenation has order `H=o(s)` and adjacent support `(1-o(1))binom(n,2)`.
- Applying the verified inflation lemma yields
  `lambda_s(n)>=(1-o(1))binom(n,2)s`.
- Together with the elementary upper bound, the candidate theorem is:

  **If `s/(log n)^3 -> infinity`, then `lambda_s(n) ~ binom(n,2)s`.**

This proves the highlighted `o(sqrt(n))` question affirmatively by a very wide margin. The exact necessity/minimal threshold has not yet been derived; current work is auditing the theorem and looking for either a matching obstruction or a further pruning improvement.

## 2026-08-28 01:43 CEST (Unix `1787874215`): first adversarial audit

- Wrote the complete polylogarithmic sufficient-condition proof to `PROOF.md`, explicitly separating it from the still-unproved exact threshold.
- Re-read the proof end to end and checked every random variable is sampled in the required distribution after restriction to arbitrary `n`:
  a uniform injection sends a fixed pair to a uniform distinct pair of `F_2^t`; fresh independent row bijections make child pairs uniform and independent across recursion branches; fresh copies make the concatenated pair variables independent.
- Verified by direct enumeration for dimensions `2,...,10` that the child-count formula is correct. (The dimension-2 `X=2` count is zero, as the displayed formula says.)
- Verified numerically for depths up to 1000 that the claimed Galton--Watson MGF recurrence is far below the bound `1+1/t`; the analytic induction has slack.
- Generated random recursive words for dimensions `2,...,8`. Observed lengths, support densities, and maximum pair changes agreed with the predicted qualitative behavior (support density decreasing roughly as `1/t`, maximum changes well below the conservative `O(t^3)` bound).
- Ran 1000 randomized simultaneous-inflation tests for each alphabet size `3,...,7`; in every test, the change in each pair count was exactly the allocated even increment for that pair and zero for all other pairs.
- Strengthened a boundary claim: suppressing `...a x x b...` to `...a x b...` preserves **both** distinct adjacent types `{a,x}` and `{x,b}`. Thus copy-boundary cleanup loses no support types at all.
- Rechecked arbitrary-`n` restriction: an original adjacent supported transition with both endpoints retained remains a transition after restriction and run suppression; a two-letter projection is unchanged before run suppression and can only lose changes afterward.
- Rechecked simultaneous-event argument: the uncovered fraction is `o(1)` with high probability by Markov; the maximum-order event is high probability by Chernoff plus the `n^2<=4^t` union bound; no independence between these two aggregate events is assumed.

### Audit outcome

No unsupported inference or counterexample was found in the theorem
`s/(log n)^3 -> infinity => lambda_s(n) ~ binom(n,2)s`.

This audit is not yet the final separate audit required for early termination, because the first clause of the original problem (an exact smallest scale) remains unresolved.

## 2026-08-28 01:45 CEST (Unix `1787874333`): removed the unnecessary omega factor

- Found that the first finish of the polylog proof subtracted the **maximum** baseline pair count from every supported pair. Pair-specific inflation instead adds at least `s-c_ab-1` for pair `{a,b}`, so the total loss is governed by `sum c_ab`, not `N max c_ab`.
- Fixed the number of independent recursive copies at `r=ceil(t^(3/2))`, where `t=ceil(log_2 n)`.
- Coverage still tends to one because a pair is supported per copy with probability `Omega(1/t)`, giving failure `exp(-Omega(sqrt(t)))`.
- The MGF union bound gives `max c_ab <= C_0 t^3` simultaneously for all pairs.
- On the other hand `E A_t<=5t` (expected total progeny is at most `t`), so the expected average concatenated pair count is `O(rt)=O(t^(5/2))`. Markov gives a simultaneous deterministic outcome with average at most `t^(11/4)=o(t^3)`.
- Hence for every `s>=C_0 t^3`, the scaffold itself is order at most `s`, while total pair-specific inflation loss is `o(Ns)`. The proved condition strengthens to

  **There is an absolute `C` such that `s>=C(log n)^3` implies `lambda_s(n)~binom(n,2)s`.**

- Updated `PROOF.md`, including a pair-specific statement of the inflation lemma.

## 2026-08-28 01:49 CEST (Unix `1787874554`): subcritical thinning refinement

- Tested a substantially different parameter regime: independently retain each recursive row block with probability `p=1-epsilon`. The common-block pair tree is then exponentially dominated by a Galton--Watson process with offspring `Bin(2,p/2)` and mean `p<1`.
- Proved the two required quantitative facts:
  1. base survival (hence pair support) has probability `Omega(epsilon p^t)`;
  2. total progeny has MGF `E exp(c epsilon^2 T)<=1+C epsilon` and mean `O(1/epsilon)`.
- Chose, with `t=ceil(log_2 n)` and `ell=log t`,
  `epsilon=(ell-log ell)/t`, so `p^t~ell/t`.
  Then one-copy support probability is `Omega(ell^2/t^2)`.
- With `G=log ell` and `r=Theta(G t^2/ell^2)` independent thinned copies:
  - uncovered fraction is `exp(-Omega(G))=o(1)`;
  - the all-pairs Chernoff/union threshold is `O(t^3/ell^2)`;
  - the average pair count is `O(G t^3/ell^3)=o(t^3/ell^2)`.
- Pair-specific inflation therefore proves the stronger sufficient condition

  **`s >= C (log n)^3/(log log n)^2`.**

- Added this as a separate Section 6 in `PROOF.md`, leaving the independently audited unthinned `C(log n)^3` argument intact as a fallback.
- Adversarial correction during formalization: an initially written second-moment recurrence used a variance term `p^2 E Z_j`; the safe bound is `4 E Z_j`. Iterating the corrected recurrence still gives `E Z^2=O(p^t/epsilon)`, so the survival estimate is unchanged. The proof file contains the corrected inequality.
- Made the subcritical MGF invariant explicit: with `theta=epsilon^2/100`, the interval `0<=F_j-1<=2epsilon` is invariant. This removes a previously heuristic constant-choice sentence.

## 2026-08-28 01:54 CEST (Unix `1787874845`): lower-bound routes and construction limit

### Reference-gap/local-Ramsey route

- For a reference symbol `x`, every other symbol `y` occurs in only `O(s)` distinct `x`-gaps, since each occupied gap costs changes in the `{x,y}` projection.
- Choosing one `x`-gap for every supported edge among the other symbols gives a locally `O(s)`-colored complete graph: at every vertex, only `O(s)` gap-colors occur.
- Verified a simple local-Ramsey lemma. Greedily choosing a vertex and its largest color-neighborhood for `m~log_k n` steps (where `k` is the local color bound), then pigeonholing the colors seen by the final vertex, yields a monochromatic clique of size `Omega(log n/(k log k))`.
- Such a clique lies in one `x`-gap, so the argument can be iterated inside nested gaps. However the reference symbols then occur in a nested pattern
  `x_0 x_1 ... x_d ... x_1 x_0`, not an alternating pattern. Order-2 tree-traversal DS sequences show that arbitrarily deep nesting is compatible with tiny order. Thus this route does not produce a threshold lower bound and is discarded unless supplemented by a non-nesting invariant.

### Optimizing uniform thinning

- For retention mean `p=1-epsilon`, the scheme has:
  - one-copy support probability about `epsilon exp(-epsilon t)`;
  - MGF scale `epsilon^2`;
  - expected within-copy pair count `Theta(1/epsilon)`.
- Covering almost all pairs and keeping the average baseline loss negligible impose `exp(epsilon t)=o(t)` (up to slowly growing coverage factors), while the all-pairs union threshold is `Theta(t/epsilon^2)`.
- The largest admissible `epsilon` is therefore `(1-o(1))log(t)/t`, yielding `Theta(t^3/log^2 t)`. Stronger uniform thinning makes the number/average cost of copies too large. This verifies that the current scheme naturally stops at `(log n)^3/(log log n)^2`; it is not a universal necessity proof.

### Necessary condition currently verified

- Any exact threshold must diverge: if `s` is bounded along a subsequence, classical fixed-order DS bounds give `lambda_s(n)=n^(1+o(1))=o(n^2s)`. No quantitatively stronger universal obstruction has yet survived audit.

## 2026-08-28 01:56 CEST (Unix `1787875009`): small dense-support search

- Reformulated the base problem as finding a word of minimum pair order whose **adjacent support graph is complete**. Appending a symbol is a move-to-front operation on the recency permutation; it increments `c_xy` for precisely the symbols preceding `x` in that permutation. This gives an exact finite-state search.
- Exhaustive memoized search certified the minimum complete-support orders:
  - `n=3`: order 2, witness `0 1 2 0`;
  - `n=4`: order 3, witness `0 1 2 0 3 1 2 3`;
  - `n=5`: order 3, witness `0 1 2 0 3 4 0 4 1 3 2 4`.
- Search certified no order-2 witness for `n=4,5,6`; the order-3 search for `n=6` was interrupted after state growth became excessive and is not a result.
- The `n=4` witness is closely related to the first row/column recursion of Wellman--Pettie. At higher levels that recursion has length only `Theta(n log n)`, hence cannot support all `Theta(n^2)` pairs. Small cases therefore do not extend directly to a logarithmic-order construction.

## 2026-08-28 01:58 CEST (Unix `1787875105`): exact skeleton characterization

- Proved a converse to the inflation method. Given a near-optimal order-`s` word, let
  `D=sum_(a<b)(c_ab-e_ab)`, where `e_ab` counts actual adjacent transitions. Near equality forces `D=o(Ns)` and leaves only `o(N)` unsupported pairs.
- Partition the transition path into maximal runs with one unordered edge label. Every boundary is a factor `a b c` with `a!=c`, hence produces a distinct non-adjacent `{a,c}` projection change counted by `D`. Therefore the number of edge-runs is at most `D+1`.
- Contract each run to the shortest alternating path with the same endpoints (one transition for different endpoints, two for equal endpoints). This preserves every supported edge, uses at most two transitions per run, and preserves `D`: it reduces `c_ab` and `e_ab` equally for the run pair and deletes only repetitions in projections involving a third symbol.
- The contracted scaffold `V` therefore has
  `sum c_ab(V)<=3D+2=o(Ns)`, maximum pair count at most `s`, and support density `1-o(1)`.
- Conversely, pair-specific inflation turns any scaffold with support density `1-o(1)`, maximum pair count at most `s`, and average pair count `o(s)` into a near-optimal order-`s` word.
- Thus the original threshold is exactly equivalent to the minimum maximum pair count of an almost-complete-support scaffold subject to negligible average pair count. Added this Skeleton Lemma to `PROOF.md`.
- Immediate elementary necessity: such a scaffold has average pair count at least `1-o(1)`, so `o(s)` forces `s->infinity`. This replaces reliance on fixed-order DS asymptotics for the only currently proved universal obstruction.

## 2026-08-28 02:00 CEST (Unix `1787875206`): supercritical and low-variance variants

- Tested a slightly supercritical common-block recursion (duplicate a common child with small probability so mean offspring is `1+epsilon`). Although base survival rises to `Theta(epsilon)`, a surviving near-critical tree has total progeny scale `exp(epsilon t)/epsilon^2` (one `1/epsilon` factor for its final population conditioned on survival and another from summing the last `1/epsilon` generations). After enough copies for coverage and an all-pairs tail bound, this does not improve the subcritical scale. Discarded.
- Investigated whether a low-variance, mean-one incidence design could replace the Poisson-like common-block law. For a regular incidence matrix with `b=q^2` blocks, column weight `q`, and centered column vectors, the centered inner product of two columns is `d_ab-1`, where `d_ab` is their codegree. The Welch/rank bound in dimension `b-1` gives average `(d_ab-1)^2=Omega(1)` whenever the number of symbols is much larger than `b`. Thus constant offspring variance is unavoidable in this natural regular-incidence framework. This explains why merely changing the polynomial code is unlikely to remove the critical `t^2` progeny-tail scale, though it is not a universal lower bound for arbitrary words.

## 2026-08-28 02:03 CEST (Unix `1787875433`): universal working-set lower bound

- Identified `sum c_ab` exactly with total move-to-front reuse rank. When an occurrence of `x` has recency rank `r`, exactly the `r` more-recent distinct symbols cause a projection change with `x`.
- For cache size `k`, let `M_k` count accesses of rank at least `k`. Cheap accesses only permute the top-`k` symbol set. Every expensive access swaps in at most one symbol and creates at most `k-1` new co-resident pair possibilities. Including initial cache filling, a word with `P` supported adjacent pair types satisfies
  `P <= k^2+(k+1)M_k`.
- If `P=(1-o(1))binom(n,2)`, then for every dyadic `k<=n/4`, `M_k=Omega(n^2/k)`.
- The dyadic identity `r >= (1/2) sum_(2^j<=r)2^j` yields
  `sum c_ab=sum r_i >= Omega(n^2)` at each of `Theta(log n)` scales, hence
  `sum c_ab=Omega(n^2 log n)`.
- Combined with the skeleton lemma's average `o(s)`, this proves the universal necessary condition

  **`s/log n -> infinity`.**

- Added the Working-Set Lemma and this necessary condition to `PROOF.md`.
- The exact remaining gap is now quantitative and explicit:
  necessary `s=omega(log n)` versus sufficient `s>=C(log n)^3/(log log n)^2`.

## 2026-08-28 02:08 CEST (Unix `1787875682`): stationary move-to-front attempt

- Considered a stationary recency-chain scaffold. Start from a uniform permutation and choose rank `r>=1` with telescoping probability `1/(r(r+1))` (put the remaining tail mass at rank `n-1`), then move that symbol to the front.
- Verified exact marginals:
  - uniform permutations are stationary;
  - every transition edge is marginally uniform among the `binom(n,2)` pairs;
  - a fixed pair flips at rate `H_(n-1)/binom(n,2)`, so total average pair count over `Theta(binomial(n,2)g)` steps is `Theta(g log n)`, matching the Working-Set lower scale.
- Simulations for `n=30,...,1000` falsified the naive independent-hit heuristic. After `binom(n,2)` steps only about `0.15--0.24` of edge types were covered, despite one expected hit per edge; hits cluster strongly. Worst pair flip counts were also much larger than the mean (e.g. about 244 versus mean 22 for `n=1000`, three units of normalized runtime).
- Periodic independent recency resets or flatter rank distributions trade clustering against a much larger expected reuse rank. No rigorous hitting-time/concentration bound was obtained that improves the recursive theorem.
- Status: potentially promising for closing the gap if its clusters can be controlled or decorrelated, but entirely unproved and excluded from `PROOF.md`.

## 2026-08-28 02:20 CEST (Unix `1787876456`): balanced prefix rotations and edge-order scaffolds

### Removing rank-one rotations

- Modified the stationary prefix-rotation chain to forbid selecting the current front: in zero-based rank notation, set
  `P(R>=j)=2/(j+1)` for `j>=1`.  Thus `q_1=1/3`, `q_j=2/((j+1)(j+2))` in the interior, and the final rank receives the remaining tail mass.  It still has uniform stationary distribution, a uniform marginal transition edge, and expected reuse rank `Theta(log n)`, while eliminating immediate repeated requests to the front.
- Simulations up to `n=2000` showed better edge coverage but did **not** justify independent coupon-collector behavior.  In `N=binom(n,2)` steps, coverage decreased slowly from about `0.35` at `n=50` to `0.23` at `n=2000`; after `10N` steps it was about `0.95--0.99` over the tested range.
- Inspected the worst-pair event histories.  The obstruction is not just immediate toggling.  Once two labels are pulled toward the front, they can remain in the shallow ranks for a long excursion and flip dozens of times.  Across depths `j`, the residence time is of order `j` and the flip hazard is of order `1/j^2`, producing a harmonic number of flips in one excursion.  Empirical worst counts after `N` steps were consistent with a possible `Theta(log^2 n)` rather than a proved `Theta(log n)` maximum.  No concentration lemma strong enough for the all-pairs maximum was obtained.

### Ordering all edge blocks

- Considered the explicit complete-support word obtained by sorting the unordered edges `(a,b)` by their interleaved binary (Morton) key and concatenating their endpoint blocks.  Exact computation for powers of two showed
  `average c_ab=Theta(log n)` but `max c_ab=2n+O(1)`.
- Determined the heavy-tail mechanism: pairs whose binary labels first differ near the least significant bit have `c_ab=Theta(n)`, and more generally the pair-count distribution has an approximate `P(c_ab>=x)=Theta(1/x)` tail.  Thus the construction attains the Working-Set lower bound in total but fails badly in maximum norm.
- Randomly assigning edges among `r` independently relabeled Morton orders and concatenating the thinned orders was tested.  With `r=log_2 n`, the observed average grew like `Theta(log^2 n)` and finite-size maxima improved, but asymptotically a close pair in some coordinate still contributes `Omega(n/r)`.  Taking `r` large enough to cap this creates `Omega(r)` projection changes at concatenation boundaries.  Hence this smoothing idea does not give a polylogarithmic worst-case proof.
- A recursive four-quadrant Gray ordering of the bipartite edge grid was also tested.  It again had average `Theta(log n)` and maximum `Theta(n)` (for `n=128`, average about `14.4`, maximum `130`).  This confirms that the heavy maximum is structural for these simple space-filling traversals, not an artifact of the particular Morton key.

## 2026-08-28 02:30 CEST (Unix `1787877053`): boundary support, ruler schedules, and linear recursion maps

### Boundary transitions in the recursive construction

- The proof only certifies support when a pair's common-block tree survives to a base `12121` word.  I tested whether the many transitions at concatenation boundaries give a substantially larger support probability.
- Fresh random recursive words on `n=2^d`, `d=3,...,11`, had one-copy support densities decreasing from about `0.65` to `0.259`.  The data are closer to `Theta(d^(-1/2))` than the certified `Omega(1/d)`, so boundary support is real.  However it does not improve the maximum-pair exponential-moment scale, which is the term responsible for the final `d^3/(log d)^2` threshold.  The **expected** thinned word-length scale is only `n^2p^d`, so even perfectly dispersed boundary transitions could improve the support estimate by at most the factor `1/epsilon`; in the parameter optimization this changes only the leading constant in `epsilon*d`, not the asymptotic power.

### Binary ruler rank schedule

- Replaced the random prefix ranks by the deterministic multiscale schedule with prefix length `2^v_2(t)`.  It has the desired harmonic aggregate rank cost.
- This route fails decisively: its permutation orbit supports only about `2/n` of all pair types, even after many periods.  For example the stabilized coverage fractions for `n=32,64,128,256,512` were respectively about `0.062,0.031,0.016,0.008,0.004`.  Meanwhile repeated periods keep increasing pair counts.  Exact scale frequencies without phase mixing are therefore insufficient.
- Revisited whether one *short* ruler period could be amplified by independent random relabelings.  Exact periods of length `2^t` used approximately `2^(t/2)` distinct labels (not `O(t)`) and supported essentially a path on those labels.  More decisively, at the number of copies needed for edge coverage, a fixed ambient pair appears in `Theta(n)` singleton copies (copies containing exactly one endpoint).  Those singleton projections alternate across copy boundaries and force linear order.  This falsifies the tempting calculation that counted only copies containing both endpoints.

### Linear rather than arbitrary child bijections

- Tried affine-linear identifications of every child support with the canonical smaller alphabet, hoping that pair trees would depend only on the `n-1` nonzero difference vectors and could be balanced deterministically.
- The natural linear maps give an explicit exponential bad family: for dimensions `d=4,...,9`, the maximum pair count doubled as `24,48,96,192,384,768`, while coverage fell to about `0.025` at `d=9`.  Thus fresh random/nonlinear relabeling is essential to the proved construction.
- Linear algebra explains the persistence.  The double-child differences form a codimension-two subspace.  Under any child linear isomorphism its image is a hyperplane, which must intersect the next double-child subspace in codimension at most one.  Hence at least half of the double-child differences remain double-child along each branch.  Two branch maps cannot make the two bad preimages disjoint because both are subspaces containing zero.  This rules out the simplest proposed deterministic anti-branching map, though not arbitrary nonlinear balancing.

### Hard-cap alteration of the harmonic process

- Tested a direct attempt to force maximum order: reject any proposed prefix rotation that would increment a pair already at budget `h=q log n`, and resample a rank.  The total-count heuristic suggested that only `O(g/q)` of pairs could saturate in a run of `gN` accepted moves.
- This heuristic is false because saturated edges can concentrate.  In every tested run (`n=100,...,1000`) the process deadlocked: about `Theta(n)` saturated edges formed essentially a star around the current front symbol, although their global density was only `Theta(1/n)`.  Since every nontrivial next access crosses the current front pair, no move was feasible.  This is an explicit obstruction to any alteration argument that controls only the **number** of over-budget pairs; degree/distribution control is indispensable.

## 2026-08-28 02:37 CEST (Unix `1787877454`): separate adversarial audit

- Completed a fresh line-by-line audit of the two claims in `PROOF.md`, recorded separately in `AUDIT.md`.
- Re-derived, rather than assumed, every deterministic identity, branching distribution, moment recurrence, MGF inequality, parameter asymptotic, and simultaneous-event argument.
- Exhaustively checked the skeleton contraction on every repetition-free word on at most four symbols and length at most nine.  Support and defect were always preserved and no pair count increased.
- Exhaustively checked `P<=k^2+(k+1)M_k` on every repetition-free word on at most five symbols and length at most eight.
- Independently iterated the critical MGF recurrence through depth 3000; its numerical excess over one was about `0.01/t`, versus the proved upper bound `1/t`.
- Audit outcome: no unsupported step, hidden independence assumption, parity issue, or counterexample was found in the polylogarithmic sufficient theorem or the `omega(log n)` necessity theorem.  The audit explicitly does not certify an exact threshold inside the remaining gap.

### Most promising unresolved alteration

- The recursive construction has exactly `Theta(N log n)` pair-tree node mass in aggregate but pays an `L_infinity` tail to control every pair.  Fresh independent child bijections distribute this mass randomly and the union bound yields the extra `log n/epsilon^2` maximum scale.
- A plausible next route is **adaptive load-balanced child relabeling**: at each recursive invocation, choose among several bijections to minimize a global exponential or maximum edge-load potential (a graph-valued analogue of the power-of-two-choices process).  If this can keep every root pair near the `Theta(log n)` average while preserving the branching survival density, the Working-Set lower scale could be approached.
- Equivalently, one would try to impose negative dependence across generations: pairs that branch early should be routed toward later death, while the `Theta(1/t)` surviving roots postpone most of their branching until the last `O(log t)` levels.  Abstract offspring counts allow total progeny `O(t)` under such a schedule; the unresolved issue is realizing it simultaneously by vertex bijections of the child blocks.
- The exact obstruction is a coupled graph-packing/discrepancy statement: a child bijection permutes an entire weighted complete graph of pair loads, not independent balls, so standard scalar load-balancing bounds do not apply directly.  No theorem proving the required simultaneous edge-load bound was obtained.

### Larger-field version of the branching construction

- Generalized the recursion formally from `F_2` to `F_q`: use all `q^2` evaluation blocks `(x,v)`, so each symbol lies in `q` blocks and a random pair's common-child count is dominated by `Bin(q,1/q)` when the evaluation map has full rank.  The offspring mean remains one and its variance remains bounded away from zero, while singleton blocks make the projection cost per tree node `Theta(q)`.
- With depth `d=Theta(log n/log q)`, the same thinning/union calculation gives the maximum scale
  `Theta(q (log n)^3/((log q)^2 (log log n)^2))` up to lower-order logarithms.  The factor `q/(log q)^2` is minimized at a constant `q`; allowing `q` to grow cannot improve the asymptotic order.  Thus changing the base field only optimizes constants and does not close the logarithmic gap.

### Additional finite search

- Revisited the unresolved complete-support scaffold on six symbols at order three with a randomized budget-aware search.  It reached 13 of the 15 pair types but found no full witness in the allotted run.  This is not exhaustive and supplies no nonexistence result; the earlier certified facts for `n<=5` are unchanged.
- As a positive control, found and directly verified an order-four complete-support word on six symbols:
  `0 5 3 2 1 3 4 1 5 4 0 2 4 2 5 1 0 3`.
  Its fifteen pair-change counts are all at most four.  Thus the minimum for `n=6` is certified to lie in `{3,4}`; the order-three side remains undecided.
- Found and verified an order-four complete-support word on seven symbols:
  `3 4 0 6 3 1 6 2 4 5 6 4 1 5 3 2 5 0 2 1 0 3`.
  A corresponding order-four search for eight symbols reached 25 of 28 pairs but no witness; that latter negative search was not exhaustive and is not a result.
- As a further positive control, found a verified order-five complete-support word on eight symbols:
  `6 2 7 3 2 5 7 1 6 7 0 4 2 1 0 6 4 5 6 3 0 2 0 5 3 4 7 4 1 3 1 5`.
- A time-bounded order-five search for nine symbols reached 35 of 36 pair types but no full witness; this was nonexhaustive and yields no negative conclusion.
- An order-six positive-control search did find and verify a complete-support word on nine symbols:
  `1 8 0 3 2 8 4 2 1 4 0 2 7 6 2 5 0 6 5 3 7 5 4 6 1 3 8 6 3 4 7 8 5 1 7 0 1`.
- The final nonexhaustive order-six search for ten symbols reached 44 of 45 pair types but no full witness; no negative claim is made.
- An order-seven positive control on ten symbols produced the verified complete-support word
  `8 6 9 0 4 6 2 0 6 7 0 8 7 1 0 3 7 2 8 4 7 5 6 3 4 1 6 4 5 1 8 3 1 2 4 9 1 9 2 5 9 8 5 3 2 3 9 7 0 5`.
- The same search found a verified order-seven complete-support word on eleven symbols:
  `2 8 10 2 9 3 8 6 3 0 8 9 0 6 1 8 7 9 6 7 3 4 6 10 1 4 10 9 1 7 10 0 7 4 2 3 10 5 4 8 5 0 4 9 5 3 1 5 6 2 1 0 2 5 7 2`.
  A final 28-second order-seven search on twelve symbols reached 63 of 66 pairs but no witness; this is explicitly nonexhaustive.

## 2026-08-28 03:03:57 CEST (Unix `1787879037`): search threshold reached

- Elapsed wall-clock proof-search interval since the recorded start `1787871803`: `7234` seconds, exceeding the requested `7200` seconds.
- No proof of the exact smallest growth rate was obtained.  The strongest complete and separately audited result remains the window
  `s/log n -> infinity` (necessary) and
  `s >= C(log n)^3/(log log n)^2` (sufficient).
- The sufficient theorem answers the highlighted question affirmatively because its scale is `o(sqrt(n))`.
- Final artifacts: `PROOF.md` (complete proof of the window), `AUDIT.md` (separate adversarial audit), and this exhaustive chronological worklog.

### Why survival-based critical recursions have a tail cost

- Rechecked a general limitation of the present proof architecture.  A critical depth-`t` pair tree has expected total progeny `Theta(t)` and its certified survival scale is `Theta(1/t)`.  A critical tree conditioned to survive to depth `t` has total progeny on the `t^2` scale (the standard size-biased calculation).  In the actual thinned construction the proof certifies survival `Omega(epsilon p^t)`; independently, the dominating subcritical tree's unconditioned total-progeny exponential tail has scale `1/epsilon^2`, exactly as the fixed-point MGF calculation shows.
- This does not prove a lower bound for arbitrary DS scaffolds, and no claim about the exact conditional mean in the finite-depth subcritical tree is needed.  It does identify why merely sharpening constants cannot remove the `1/epsilon^2` MGF scale.  A genuine improvement must either balance/prune the all-pairs maximum or certify support by a mechanism not tied to the same branching tail.
- As a calibration, simulated `2^t` independent critical binary trees for `t=8,...,18`.  Their maximum total progeny was consistently about `0.07--0.10 t^3`, while the mean was `Theta(t)`.  This is not a proof about the correlated pair trees, but it confirms that the proof's `t^3` union scale is the correct extreme-value scale for independent trees rather than a numerical artifact of loose constants.

### Final revisit of nested gaps

- Retained the stronger invariant omitted in the first local-Ramsey attempt: every shrinking clique still has complete adjacent support inside its parent gap.  This does not repair the argument.  The support edge between an older reference `x_i` and a later `x_j` can be placed in the annulus outside the chosen `x_i`-gap, while all later occurrences remain nested inside it.  Their projection can still be only `x_i x_j x_i`, independent of nesting depth.  No forced alternating pair follows, so the route gives no lower bound beyond the verified working-set estimate.
