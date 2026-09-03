# Proof-search report: universal relation followed by a function

## Status and conventions

Start Unix time: `1787909318`.

End Unix time: `1787916520`.  Elapsed active search: `7202` seconds.

Outcome: no complete proof was obtained.  The all-`g` statement remains an open conjecture in the primary literature checked, and none of the attempted arguments below closes its depth-fortification/row-selection gap.  Accordingly, no `solution.md` is presented as if the conjecture had been proved.

Write `h=g^m`, so that `h(X)=(g(X_1),...,g(X_m))`.  The ordinary composed relation in the problem is the generalized KW relation for `h`: on inputs with `h(X) != h(Y)`, output any raw coordinate `(i,j)` at which `X` and `Y` differ.  Crucially, the chosen row need not satisfy `g(X_i) != g(Y_i)`.

The exact little-`o` assertion also requires an asymptotic family and a specified “relevant range” of `m,n`; the supplied problem does not state these.  All asymptotic conditional statements below are to be read along a family for which `r=min{m,CC(KW_g)}` tends to infinity.

The target is Conjecture 1.4 in Hao Wu's 2023 paper, not a theorem stated elsewhere in the supplied source.  Wu proves the quoted near-additive result only for most/random inner functions in the specified range.  Dinur--Meir had earlier isolated the arbitrary-`g` dense-core statement and its `1-out-of-k` special case as open conjectures.  A literature search through later primary work found partial and strong-composition results, but no proof of the all-`g` assertion.

## Unconditional results verified during the search

Let `C=CC(U_m diamond KW_g)` and `D=CC(KW_g)`.

### 1. Elementary restrictions

For fixed representatives `z_0 in g^{-1}(0)` and `z_1 in g^{-1}(1)`, the restriction `X_i=z_{a_i}`, `Y_i=z_{b_i}` locally embeds `U_m`: a raw difference in row `i` certifies `a_i != b_i`.  Hence

`C >= CC(U_m) = m-O(1)`.

Fixing every row but one identically and allowing the remaining row to be an oppositely colored pair embeds `KW_g`, so `C >= D` (up to the harmless orientation convention).  Therefore

`C >= max{m-O(1),D} = m+D-min{m,D}-O(1)`.

This is the strongest bound obtained from independent restrictions; it loses the entire smaller summand.

### 2. Formula-leaf restriction lemma

If an outer Boolean function `f` depends on all `m` variables, then

`L(f diamond g) >= m L(g)`.

Proof.  For a formula `F` computing `f diamond g`, let `ell_i` be the number of leaves labeled by variables in row `i`.  Since `f` depends on bit `i`, there is a fixing of the other outer bits under which `f` becomes bit `i` or its negation.  Fix the corresponding other rows to `z_0,z_1`.  After simplifying constants, `F` gives a formula for `g` or `not g` with at most `ell_i` leaves.  Thus `ell_i>=L(g)` for every `i`, and summing proves the claim.

Since the composed universal relation restricts to `KW_{f diamond g}` for every `f`, this gives

`C >= log m + log L(g)`.

This does not yield the desired depth coefficient because only `log L(g)=Omega(D)` with a constant-factor loss follows from general formula balancing.

### 3. Universal-stage lemma

Choose nonempty equal-cardinality sets `H_0 subset g^{-1}(0)` and `H_1 subset g^{-1}(1)`, write `|H_0|=|H_1|=q`, and put `X_0=(H_0 union H_1)^m`.  Every `h`-fiber in `X_0` then has cardinality `q^m`.

Run a depth-`c` protocol on off-promise diagonal pairs `(Z,Z)`.  At level `t`, at most `2^t` transcript rectangles partition the diagonal points, so some transcript has diagonal intersection `S subset X_0` of relative density at least `2^{-t}`.  In the relaxed relation, a rejecting leaf can contain diagonal points from only one `h`-fiber: otherwise a cross pair from two values is valid but is rejected.  In the strict-promise relation, a leaf labeled by raw coordinate `q_0` can contain diagonal points from at most two `h`-fibers: representatives of any two distinct values must have opposite `q_0`-bits, and three values violate this by pigeonhole.

It follows (with only a constant convention difference between strict and relaxed games) that

`c >= t + min_{S subset X_0, density(S)>=2^{-t}} CC(KW_h restricted to S x S)`

for all relevant `t<m`.

The same proof has a useful weighted form that avoids fiber-cardinality issues.  Choose arbitrary distributions `mu_0,mu_1` supported on the two `g`-fibers, first choose each outer bit uniformly, then sample its row from `mu_bit`, independently across rows.  The resulting `mu` makes `h(Z)` uniform.  Averaging produces a transcript event `S` of `mu`-mass at least `2^{-t}`, and the suffix solves the restriction to `S x S`.  A rejecting leaf has mass at most `2^{-m}` and a strict coordinate leaf's diagonal intersection has mass at most `2^{1-m}`, by the one-/two-value argument.  Thus all stage statements above remain valid with relative cardinality replaced by `mu`-mass.

