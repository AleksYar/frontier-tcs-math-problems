# Moderate III: two-hour proof-search report

## Outcome and timing

The target in `yoav-danieli-shapprox-moderate-3.pdf` is:

> For every fixed `k >= 1`, decide in polynomial time, from a minimal DFA `A`, whether `h(L(A)) <= k` or `h(L(A)) > 2k`, under that promise.

The search began at Unix time **1787930149** and reached its terminal audit at Unix time **1787937355**, for **7206 seconds** of continuous proof search. I did **not** obtain a complete proof. I also did not find an unconditional counterexample to the algorithmic conjecture. The statement in the supplied document is explicitly a conjecture, and a current exact-statement search found no published resolution.

This report therefore gives only results that were independently checked. It does not present any heuristic as a theorem.

## Verified baseline

Eggan's theorem gives

`h(L) = min { r(B) : B is an NFA accepting L }`,

where `r` is directed cycle rank. It follows that `h(L(A)) <= r(A)`, but the minimum is over all equivalent NFAs, not the input DFA. The known exact algorithms do not make this minimum polynomially accessible: Kirsten's construction reduces star height to limitedness of nested distance/desert automata and has a double-exponential-space bound for NFA input; the later literature records EXPSPACE as the best general DFA upper bound. The Stamina implementation constructs a stabilisation monoid exponentially larger than its cost automaton and uses loop/sharp-expression tests only as heuristics.

