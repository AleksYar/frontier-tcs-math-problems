# Proof-search report: eventual ratio monotonicity for fixed polyominoes

## Outcome and search interval

The search began at Unix time `1787853262` (`2026-08-27T19:54:22+02:00`) and ended at Unix time `1787860519` (`2026-08-27T21:55:19+02:00`). This is 7,257 elapsed seconds; the active-goal timer recorded 7,250 seconds.

No complete proof was found. In particular, this report does **not** claim that the assertion is false or impossible. The assertion remains a published open conjecture: Bui states it explicitly as Conjecture 2, while Madras proves convergence of the ratios but not their monotonicity. The 2024/2026 Barequet--Ben-Shachar work extends exact enumeration to 70 terms without resolving the conjecture.

The target, for the number `A(n)` of fixed `n`-cell polyominoes, is

\[
A(n+1)^2<A(n)A(n+2),
\]

equivalently strict increase of `A(n+1)/A(n)` for all sufficiently large `n`.

The complete timestamped search record is in `WORKLOG.md`. All computational assertions below are evidence or finite verification only; none is used as an all-size proof.

## Verified finite evidence

- The exact published values `A(0),...,A(70)` satisfy the strict inequality at every center `1<=n<=68`.
- At the last available comparison,

  \[
  \frac{A(69)}{A(68)}\approx4.004298257436,
  \qquad
  \frac{A(70)}{A(69)}\approx4.005122972641.
  \]

  Their difference is approximately `0.0008247152052`, and multiplying by `68^2` gives approximately `3.81348`. Thus the observed sign lives at order `n^(-2)`.
- An independent generator reproduced `A(1),...,A(11)` as

  `1,2,6,19,63,216,760,2725,9910,36446,135268`.
- Exhaustive one-cell cover-graph calculations were carried through size 10. The scripts in `tmp/` reproduce the stated counts, identities, and counterexamples.

## Strongest proved reduction: a renewal record-ratio lemma

Set `A(0)=1` and define formal reciprocal coefficients `Q(n)` by

\[
A(n)=\sum_{i=1}^n Q(i)A(n-i).
\]

These coefficients have a genuine combinatorial interpretation. Define an oriented horizontal product as follows: put the second polyomino strictly above the first and align the leftmost cell in its bottom row immediately above the rightmost cell in the first polyomino's top row. There is exactly one vertical edge between the factors. Valid product cuts are linearly ordered by height, so cutting at all of them gives a unique factorization into cut-indecomposable factors. Consequently

\[
A(z)=\frac{1}{1-Q(z)},
\]

and every `Q(n)` is a positive integer. Exhaustive geometry recovers

`1,1,3,8,24,76,252,860,2997,10618,38125`

through size 11, agreeing with formal series inversion.

Here is the proved lemma. Let positive sequences `a_n,q_n` satisfy

\[
a_0=1,\qquad a_n=\sum_{i=1}^n q_i a_{n-i}.
\]

Put

\[
R_n=\frac{a_n}{a_{n-1}},\qquad
s_i=\frac{q_{i+1}}{q_i},\qquad
w_{n,i}=\frac{q_i a_{n-i}}{a_n}.
\]

Then `sum_i w_(n,i)=1` and

\[
R_{n+1}=q_1+\sum_{i=1}^n w_{n,i}s_i. \tag{1}
\]

Assume `R_1<...<R_n`. For `i<n`,

\[
\frac{w_{n,i}}{w_{n-1,i}}
=\frac{R_{n-i}}{R_n}<1.
\]

Let `delta_i=w_(n-1,i)-w_(n,i)>0`. Since the missing old mass is the new atom, `sum_(i<n) delta_i=w_(n,n)`. Subtracting (1) at consecutive indices gives the exact identity

\[
R_{n+1}-R_n
=\sum_{i=1}^{n-1}\delta_i(s_n-s_i). \tag{2}
\]

Therefore, if `s_n` is at least every preceding `s_i`, then `R_(n+1)>R_n` whenever at least one of those comparisons is strict.

For the polyomino coefficients,

\[
s_1=1,\quad s_2=3,\quad s_3=\frac83,\quad s_4=3,
\]

and the `s_n` are strictly increasing from `n=4` through every available value. The animal ratios are strictly increasing through the required base cases. Hence the following single statement would prove the original conjecture (indeed, for every index):

\[
Q(n)^2\le Q(n-1)Q(n+1)\qquad(n\ge4). \tag{3}
\]

Statement (3) is not proved. It is the sharpest exact remaining combinatorial obstruction found in the search.

