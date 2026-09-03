# A polylogarithmic sufficient order for pigeonhole-optimal Davenport--Schinzel sequences

## Result

Write

\[
N_n=\binom n2.
\]

We prove the following.

**Theorem.** There is an absolute constant `C` such that, for every integer-valued `s=s(n)` satisfying

\[
s\ge C\frac{(\log n)^3}{(\log\log n)^2}
\]

for all sufficiently large `n`, one has

\[
\lambda_s(n)\sim N_n s.
\]

In particular, the question singled out in the problem has an affirmative answer. Sections 1--5 first prove the slightly weaker but simpler condition `s>=C(log n)^3`; Section 6 gives the thinning refinement that saves the factor `(log log n)^2`.

The proof is self-contained apart from elementary probability inequalities.

## 1. Pair projections and inflation

For a word `U` with no immediate repetition and distinct symbols `a,b`, let `c_ab(U)` be the number of changes in the projection of `U` onto `{a,b}`. Thus the longest alternating subsequence on `a,b` has length `c_ab(U)+1`, provided both symbols occur. In particular, `U` is an order-`s` DS sequence if

\[
c_{ab}(U)\le s\qquad(a\ne b).
\]

Every transition between consecutive terms of `U` changes the corresponding two-symbol projection. Therefore

\[
|U|-1\le \sum_{a<b}c_{ab}(U)\le N_n s. \tag{1}
\]

This gives the upper bound `lambda_s(n)<=N_n s+1`.

Call `{a,b}` *supported* by `U` if `a,b` occur consecutively somewhere in `U`.

**Inflation lemma.** Suppose `c_ab(U)<=s` for all pairs. There is an order-`s` DS sequence on the same alphabet whose length exceeds that of `U` by at least

\[
\sum_{\{a,b\}\text{ supported}}(s-c_{ab}(U)-1). \tag{I}
\]

In particular, if `c_ab(U)<=h<s` for every pair and `P` pairs are supported, the increase is at least `P(s-h-1)`.

**Proof.** For every supported pair `{a,b}`, choose one transition between `a` and `b`. Replace that transition by a longer alternating walk on `a,b` with the same endpoints. Its number of transitions must be odd, so we may add any even number of transitions. Add the largest even integer not exceeding `s-c_ab(U)`, which is at least `s-c_ab(U)-1`. Under the additional uniform bound `c_ab(U)<=h`, this is at least `s-h-1`.

This operation adds that number to `c_ab`. It changes no other pair count: for a third symbol `x`, deleting `b` from the inserted `a,b`-walk leaves only repetitions of `a` at the location of the old `a`, and symmetrically after deleting `a`. The same observation shows that all chosen transitions can be inflated simultaneously, even when two chosen transitions share an endpoint. No immediate repetition is introduced. The resulting pair counts are at most `s`, and the claimed length bound follows after discarding the original positive length of `U`. `square`

It is consequently enough to construct a word of order `o(s)` that supports `(1-o(1))N_n` pairs.

There is also a converse structural statement, which identifies exactly what remains in the threshold question.

**Skeleton lemma.** Suppose `U` is an order-`s` word satisfying

\[
|U|-1=(1-o(1))N_ns.
\]

Then `U` has a subsequence `V` such that

\[
|\{\text{pairs supported by }V\}|=(1-o(1))N_n,
\qquad
\max_{a<b}c_{ab}(V)\le s,
\qquad
\frac1{N_n}\sum_{a<b}c_{ab}(V)=o(s). \tag{S}
\]

**Proof.** Let `e_ab` count actual consecutive transitions of type `{a,b}`, and put

\[
D=\sum_{a<b}(c_{ab}-e_{ab}).
\]

Since `sum e_ab=|U|-1` and `sum c_ab<=N_ns`, we have `D=o(N_ns)`. Also the number of unsupported pairs is at most `(N_ns-sum e_ab)/s=o(N_n)`.