Primary sources used for this baseline are [Kirsten's 2005 paper](https://www.numdam.org/articles/10.1051/ita%3A2005027/), [Gruber's cycle-rank/star-height survey and results](https://arxiv.org/abs/1111.5357), [the Stamina paper](https://perso.ens-lyon.fr/denis.kuperberg/papers/CIAA17.pdf), and [Bojanczyk's game characterization](https://www.mimuw.edu.pl/~bojan/upload/conflicsBojanczyk15.pdf).

## Strongest verified structural statements

### 1. Quotient localization

Left and right quotients by words do not increase ordinary star height. For a letter, the usual derivative identities preserve nesting depth:

`D_a(EF)=D_a(E)F union (nullable(E) ? D_a(F) : empty)` and
`D_a(E*)=D_a(E)E*`.

Iteration gives left word quotients; reversal gives right quotients.

Moreover, for every positive-height language,

`h(L) = max_{a in Sigma} h(a^{-1}L)`.

The nontrivial inequality follows from

`L = (epsilon if epsilon in L) union union_a a(a^{-1}L)`,

which adds no star. Repeatedly choosing a height-preserving derivative eventually enters a cycle of the finite residual automaton. Consequently:

- some reachable SCC of the minimal DFA carries residuals of the full height `h(L)`;
- residual heights are constant within each SCC, because mutually reachable residuals are mutual quotients;
- heights are nonincreasing along the condensation DAG.

This localizes high height to recurrent residual behavior, but it is not an algorithm because the residual height is not determined by the visible SCC graph.

### 2. Polynomial special cases and one-sided tests

- **Unary alphabets.** Every unary regular language is ultimately periodic and has ordinary star height at most one. Thus for `k>=1` no promised NO instance exists.
- **Bideterministic minimal trim DFAs.** McNaughton's theorem gives `h(L(A))=r(A)`. For fixed `k`, the recursive definition of cycle rank yields an `n^{O(k)}` exact threshold algorithm: decompose into SCCs and, in a cyclic strongly connected graph, branch over the vertex whose deletion reduces the budget.
- **Sound promised-YES test.** If `r(A)<=2k`, then Eggan gives `h(L(A))<=2k`; under the promise this cannot be a NO instance.
- **Sound promised-NO test.** Enumerate all left quotients by choosing each DFA state as initial, trim/minimize, and retain the bideterministic quotients. If any has cycle rank greater than `2k`, McNaughton and quotient monotonicity prove `h(L)>2k`. This is polynomial for fixed `k`, but incomplete because the height-preserving quotient from the localization lemma need not be bideterministic.
- If the number of states is at most `k`, Eggan and `r(A)<=n` give an immediate YES answer.

### 3. The analogous NFA gap is PSPACE-hard

Fix a binary language `K` of height `2k+1`. From an NFA for `L`, Kirsten's construction forms

`L' = Sigma* c L union K c Sigma*`.

If `L=Sigma*`, then `L'=Sigma* c Sigma*` has height one. If `L` is not universal, Kirsten's lemma gives `h(L')>=h(K)=2k+1`. Hence the same `k` versus `2k` gap is PSPACE-hard for NFA input. This does not settle the DFA conjecture because determinization may be exponential, but it rules out any proposed proof that applies unchanged to NFAs.

There is a second, independent verification barrier: universality remains PSPACE-complete for partially ordered NFAs over a fixed alphabet. Such NFAs have only self-loops as cycles and therefore cycle rank at most one. Thus even coverage of `Sigma*` by a fixed-rank NFA is PSPACE-hard. See [Krötzsch--Masopust--Thomazo](https://arxiv.org/abs/1609.03460).

### 4. Height-one inputs can hide exponential residual correlations

For `m>=1`, let `J_m` be the binary words of lengths from `m` to `2m` whose `m`-th symbol from the beginning is `1`. It has an `O(m)`-state DFA. Its reverse has at least `2^m` left quotients: for distinct `x,y in {0,1}^m`, choose a differing coordinate `j` and append a word of length `j-1`; membership then queries coordinate `j` as the `m`-th symbol from the end.

With a fresh reset letter `c`, define

`L_m = J_m union Delta* c J_m`, where `Delta={0,1,c}`.

The corresponding `O(m)`-state DFA is strongly connected because every state resets to the initial state and every state is reachable from it. The language is infinite and the displayed expression has height one. Also

`L_m^R intersect {0,1}* = J_m^R`,

so the reverse minimal DFA has at least `2^m` states. Thus even strongly connected height-one YES instances can require exponentially many reverse columns/subsets. Direct computations for `m=1,...,8` gave reverse subset counts `6,12,24,48,96,192,384,768`.

### 5. A height-one language can have an arbitrarily high state fiber

This is the strongest new obstruction found in the final audit.

Let `G` be a finite loopless strongly connected digraph of arbitrarily large cycle rank; a sufficiently long symmetric directed path suffices. Give every edge a distinct letter, fix a vertex `v`, and let `K` be the language of edge sequences forming a closed walk at `v`. The edge-labelled automaton is minimal and bideterministic, so

`h(K)=r(G)`,

which is arbitrarily large.

Let `E` be the edge alphabet. For a vertex `u`, let `I_u` and `O_u` be its incoming and outgoing edge letters. They are disjoint because `G` has no self-loops. Put

`C_u = (O_u union (E \ (I_u union O_u)) union I_u O_u)* (epsilon union I_u)`.

Here every set difference denotes a finite union of letters, so this is an ordinary height-one expression. It says exactly that an incoming edge at `u`, unless last, is immediately followed by an outgoing edge at `u`. Also put

`S = epsilon union O_v E*`, and `T = epsilon union E* I_v`.

Then

`K = S intersect T intersect intersection_u C_u`:

the conditions impose the first vertex, every adjacency, and the final vertex. Enumerate these height-one languages as `R_1,...,R_m`, introduce fresh letters `d,c_1,...,c_m`, and define

`L = union_i R_i d c_i`.

The displayed expression has height at most one, and `L` is infinite, hence `h(L)=1`. After the prefix `w d`, the residual of `L` is exactly

`{c_i : w in R_i}`.

Therefore the all-markers residual is reached exactly by the prefixes `w d` with `w in K`. Fresh markers ensure that no pre-marker, completed, or malformed prefix has that residual. The transition fiber of this minimal-DFA state is exactly `K d`. Since `(K d)d^{-1}=K`, quotient monotonicity and the trivial concatenation upper bound give

`h(Kd)=h(K)`.

Thus state annotation can increase height without any bounded factor, even when the root language has height one. This decisively invalidates any proof based on a universal `2h` bound for entry/exit or syntactic state fibers.

## Explicit counterexamples to false subclaims

### Minimal-DFA cycle rank is not a 2-approximation

Let

`F={aa,aaa,aaab,aaba,ab,abab,abba,b,bbab}` and `L=F*`.

The language is infinite and the displayed expression has height one. Its trim minimal DFA has initial state `0`, accepting states `0,...,5`, rejecting state `6`, and transitions

| state | `a` | `b` |
|---:|---:|---:|
| 0 | 6 | 0 |
| 1 | 6 | 5 |
| 2 | 4 | 5 |
| 3 | 3 | 2 |
| 4 | 3 | 1 |
| 5 | 4 | 0 |
| 6 | 2 | 1 |

Its cycle rank is exactly three. An upper certificate deletes `0`, then `1`, then `3`. For the lower bound, after deletion of any one vertex a remaining SCC contains two vertex-disjoint cycles:

- delete `0`: `(3)` and `(1,6)`;
- delete `1`: `(0)` and `(3)`;
- delete `2`: `(0)` and `(1,6)`;
- delete `3`: `(0)` and `(1,6)`;
- delete `4`: `(0)` and `(1,6)`;
- delete `5`: `(3)` and `(1,6)`;
- delete `6`: `(3)` and `(1,5,4)`.

Hence `r(A)=3>2h(L)=2`. A direct word-break implementation agrees with the DFA through length 18, all seven states have explicit reaching words, and all 21 state pairs have distinguishing suffixes of length at most three.

### Other falsified surrogates

| Proposed surrogate | Verified counterexample |
|---|---|
| Full universal-automaton rank `<=2h` | The preceding `F*` language has nine trim universal states of exact rank 4. |
| Canonical morphic image rank `<=2h` | A separate finite dictionary-star language has a rank-one bouquet NFA but an 11-state canonical image of exact rank 3. |
| `min(r(D_L),r(D_{L^R}))<=2h` | For the preceding `H=F*`, `S=cHd union dH^R c` is reversal invariant, has height one, and its forward and reverse minimal DFAs both have rank 3. |
| Reverse/subset size polynomial on low-height or strongly connected inputs | The reset family `L_m` above has height one, `Theta(m)` forward states, and at least `2^m` reverse states. |
| Bounded-cardinality subset automata have low rank | On the seven-state `F*` language, the singleton version has rank 3, while cardinality bounds two and three already have rank greater than 4. |
| Canonical state slicing costs at most a factor two | The closed-walk/intersection-marker construction above gives a height-one root language with an arbitrarily high state fiber. |
| Coverage of a DFA by a low-rank NFA is easy | Universality is PSPACE-complete already for partially ordered/rank-one NFAs. |

These counterexamples attack different failure modes: deterministic graph inflation, canonical merging, reversal state complexity, subset correlation, state slicing, and NFA coverage. Repairing one does not repair the others.

## Approaches attempted and why they failed

The detailed timestamped record is in `WORKLOG.md`. The routes can be grouped as follows.

1. **Input-graph surrogates (Routes A, H, V, Y).** Minimal-DFA cycle rank, entanglement, the minimum of forward/reverse ranks, and de Bruijn-core rank were tested. Explicit examples destroy the needed factor-two inequalities. The de Bruijn computations gave ranks `2,2,3,4,6` in dimensions `1,...,5`, but no general lower bound was claimed.

2. **Exact limitedness and game constructions (B, K, Q, R, W).** Kirsten's cost automaton, the stabilisation monoid, and Bojanczyk's limitedness game are sound and complete. Their finite control stores sets of transformations/residuals, and those sets are exponential before the game is solved. Stamina's state-elimination-induced sharp witnesses are sound lower certificates but only heuristic: the global factorisation theorem can produce algebraic products not induced by the chosen circuit. No proof showed that height greater than `2k` forces one of the polynomially induced witnesses.

3. **Universal, saturated, and concept automata (C, I, J, S, AD).** The universal automaton can be double exponential, and the literature leaves open whether it always contains a minimum-loop-complexity equivalent subautomaton. The saturated core is a valid lower bound but can be zero and depends on the exponential backward automaton. The full universal automaton and a canonical image both violate `rank<=2h` on explicit height-one examples. Restricting to finitely many Hankel rows loses the untracked entries needed to validate a concept/rectangle.

4. **Expression compression and state annotation (D, Z, AC, AE).** Pumping an expression uniformly needs equality of transformations on every possible entry state, whose natural domain is the exponential transition monoid. Entry/exit annotation turns a star into a path problem on a DFA-state graph and can add its whole cycle rank. The final construction proves more strongly that a height-one root language can have an arbitrarily high state fiber. Thus no universal factor-two slicing theorem exists.

5. **State-local, alternating, and relation abstractions (E, M, T, AB).** Letting a strategy see one DFA state changes the quantifier order: later choices may depend on a state that a genuine expression cannot observe. Union-of-graphs relations erase word correlation so completely that every regular language receives bounded height-zero covers by shortest representatives. Tracking `O(k)` states would be polynomial, but no Helly theorem makes those tuples universal over all compatible states; low-height languages can have arbitrary monoid complexity.

6. **Small or canonical low-rank NFAs (F, L, N, O, P, AA).** A small-witness theorem would still need polynomial coverage verification. That verification is PSPACE-hard even at rank one. Products that make nondeterministic choices online can raise rank, and cardinality-bounded subset automata are already high-rank on height-one examples. No canonical polynomial fold with both a `2k` rank guarantee and a direct equivalence certificate was found.

7. **Pure syntactic-monoid invariants (G).** Pin's construction places arbitrary finite monoids as divisors of syntactic monoids of languages `F*` of height one. Related inverse-morphism results recover arbitrary regular behavior from restricted height-one languages. Hence ordinary star height above zero is not controlled by a simple monoid variety or bounded algebraic pattern.

8. **Hardness transfer from NFAs (U).** Accepting-run annotations make a polynomial DFA language whose homomorphic image is the NFA language, so the high-height direction transfers. The universal-NFA/low-height direction fails because rejecting or malformed annotations remain excluded. Encoding whole reachable subsets makes the checker exponential; local tableau encodings cannot enforce equality of successive `n`-bit subsets with polynomially many DFA states.

9. **Bideterministic quotient/sandwich witnesses (X).** Quotient localization guarantees a quotient of equal height but not a bideterministic one. The saturated-core construction is a special sandwich lower bound, but it may be trivial and requires exponential backward information. No theorem shows that height above `2k` yields a polynomially enumerable bideterministic rank-above-`k` subquotient.

## Exact remaining obstruction

Every sound-and-complete characterization examined must preserve the simultaneous action of a word on a set of residual states, or equivalently a correlated set of transition-monoid elements. These sets have exponentially many reachable values even for strongly connected height-one DFAs.

The obvious compressions all fail:

- projecting to individual states is unsound;
- slicing by state can increase star height arbitrarily;
- retaining only bounded-cardinality subsets produces high-rank graphs;
- canonical merging can raise rank beyond `2h`;
- guessing a low-rank NFA leaves a PSPACE-hard coverage problem.

Therefore a proof needs a new promise-specific theorem of one of the following forms:

1. a polynomially representable upper certificate guaranteed whenever `h(L)<=k`; or
2. a polynomially enumerable lower witness guaranteed whenever `h(L)>2k`;

together with a proof that removing the residual correlations loses at most the factor two. None of the inspected exact algorithms, games, quotient identities, or canonical automata provides that theorem.

## Most promising next route

The most focused remaining route is to turn Stamina's loop/sharp-expression heuristic into a promise theorem. For a fixed `k`:

1. Build only the sharp witnesses induced by a polynomial-size state-elimination circuit.
2. Prove the semantic implication

   `h(L)>2k  =>  some induced level-k sharp witness is unlimited`.

   Equivalently, prove that absence of all such witnesses lets the local bounded decompositions assemble into an expression of height at most `2k`.
3. Prove a direct `n^{O(k)}` evaluator for those induced witnesses without materializing the exponential subset cost automaton or stabilisation monoid.

Soundness of an unlimited sharp witness already exists in stabilisation theory. What is missing is completeness under the factor-two promise and the polynomial evaluator. This route targets the exact numerical gap and an existing practical construction; unlike the discarded graph and slicing surrogates, it has not been refuted by the explicit counterexamples above.

## Adversarial audit

- The seven-state dictionary-star example was generated by a trie NFA, determinized and minimized, then checked independently by direct word-break membership through length 18. Reachability and all Myhill--Nerode distinctions were independently generated.
- Exact recursive cycle-rank code reproduces the ranks of the minimal DFA, full universal automaton, tagged reversal construction, and canonical image.
- The reset/reversal family was proved symbolically and instantiated for `m=1,...,8`.
- The final arbitrary-height state-fiber construction was rechecked at the language level: the local regular expressions enforce exactly edge composability, the fresh markers make the relevant residual unique, and the right quotient by `d` proves equality of heights.
- All exploration scripts compile. A long higher-cardinality cycle-rank computation was interrupted and no statement relies on it.
- The timestamp sequence in `WORKLOG.md` is monotone. The terminal audit occurred after 7200 seconds.

No candidate proof remained after this audit, so no proof file was created. The report intentionally separates disproved claims, verified lemmas, computational evidence, and unresolved possibilities.