Two useful facts about this reduction were also proved:

- adding a horizontal leaf in a new rightmost column preserves cut-indecomposability, giving an injection `Q(n)->Q(n+1)`;
- cut-indecomposables are not deletion-accessible. The indecomposable pentomino

  `{(0,2),(1,0),(1,1),(1,2),(2,0)}`

  has no removable cell whose deletion remains indecomposable. Thus a generating-tree induction for (3) fails.

## Other proved intermediate statements

For a polyomino `P`, let `b(P)` be its number of adjacent exterior cells and `d(P)` the number of cells whose deletion leaves a polyomino.

1. Double counting marked additions gives

   \[
   \sum_{|P|=n}b(P)=\sum_{|Q|=n+1}d(Q).
   \]

2. If a vertex is added to any connected graph, the number of non-articulation vertices cannot decrease. Indeed, an old non-articulation vertex can become an articulation only when it is the sole neighbor of the new vertex; then the new vertex replaces it. Hence `d(Q)>=d(P)` along every one-cell extension.
3. Marking an additional boundary site or removable cell gives

   \[
   \sum_{|P|=n}b(P)(b(P)-1)
   \le \sum_{|Q|=n+1}d(Q)b(Q),
   \]

   \[
   \sum_{|P|=n}b(P)d(P)
   \le \sum_{|Q|=n+1}d(Q)^2.
   \]

4. Distinct additions or deletions yield distinct translation classes except for the two straight bars. Consequently, for `n>=2`, the simple cover-edge count is exactly `sum b(P)-2=sum d(Q)-2`.

These facts do not compare the needed uniform level averages: the pointwise inequalities live under an edge-size-biased measure. This is the precise obstruction in the incidence approach.

A separate sufficient analytic statement was verified. If

\[
\frac{A(n)}{A(n-1)}
=\lambda\left(1-\frac1n+\frac{c}{n^2}+o(n^{-2})\right),
\]

then subtracting consecutive expansions gives

\[
\frac{A(n+1)}{A(n)}-\frac{A(n)}{A(n-1)}
=\frac{\lambda}{n^2}+o(n^{-2})>0.
\]

A Delta-domain logarithmic singular expansion for `A(z)` with coefficient error `o(lambda^n/n^2)` would provide this. No such expansion is known; even the predicted leading law `A(n)~C lambda^n/n` is unproved for square-lattice animals.

## Attempted approaches and why they stopped

### Direct injections and cover graphs

Canonical deletion has unbounded and nonmonotone fibers. The lexicographically greatest cell need not be removable: in the L-triomino `{(1,1),(0,1),(1,0)}`, removing `(1,1)` disconnects the other cells. A symmetric transfer between two rooted animals also fails already for triominoes. Normalized matching was verified by exact max flow through the level pair `9910 -> 36446`, but even an all-size normalized-matching theorem would only provide a uniform monotone coupling; it does not determine the relative growth of boundary and parent degrees.

### Renewal and concatenation

The usual lexicographic concatenation is not uniquely factorable. The `2 by 2` square is both monomino followed by an L-triomino and an L-triomino followed by a monomino; both L factors are indecomposable. Thus the actual count of indecomposable tetrominoes is 9, while formal renewal inversion gives 8. The oriented product above repairs uniqueness but leaves (3).

Freeness and eventual log-convexity of the generators alone are insufficient. An exact integer counterexample has

\[
q_1=10,\quad q_2=100,\quad q_n=1\ (n\ge3),
\]

with renewal generating function

\[
\frac{1-z}{1-11z-90z^2+99z^3}.
\]

Its negative subdominant pole produces permanent alternating ratio errors, although the generator tail is log-linear, the counts are integers, the free monoid is supermultiplicative, and the ratios converge. This falsifies any argument that simply ignores finitely many early defects.

### Pattern switching

Madras's size-changing pattern switch leads exactly to a variance term minus a falling-factorial correction. With `X=i/(j+1)` and `Y=i(i-1)/((j+1)(j+2))`,

\[
Y-X^2=-\frac{i(i+j+1)}{(j+1)^2(j+2)}.
\]

Both the variance and negative correction are of order `1/n`, and their leading terms cancel in the natural binomial regime. Existing pattern theorems and concentration estimates do not control the residual order-`n^(-2)` sign. Inside a fixed switch class the coefficients are binomial and log-concave, the opposite direction; the desired sign must arise from a finely controlled mixture of classes.

### Posets, antimatroids, and positive operators