Partition the transition path of `U` into maximal runs having one fixed unordered edge label. At a boundary between two runs the word has a factor `a b c` with `a!=c`. The change from `a` to `c` in the `{a,c}` projection is not an actual `{a,c}` transition, so it is counted by `D`. Different run boundaries give different such projection changes. Hence the number `R` of edge-runs is at most `D+1`.

Contract each edge-run to the shortest alternating path on the same two symbols with the same endpoints: it has one transition when the endpoints differ and two when they agree. This is a subsequence, preserves every supported edge type, and has at most `2R` transitions. It also preserves `D`: contracting an `{a,b}`-run decreases `c_ab` and `e_ab` by the same amount, while for a pair involving a third symbol it merely deletes repetitions from one run of that projection. Therefore

\[
\sum_{a<b}c_{ab}(V)
=\sum_{a<b}e_{ab}(V)+D
\le2R+D\le3D+2=o(N_ns).
\]

The maximum pair count cannot increase under passage to a subsequence. This proves (S). `square`

Together, the skeleton lemma and pair-specific inflation say that asymptotic pigeonhole optimality is equivalent to the existence of an almost-complete-support scaffold of maximum pair count at most `s` and average pair count `o(s)`.

The scaffold characterization gives a nontrivial universal necessary condition.

**Working-set lemma.** If a word on `n` symbols supports `(1-o(1))N_n` pairs, then

\[
\sum_{a<b}c_{ab}=\Omega(n^2\log n). \tag{W}
\]

**Proof.** Process the word from left to right while maintaining the symbols in decreasing order of recency. When `x` is read, let `r` be its zero-based rank just before the access; for its first access, let `r` be the number of symbols seen previously. Exactly those `r` more-recent symbols have appeared since the preceding `x`, so this access creates exactly `r` pair-projection changes. Consequently

\[
\sum_{a<b}c_{ab}=\sum_i r_i. \tag{W1}
\]

Fix `k` and let `M_k` be the number of accesses with `r_i>=k`. An access with `r_i<k` merely permutes the set of the `k` most recent symbols. An access with `r_i>=k` changes that set by at most one symbol and therefore introduces at most `k-1` new unordered pairs that have ever been simultaneously present in it. Starting from the empty cache, the total number of pairs ever co-resident in the top-`k` set is at most `k^2+kM_k` (with deliberately loose constants).

At the first occurrence of every supported transition type, either the new access has rank at least `k`, accounting for at most `M_k` types, or its two endpoints are co-resident in the top-`k` set. If `P` is the number of supported pair types, it follows that

\[
P\le k^2+(k+1)M_k. \tag{W2}
\]

When `P=(1-o(1))N_n`, (W2) gives `M_k=Omega(n^2/k)` uniformly for every dyadic `k<=n/4`. Finally, for every nonnegative integer `r`,

\[
r\ge\frac12\sum_{\substack{k\le r\\k\text{ a power of }2}}k.
\]

Summing this inequality over accesses and then using the bounds for `M_k` at the `Theta(log n)` dyadic scales proves (W). `square`

If the original asymptotic equivalence holds, the skeleton lemma gives a scaffold with average pair count `o(s)`, whereas (W) makes that average `Omega(log n)`. Hence necessarily

\[
\frac{s}{\log n}\longrightarrow\infty. \tag{N}
\]

## 2. A random recursive word

For `d>=1`, let the canonical level-`d` alphabet be

\[
\mathcal A_d=\mathbb F_2^d.
\]

Regard `a=(a_0,...,a_{d-1})` as the polynomial

\[
f_a(x)=\sum_{i=0}^{d-1}a_i x^i
\]

evaluated only at `x=0,1`.

At level one take

\[
W_1=1,2,1,2,1. \tag{2}
\]

For `d>=2`, form four row supports

\[
C_{x,v}=\{a\in\mathcal A_d:f_a(x)=v\},
\qquad (x,v)\in\mathbb F_2^2. \tag{3}
\]