There is also a one-copy balancing lemma.  If `A=g^{-1}(1)`, `B=g^{-1}(0)`, and `s=min{|A|,|B|}`, then there are equal-cardinality `H_1 subset A`, `H_0 subset B`, each of size `s`, for which

`CC(KW_g restricted to H_1 x H_0) >= D-ceil(log_2 ceil(max{|A|,|B|}/s))`.

To prove it, partition the larger fiber into at most `ceil(max{|A|,|B|}/s)` pieces of size at most `s`, pad each piece within that fiber to size `s`, and suppose every resulting restriction had depth at most `d`.  The player holding the larger-fiber input could send its piece index and then run the corresponding protocol, giving `D<=d+ceil(log_2 number_of_pieces)`.  This lemma removes a mere fiber-cardinality imbalance, but it does not provide robustness after taking `m` correlated copies.

### 4. Range lemma

For every vector-valued map `h` and every set `S`,

`CC(KW_h restricted to S x S) >= log_2 |h(S)|-1`.

Indeed, run the protocol on every diagonal `(z,z)`.  At a coordinate leaf, the preceding cross-pair argument permits at most two distinct `h`-values among its diagonal points.  A depth-`d` tree has at most `2^d` leaves, so `|h(S)|<=2^{d+1}`.

Applied after the stage lemma, this recovers only the outer `m-O(1)` lower bound.  It cannot distinguish multiple representatives inside one `h`-fiber.

### 5. Simultaneous formula-skeleton lemma

One protocol for the generalized relation induces a formula for `f diamond g` for every coloring `f:{0,1}^m->{0,1}`.  Moreover, all these formulas use the same AND/OR tree skeleton: the speaking party at a protocol node fixes the corresponding gate; only the sign of a fixed leaf coordinate, constants, and pruning depend on `f`.  At a leaf restricted to `f(h(X))=1,f(h(Y))=0`, all cross pairs are valid, so the leaf coordinate has a fixed orientation and is a legitimate literal.

A depth-`c` protocol tree has at most `2^c` leaves.  For each `f`, a fixed protocol leaf becomes one of its two coordinate literals or one of two constants, so the tree produces at most `4^{2^c}` formulas.  Since `g` is nonconstant, `h` is onto and the `2^{2^m}` functions `f diamond g` are distinct.  Counting therefore yields only

`c >= m-1`.

No dependence on `D` follows without controlling cancellations by subformulas that are not individually constant on `g`-fibers.

### 6. Diagonal entropy identity (relaxed relation)

For a correct protocol `Pi`, let `T=Pi(Z,Z)`.  The rejecting transcript determines `h(Z)`, by the same cross-pair argument as above.  Hence, under any diagonal distribution with uniform `h(Z)`,

`H(T)=m+H(T | h(Z))`.

This proves that leakage about inner representatives during the outer stage contributes genuine transcript entropy.  The missing implication is from low conditional entropy to residual deterministic depth `D`; arbitrary non-monotone KW relations do not have a general protocol-independent hard distribution.

### 7. Deterministic partition tradeoff

For arbitrary partitions `A=union_{p=1}^P A_p` and `B=union_{q=1}^Q B_q` of the two sides of a KW rectangle,

`max_{p,q} CC(KW_g restricted to A_p x B_q) >= D-ceil(log_2 P)-ceil(log_2 Q)`.

Otherwise Alice and Bob send their cell indices and run the corresponding restricted protocol, contradicting the definition of `D`.  This is a protocol-dependent substitute for a hard-distribution argument: if an early transcript induces few cells in an inner fiber, some cell pair stays hard.  It still does not prove the composition bound, because the two cell indices may cost twice the diagonal leakage, and the hard cell pair can depend on the outer context/row.  Those preferences need not align in one surviving outer transcript.

## Exact conditional reduction to the missing hard core

Let `r=min{m,D}` and `epsilon=o(1)`.  Suppose there is a balanced `X_0` (equal-size nonempty `h`-fibers) such that every `S subset X_0` of density at least `2^{-(m-epsilon r)}` obeys

`CC(KW_h restricted to S x S) >= D-epsilon r`.

Taking `t=m-epsilon r-O(1)` in the universal-stage lemma gives

`C >= m+D-2 epsilon r-O(1) = m+D-o(r)`.

Thus a depth-preserving fortified hard core proves exactly the requested result.  Establishing that premise for arbitrary `g` is the unresolved step, not an omitted routine estimate.

Equivalently, the balanced-set premise may be replaced by its weighted version: it is enough to find conditional row distributions `mu_0,mu_1` such that every event of product-mixture mass at least `2^{-(m-epsilon r)}` retains depth `D-epsilon r`.  This removes any imbalance between `|g^{-1}(0)|` and `|g^{-1}(1)|`; what remains is genuine depth fortification, not counting.

## Explicitly discarded claims and counterexamples