Canonical representatives with their least cell at the origin form an infinite antimatroid, but modern inequalities count feasible growth words, not unweighted terminal sets. Connected sets lack symmetric exchange and their intersections can be disconnected. Higher Hankel determinants of `A(n)` are negative at several exact shifts, ruling out a global Stieltjes-moment or simple positive-operator representation. Differential-poset commutators also have no sign: a solid `k by k` square has `d=k^2` but `b=4k`.

### Refined generating functions and transfer matrices

Coefficientwise boundary-polynomial log-convexity fails (already at centers 2, 5, and 8), and hole-weighted log-convexity fails for large hole fugacity at centers 8 and 9. Fixed-width counts become log-concave in the tested range, so their mixture cannot be handled termwise. A uniform saddle-point/local-limit theorem over growing widths would again need second-order precision not presently available.

### Global asymptotics

Supermultiplicativity, ratio convergence, polynomial or quasi-polynomial corrections, and even the conjectured leading equivalent do not force a local sign. A concrete countermodel is obtained by choosing sparse `N_j=2^(J+j)`, setting `c_(N_j)=2/N_j^2` and zero elsewhere, and defining

\[
h_n=\sum_{k>n}(k-n)c_k,
\qquad
a_n=\frac{\lambda^n}{n}e^{-h_n}.
\]

Then `h_n` is positive, decreasing, convex, and tends to zero. Thus `a_n~lambda^n/n`, its ratios converge, and it is supermultiplicative after a harmless finite initial adjustment. Also `n a_n` is log-concave. Nevertheless, at every sparse `N_j`,

\[
\Delta^2\log a_n
=\log\!\left(\frac{n^2}{n^2-1}\right)-\frac{2}{n^2}<0,
\]

so its ratios decrease infinitely often. A small positive curvature baseline and flooring make the example integer-valued while preserving all eventual strict signs. Therefore a smooth error estimate, not merely `A(n)~C lambda^n/n`, is essential.

## Explicitly discarded claims

- “The lexicographically greatest cell is removable”: false by the L-triomino above.
- “Lexicographic concatenation has unique prime factorization”: false by the `2 by 2` square.
- “Every cut-indecomposable has an indecomposable parent”: false by the five-cell path-shaped example above.
- “A rooted symmetric one-cell exchange always exists”: false for

  `X={(0,0),(0,-1),(-1,-1)}` and `Y={(0,0),(0,1),(0,2)}`.
- “Boundary plus removability is monotone under addition”: false for the size-14 horseshoe recorded explicitly in `WORKLOG.md`; adding one cell changes `(b,d)` from `(20,14)` to `(19,14)`.
- “Eventual log-convexity of renewal generators implies eventual log-convexity of the renewal sequence”: false by the exact rational free-monoid example above.
- “The expected `C lambda^n/n` asymptotic would by itself settle the sign”: false by the sparse-curvature countermodel.

## Exact remaining obstruction and best next route

The exact unresolved issue is second-order regularity. Known results determine the exponential growth and convergence of the first ratio, but the desired difference is of order `n^(-2)` and can be reversed by perturbations invisible to every currently proved first-order estimate.

The most concrete next route is to study the oriented cut-indecomposable counts and prove the tail record property (3). Identity (2) would then finish the original problem immediately. A viable proof would need a genuinely global switching or local-limit theorem for indecomposable animals; local accessibility and monotone-degree approaches are explicitly false.

The most promising analytic route is a rigorous logarithmic singular expansion for the fixed-animal generating function with a smooth transferred remainder. This would settle the claim directly, but it would also resolve a major presently open asymptotic problem for two-dimensional lattice animals.

## Sources

- Problem source: `antoine-vinciguerra-polyominoe-monotonicity.pdf`.
- Neal Madras, [A pattern theorem for lattice clusters](https://arxiv.org/abs/math/9902161) (ratio convergence, not monotonicity).
- Vuong Bui, [An asymptotic lower bound on the number of polyominoes](https://arxiv.org/abs/2211.14909) (states ratio increase as Conjecture 2).
- Gill Barequet and Gil Ben-Shachar, [Counting Polyominoes, Revisited](https://epubs.siam.org/doi/10.1137/1.9781611977929.10) (enumeration through 70; later Algorithmica version DOI `10.1007/s00453-026-01392-6`).
- Iwan Jensen, [Enumerations of lattice animals and trees](https://arxiv.org/abs/cond-mat/0007239) (numerical evidence for a logarithmic singularity).
- [OEIS A001168](https://oeis.org/A001168), exact fixed-polyomino counts.