Each support has size `2^(d-1)`, and every symbol belongs to exactly two supports. On each `C_(x,v)`, put an independent random copy of `W_(d-1)`: use a uniformly random bijection from `A_(d-1)` to `C_(x,v)`, and use fresh independent randomness in its recursive construction. Concatenate the four copies in any fixed order and suppress immediate repetitions at their boundaries. This defines the random word `W_d`.

If `L_d` is its length, then deterministically

\[
L_1=5,\qquad L_d\ge4L_{d-1}-3,
\]

and hence

\[
L_d\ge4^d+1. \tag{4}
\]

Suppressing a run of equal symbols cannot increase a two-letter alternation count. It also preserves every distinct adjacent pair type: replacing `...a x x b...` by `...a x b...` preserves the types `{a,x}` and `{x,b}`.

## 3. The recursion tree of one pair

Take a uniformly random distinct pair in `A_d`. Its difference is uniform on `F_2^d\setminus{0}`. The pair occurs together in one child block for each `x in F_2` at which its difference polynomial vanishes. Let `X_d` be the number of such child blocks.

For `d>=2`, put `A=2^(d-2)`. The linear map that sends a coefficient vector to its two values at `0,1` has four fibers of size `A`; only the zero vector is excluded, and it lies in the `(0,0)` fiber. Consequently

\[
\begin{aligned}
\Pr(X_d=2)&=\frac{A-1}{4A-1},\\
\Pr(X_d=1)&=\frac{2A}{4A-1},\\
\Pr(X_d=0)&=\frac{A}{4A-1}. \tag{5}
\end{aligned}
\]

For every `z>=1`, direct calculation gives

\[
\mathbb E z^{X_d}
\le \left(\frac{1+z}{2}\right)^2. \tag{6}
\]

Indeed, after putting the two sides over a common denominator, the sign is the sign of

\[
1+2z-3z^2\le0.
\]

Thus the pair's recursive common-block tree is dominated, for exponential-moment purposes, by a critical Galton--Watson tree with offspring distribution `Bin(2,1/2)`. Independence holds below the root because every child copy uses a fresh independent uniform bijection.

### Survival probability

The mean offspring number in (5) is

\[
\mu_d=1-\frac1{2^d-1}. \tag{7}
\]

Let `Z` be the population at the base level, starting with one uniformly random root pair at level `t`. Its expectation is

\[
\mathbb E Z=\prod_{d=2}^t\mu_d\ge c_0>0, \tag{8}
\]

where `c_0` is an absolute constant, because `sum_(d>=2)(1-mu_d)<infinity`.

Since `0<=X_d<=2`, conditioning on one generation gives

\[
\mathbb E Z_{j+1}^2
\le \mathbb E Z_j^2+4\mathbb E Z_j.
\]

Also `E Z_j<=1`, so `E Z^2<=1+4t`. Paley--Zygmund now gives an absolute `beta>0` such that

\[
\Pr(Z>0)\ge\frac{\beta}{t}. \tag{9}
\]

If `Z>0`, the pair reaches a copy of (2), where the two distinct symbols occur adjacently. The original pair is therefore supported by `W_t`.

### Exponential moment of the alternation length

Let `T` be the total number of nodes in the pair's common-block recursion tree. At an internal node with `r` common child blocks, each endpoint occurs alone in `2-r` further blocks. Hence the number of runs in the pair projection is at most the sum of the child run counts plus

\[
2(2-r)\le4.
\]

At a leaf the run count is at most five by (2). Therefore, if `A_t` denotes the alternating-subsequence length of a uniformly random pair in `W_t`,

\[
A_t\le5T. \tag{10}
\]

We need the following elementary bound for the dominating critical binary tree. Fix its maximum depth at `t`, put `theta=1/(100t^2)`, and let `F_j` be the moment generating function of total progeny through depth `j`. Then