1. **Ordinary composition is not strong composition.**  With `g=XOR_2`, rows `00` and `11` have the same `g`-value but differ in both raw coordinates.  If another row supplies the outer promise, an ordinary protocol may legally output a coordinate in this equal-output row.

2. **A dense set need not contain an adjacent pair of outer values.**  The even-parity subset of `{0,1}^m` has density `1/2` and no Hamming-distance-one pair.  More generally, sparse high-distance codes survive at the densities supplied near the end of the universal stage.  Comparing two surviving fibers can therefore create a distinct-row `1-out-of-k` KW game.

3. **Large projections do not give a large common fiber.**  The even-parity set projects fully onto every `m-1` coordinates, yet fixing those coordinates determines the last one.  Entropy of row projections alone cannot locally embed a fresh copy of `KW_g`.

4. **The uniform full-domain fortification statement is false.**  Define `g(p,z)=h(z)` on the rare prefix `p=00000`, and make `g` a dictator outside that prefix.  Matrices with no special-prefix row have density `(31/32)^m=2^{-Theta(m)}` and induce an easy inner behavior even though `g` can inherit the large depth of `h`.

5. **A universal-minor shortcut fails for `k>=3`.**  Under a fixed coordinatewise local output decoder, an encoding of `U_k` into binary `KW_g` would force Alice's and Bob's encoded bits to agree on every diagonal string, contradicting their opposite `g`-values.  The proof chains through a third string in each fixed-bit fiber.  The threshold has a genuine exception: `U_2` embeds into `KW_PARITY_3` via `alpha(u)=(u_2,u_1,u_1 xor u_2)` and `beta(v)=(not v_2,not v_1,not(v_1 xor v_2))`.

6. **Leaf/rank potentials do not encode depth additively.**  Minimum leaf count is subadditive under one-party partitions but measures `log L(g)`.  Exact depth rank loses one in a preferred child, and preferred children can differ across outer candidates.  A weighted aggregate then loses both an outer factor two and an inner-rank factor per message, giving only a convex-combination/max bound.

7. **Information lower bounds alone are blocked.**  Worst-case deterministic KW depth cannot generally be certified by a single hard distribution; this is the known randomized-complexity barrier for non-monotone KW relations.

## Computation on small cases

An exact rectangle-recursion checker verified, under the strict generalized-KW convention:

- `m=1,n=2`: the AND and XOR representatives have depth `2`;
- `m=2,n=1`: the dictator case has depth `2`;
- `m=2,n=2`: every non-dictator nonconstant two-bit function has composed depth `4`, while dictators have depth `2`.

These cases support exact additivity and provide no counterexample.  Three-bit/two-row searches using a restricted predicate family likewise found no shorter protocol, but their negative verdicts were not exhaustive and are not used as proofs.

## Remaining obstruction and best next route

After approximately `m` bits, the universal-stage lemma leaves a dense but potentially highly correlated set `S`.  Its outer values can form a code, and a suffix may choose whichever of several differing rows is easiest.  Proving that this choice retains `D(g)-o(D(g))` is the `1-out-of-k`/depth-fortification obstruction.  Repetition would make the reduction from one KW copy immediate, but the rows in the relevant hard instance must be distinct and arbitrary `g` need not have fiber-preserving symmetries.

The most promising next route is a depth-sensitive, protocol-dependent fortification theorem that controls the correlated choice of a row without passing through a protocol-independent hard distribution.  In the relaxed formulation, a concrete version uses the protocol's rejecting leaves: for each outer value `a`, diagonal inputs in `h^{-1}(a)` partition into `K_a` rejecting leaves, and `sum_a K_a` is at most the total protocol size.  For adjacent `a,b`, these leaf partitions induce partitions of the two sides of one copy of `KW_g`; the deterministic partition tradeoff leaves a hard cell pair.  If one could prove that some such hard pair's two rejecting leaves have a common prefix of length `m-o(r)`, the remaining suffix would give the desired `D-o(r)` term.  Ordinary tree counting finds deep adjacent leaf pairs but does not ensure that the *hard* cell pair is one of them.  This colored-tree alignment problem is an exact, protocol-dependent version of the row-selection obstruction.

## Primary references checked

- Hao Wu, [*An Improved Composition Theorem of a Universal Relation and Most Functions via Effective Restriction*](https://eccc.weizmann.ac.il/report/2023/151/), especially Conjecture 1.4 and Theorem 1.5.
- Irit Dinur and Or Meir, [*Toward the KRW Composition Conjecture: Cubic Formula Lower Bounds via Communication Complexity*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol050-ccc2016/LIPIcs.CCC.2016.3/LIPIcs.CCC.2016.3.pdf), especially Conjectures 9.3, 9.4, and 9.6.
- Nikolai Chukhin, Alexander S. Kulikov, and Ivan Mihajlin, [*Toward Better Depth Lower Bounds: Strong Composition of XOR and a Random Function*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol327-stacs2025/LIPIcs.STACS.2025.26/LIPIcs.STACS.2025.26.pdf), for the later status and distinction between ordinary and strong composition.