\[
F_0=e^\theta,
\qquad
F_j=e^\theta\left(\frac{1+F_{j-1}}2\right)^2. \tag{11}
\]

Writing `y_j=F_j-1`, the inequalities `e^theta<=1+2theta` and

\[
y_j\le y_{j-1}+\frac{y_{j-1}^2}{4}
 +2\theta\left(1+y_{j-1}+\frac{y_{j-1}^2}{4}\right)
\]

give, by induction for `0<=j<=t`,

\[
y_j\le\frac{j+1}{2t^2}. \tag{12}
\]

(The increment allowed on the right is `1/(2t^2)`; under the inductive bound the actual increment is less than `1/(8t^2)` for all sufficiently large `t`. Finitely many smaller `t` can be absorbed by changing the absolute constant 100.)

Combining (6), (10), and (12),

\[
\mathbb E\exp\left(\frac{A_t}{500t^2}\right)
\le1+\frac1t. \tag{13}
\]

## 4. Cover almost every pair while keeping small order

Now let `n` be arbitrary, put

\[
t=\lceil\log_2 n\rceil,
\qquad M=2^t<2n,
\]

and construct independent copies of `W_t` on `M` symbols. In each copy choose a uniformly random injection of `[n]` into `A_t`, restrict the word to the image, suppress immediate repetitions, and relabel the image back to `[n]`.

For every fixed pair in `[n]`, its image is a uniform distinct pair in `A_t`. Restriction neither increases its alternation count nor destroys a supported transition whose two endpoints were retained.

Set

\[
r=\lceil t^{3/2}\rceil. \tag{14}
\]

Concatenate `r` independently constructed restricted copies. By (9), the expected fraction of pairs unsupported in all copies is at most

\[
\left(1-\frac\beta t\right)^r
\le \exp(-\beta\sqrt t+o(1))=o(1). \tag{15}
\]

Markov's inequality shows that the unsupported fraction is `o(1)` with probability tending to one.

For a fixed pair, let `A_1,...,A_r` be its within-copy alternating lengths. The number of changes in the concatenation is no more than `sum A_i`; merging equal symbols at boundaries can only lower it. By (13), for every `H>0`,

\[
\Pr\left(\sum_{i=1}^r A_i>H\right)
\le
\exp\left(-\frac{H}{500t^2}+\frac rt\right). \tag{16}
\]

Take

\[
H=500t^2(\sqrt t+3t). \tag{17}
\]

Since `r/t<=sqrt(t)+o(1)`, (16) is at most `exp(-3t+o(1))`. There are fewer than `n^2<=4^t` pairs. A union bound therefore shows that, with probability tending to one, every pair has at most `H` changes. In particular, for an absolute constant `C_0`,

\[
\max_{a<b}c_{ab}\le C_0t^3. \tag{18}
\]

We also need the average, rather than merely the maximum, of these pair counts. Every generation of the dominated critical tree has expected population at most one, so `E T<=t`; by (10), `E A_t<=5t`. If

\[
\overline c=\frac1{N_n}\sum_{a<b}c_{ab}
\]

is the average pair-change count in the concatenation, then

\[
\mathbb E\overline c\le5rt=O(t^{5/2}).
\]

Markov's inequality therefore gives

\[
\Pr(\overline c>t^{11/4})=O(t^{-1/4})=o(1). \tag{19}
\]

The coverage event from (15), the maximum-order event from (18), and the average-order event from (19) consequently hold simultaneously for some deterministic outcome. We have proved the existence of a word `V` on `[n]` such that

\[
\max_{a<b}c_{ab}(V)\le C_0t^3,
\qquad
\overline c(V)\le t^{11/4}=o(t^3),
\qquad
|\{\text{pairs supported by }V\}|=(1-o(1))N_n. \tag{20}
\]

## 5. Finish

Take `C` large enough that `s>=C(log n)^3` implies `s>=C_0t^3`; changing `C` only accounts for the fixed base of the logarithm. For every supported pair, the inflation argument adds at least `s-c_ab(V)-1` terms. By (20), the resulting order-`s` sequence has length at least

\[
\begin{aligned}
\sum_{\{a,b\}\text{ supported}}(s-c_{ab}(V)-1)
&\ge (1-o(1))N_n(s-1)-N_n\overline c(V)\\
&=(1-o(1))N_n s, \tag{21}
\end{aligned}
\]

because `s=Omega(t^3)` while `overline c(V)=o(t^3)`.

Together with (1), this proves

\[
\lambda_s(n)\sim\binom n2s.
\]

`square`

## 6. A thinning refinement

We now improve the sufficient scale by making the recursion slightly subcritical. This section uses the same inflation argument, but replaces `W_d` by a thinned version.

Fix `t`, choose `p=1-epsilon` in `(0,1)`, and modify the construction of Section 2 as follows. Independently for every recursive invocation and every one of its four row blocks, retain that block with probability `p` and omit it otherwise. A retained block contains a fresh independent, randomly relabeled thinned word from the next level. The base word (2) is unchanged. Empty words and empty concatenations are allowed at this intermediate stage.

For a uniform pair at a level, let `X_d` be its number of common blocks before thinning, as in (5), and let `Y_d` be its number of retained common blocks. Conditional on `X_d`,

\[
Y_d\sim\operatorname{Bin}(X_d,p).
\]

Putting `w=1-p+pz` in (6) shows that, for `z>=1`,

\[
\mathbb E z^{Y_d}
\le\left(1-\frac p2+\frac p2z\right)^2. \tag{22}
\]

Thus the thinned pair tree is dominated in exponential moments by a Galton--Watson tree with offspring `Bin(2,p/2)`, whose mean is `p=1-epsilon`.

### 6.1 Survival

The actual mean offspring at dimension `d` is `p mu_d`. If `Z` is the base-level population, (8) becomes

\[
\mathbb E Z=p^{t-1}\prod_{d=2}^t\mu_d\ge c_0p^t. \tag{23}
\]

For the second moment, the conditional identity for a sum of independent offspring variables, the bound `Y_d<=2`, and `E Z_j<=p^j` give

\[
\mathbb E Z_{j+1}^2
\le p^2\mathbb E Z_j^2+4\mathbb E Z_j
\le p^2\mathbb E Z_j^2+4p^j.
\]

Since `E Z_j<=p^j`, iteration yields

\[
\mathbb E Z^2\le C_1\frac{p^t}{1-p}
=C_1\frac{p^t}{\varepsilon}. \tag{24}
\]

Paley--Zygmund applied to (23)--(24) gives

\[
\Pr(Z>0)\ge c_1\varepsilon p^t. \tag{25}
\]

As before, survival implies adjacency support.

### 6.2 Subcritical exponential moment

Let `T` be total progeny in the dominating `Bin(2,p/2)` tree, of any finite depth. Its MGF obeys

\[
F_0=e^\theta,
\qquad
F_j=e^\theta\left(1-\frac p2+\frac p2F_{j-1}\right)^2. \tag{26}
\]

There are absolute constants `c_2,C_2>0` such that, for `theta=c_2 epsilon^2`,

\[
F_j\le1+C_2\varepsilon\qquad\text{for every }j. \tag{27}
\]

Here is an elementary verification. Take `c_2=1/100` and suppose `epsilon<=1/2`. With `y=F_(j-1)-1`, the inequalities `e^theta<=1+2theta` and `p<=1` show that the right side of (26), minus one, is at most

\[
py+\frac{p^2y^2}{4}
+2\theta\left(1+py+\frac{p^2y^2}{4}\right).
\]

The map is increasing in `y`. At the endpoint `y=2epsilon`, its value is at most

\[
2\varepsilon-2\varepsilon^2+\varepsilon^2
+5c_2\varepsilon^2
<2\varepsilon.
\]

Also `F_0-1=e^theta-1<=2theta<=2epsilon`. Thus `[0,2epsilon]` is invariant, proving (27) with `C_2=2`. The finitely many values before `epsilon<=1/2` are irrelevant to the asymptotic statement.

The run-count argument (10) is unchanged by thinning, so after altering the absolute constants,

\[
\mathbb E\exp(c_3\varepsilon^2 A_t)
\le1+C_3\varepsilon. \tag{28}
\]

Also every generation has expected population at most `p^j`, whence

\[
\mathbb E A_t\le5\mathbb E T\le\frac5\varepsilon. \tag{29}
\]

### 6.3 Choice of parameters

Continue to put `t=ceil(log_2 n)` and use independent uniform injections into `A_t`. Let

\[
\ell=\log t,
\qquad
\varepsilon=\frac{\ell-\log\ell}{t},
\qquad p=1-\varepsilon. \tag{30}
\]

Then `epsilon->0`, `epsilon^2t=o(1)`, and

\[
p^t=\exp(-\varepsilon t+o(1))
=(1+o(1))\frac\ell t. \tag{31}
\]

By (25), a fixed pair is supported in one thinned copy with probability at least

\[
\rho\ge c_4\frac{\ell^2}{t^2}. \tag{32}
\]

Let `G=log ell` and take

\[
r=\left\lceil C_4G\frac{t^2}{\ell^2}\right\rceil, \tag{33}
\]

where `C_4` is large enough in terms of `c_4`. The expected unsupported fraction is at most `exp(-Omega(G))=o(1)`, so Markov again gives support density `1-o(1)` with high probability.

For a fixed pair, (28) and Chernoff give

\[
\Pr\left(\sum_{i=1}^rA_i>H\right)
\le\exp\left(-c_3\varepsilon^2H+C_3r\varepsilon\right). \tag{34}
\]

Here

\[
r\varepsilon=O\left(\frac{Gt}{\ell}\right)=o(t),
\qquad
\varepsilon^2=(1+o(1))\frac{\ell^2}{t^2}. \tag{35}
\]

Choosing

\[
H=C_5\frac{t^3}{\ell^2} \tag{36}
\]

with a sufficiently large absolute `C_5`, the right side of (34) is `exp(-3t+o(t))`. The union bound over at most `4^t` pairs shows that every pair simultaneously has at most `H` changes, with high probability.

Finally, (29) gives

\[
\mathbb E\overline c
\le\frac{5r}{\varepsilon}
=O\left(\frac{G t^3}{\ell^3}\right)
=o\left(\frac{t^3}{\ell^2}\right). \tag{37}
\]

Markov, with any threshold between the last two scales, supplies a simultaneous deterministic outcome whose average pair count is `o(t^3/ell^2)`, whose maximum pair count is at most (36), and whose support density is `1-o(1)`.

If

\[
s\ge C_5\frac{t^3}{\ell^2},
\]

the pair-specific inflation sum (21) therefore gives `(1-o(1))N_n s` terms. Since `t=Theta(log n)` and `ell=Theta(log log n)`, increasing the absolute constant handles the fixed logarithm bases and proves the theorem stated at the beginning.

## Scope of the result

The theorem rigorously improves the `s/sqrt(n)->infinity` sufficient condition in the supplied PDF to

\[
s\ge C\frac{(\log n)^3}{(\log\log n)^2},
\]

and decisively answers its highlighted `s=o(sqrt(n))` question.

This argument does **not** prove that the displayed sufficient scale is necessary. The Working-Set Lemma supplies the lower side of the window below, but does not close it.

The proved universal window is

\[
\frac{s}{\log n}\to\infty\quad\text{(necessary)},
\qquad
s\ge C\frac{(\log n)^3}{(\log\log n)^2}
\quad\text{(sufficient)}.
\]
