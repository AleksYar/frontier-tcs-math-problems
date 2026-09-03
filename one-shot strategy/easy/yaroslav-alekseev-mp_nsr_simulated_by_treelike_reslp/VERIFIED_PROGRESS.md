# Verified progress toward the MP-NSR versus treelike Res(LP) problem

This note records the strongest intermediate result established during the proof
search. It is not a solution of the stated problem: the construction below uses
the integer-negation axiom of Res(CP), and the last section isolates why removing
that axiom without losing treelikeness remains unresolved.

## 1. From a static certificate to a descent graph

Write the final MP-NSR combination as

\[
 F=\bigoplus_j t_j\odot f_j\leq
 G=\bigoplus_j t_j\odot g_j.
\]

For a raw dual monomial \(m\), let \(b_m\) be its coefficient in \(G\).
Because the combination is a refutation, every monomial occurring in \(F\)
also occurs in \(G\), and its coefficient in \(F\) is strictly greater than
\(b_m\). Choose a finite constant occurrence of \(G\) as a root.

For every RHS support \(u\) reached from the root, choose an occurrence
\(t_j\odot g_{j,r}\) attaining \(b_u\). For every term
\(t_j\odot f_{j,i}\) on the corresponding left side, let \(v\) be its raw
monomial support and draw an edge \(e:u\to v\). The support \(v\) occurs on
the right because of coefficientwise strict domination. If \(a_e\) is the
coefficient of this left occurrence, then

\[
 a_e>b_v. \tag{1}
\]

Let \(M_u(x)\) be the ordinary affine value of support \(u\) after replacing
each dual variable \(\bar x\) by \(1-x\). Let

\[
 k_e=(\text{coefficient of }g_{j,r})-
     (\text{coefficient of }f_{j,i}).
\]

The tropical multiplier cancels, so the Res(LP) disjunct belonging to this
edge is

\[
 f_e(x):=k_e+M_u(x)-M_v(x)\geq0. \tag{2}
\]

For the stipulated input axioms, every \(k_e\) is an integer of polynomial
magnitude. There are at most two outgoing edges: only
\(x\oplus\bar x\leq0\) gives two left terms.

If the chosen RHS occurrence at \(u\) has coefficient \(b_u\), then its
left occurrence has coefficient \(b_u-k_e\). Hence (1) gives

\[
 b_v-b_u<-k_e. \tag{3}
\]

Summing (3) around a directed cycle and using integrality of the \(k_e\)'s
shows

\[
 \sum_{e\text{ on the cycle}} k_e\leq-1. \tag{4}
\]

## 2. Polynomial normalization

Let \(N\) be the number of reachable vertices and put \(q=N+1\). Consider
the non-strict difference constraints

\[
 p_v-p_u\leq-k_e-\frac1q\qquad(e:u\to v). \tag{5}
\]

They are feasible. Indeed, every simple directed cycle has length at most
\(N\), and by (4) the sum of its right sides is at least
\(1-N/(N+1)>0\). The usual shortest-path solution of (5) has denominator
\(q\) and polynomial magnitude because the edge weights and every simple
path have polynomial magnitude.

Shift this solution so that the root value is zero and define

\[
 Q_v=q(p_v-p_r),\qquad H_v(x)=Q_v+qM_v(x).
\]

Then \(Q_v\in\mathbb Z\), all \(Q_v\)'s have polynomial numerical magnitude,
and \(H_r=0\). For every edge put

\[
 d_e=Q_u-Q_v-qk_e.
\]

Constraint (5) says \(d_e\geq1\), and (2) gives the exact identity

\[
 H_u-H_v-d_e=qf_e. \tag{6}
\]

The coefficients of every \(H_v\) also have polynomial numerical magnitude.
To see this for the monomial exponents, take a simple path from the constant
root to \(v\). It has at most \(N\) edges, and each raw-support difference is
the difference of two terms of one input axiom, whose degree is bounded by
the certificate size. Thus every reachable support is a sum of at most \(N\)
small increments.

For every vertex, the translation of its chosen input occurrence, scaled by
\(q\), is therefore the line

\[
 C_u:=\bigvee_{e:u\to v}(H_u-H_v-d_e\geq0). \tag{7}
\]

It has width at most two. Scaling can be performed treelikely, one disjunct
at a time, using fresh copies of the derivable unit \(0\geq0\).

## 3. A polynomial treelike Res(CP) refutation

For an integer \(L\), define

\[
 D_L:=\bigvee_v(L-H_v\geq0). \tag{8}
\]

Since \(H_r=0\), the derivable unit \(1\geq0\) weakens to \(D_1\).

Fix a vertex \(u\). The Res(CP) integer-negation axiom applied to
\(H_u-L\) is

\[
 (H_u-L-1\geq0)\ \vee\ (L-H_u\geq0). \tag{9}
\]

Using a fresh copy of (9) for each edge alternative in (7), add its second
disjunct to that edge. By (6) the result is

\[
 L-H_v-d_e=(L-1-H_v)-(d_e-1).
\]

Adding the nonnegative constant \(d_e-1\) and processing the at most two
edge alternatives sequentially yields

\[
 (H_u-L-1\geq0)\ \vee\
 \bigvee_{e:u\to v}(L-1-H_v\geq0). \tag{10}
\]

Resolve (10) against the \(L-H_u\) disjunct in the current copy of \(D_L\).
The selected inequalities add to \(-1\geq0\), so that disjunct disappears;
the successor disjuncts remain. Process every current-level vertex once.
The current line is always used once, and every instance of (7)--(10) is
fresh. At the end, weaken by missing successor disjuncts to obtain
\(D_{L-1}\).

Every \(H_v\) has the unit lower bound

\[
 H_v-Q_v=qM_v\geq0, \tag{11}
\]

obtained by adding the standard bounds for all literal occurrences in the
raw monomial. Put \(B=\min_v Q_v\). Iterating the preceding construction
from \(D_1\) down to \(D_{B-1}\) takes polynomially many levels. Finally,
add (11) to each disjunct of \(D_{B-1}\); the result is the false constant
\(B-1-Q_v\leq-1\). Drop all but one such false constant, and add the
appropriate derivable nonnegative integer constant to the last one to obtain
exactly \(-1\geq0\). This is a polynomial-size treelike Res(CP) refutation.

## 4. Exact unresolved step for Res(LP)

The only non-Res(LP) lines above are (9). Each is an integer split of a
polynomial-unary weighted sum of literals. Hirsch--Kojevnikov give a
polynomial daglike Res(LP) derivation of such unary splits, but their
variable induction reuses threshold lines and explicitly does not preserve
treelikeness. At a middle threshold, its tree expansion can branch into both
neighboring partial-sum thresholds.

The split is cheap at a bottom threshold, e.g.

\[
 (S-1\geq0)\vee(-S\geq0)
\]

for a nonnegative literal sum \(S\). This suffices for a polynomial treelike
Res(LP) simulation of dag Resolution by querying learned clauses along one
spine. In (9), however, \(L-Q_u\) can lie strictly inside the Boolean range
of \(qM_u\), and both sides can remain viable. Neither the difference-
constraint normalization nor coefficient shifting forces these thresholds
to the boundary. Eliminating precisely these middle-threshold splits, or
constructing an MP-NSR family for which they force a lower bound, is the
remaining obstruction.

## 5. A complete Res(LP) proof under a bottom-anchor condition

There is a useful condition under which the remaining cuts can be removed.
Suppose integers `R_u` satisfy

\[
 R_u\leq \min_{x\in\{0,1\}^n} H_u(x),\qquad R_r=H_r=0,
 \tag{12}
\]

and every edge satisfies

\[
 R_u-d_e\leq R_v. \tag{13}
\]

For a nonnegative unary weighted literal sum `S`, the bottom split

\[
 (S-1\geq0)\vee(-S\geq0) \tag{14}
\]

has a linear-size treelike Res(LP) derivation. To check this directly, write
`S=Z+a ell`. From the already derived split for `Z`, add the unit bound
`a ell>=0` to its first alternative, obtaining

\[
 (Z+a\ell-1\geq0)\vee(-Z\geq0).
\]

From the Boolean split for `ell`, scaling and adding the unit bound `Z>=0`
gives

\[
 (Z+a\ell-1\geq0)\vee(-a\ell\geq0).
\]

Resolve the two negative alternatives. Their sum is `-Z-a ell`, while the
common positive alternative contracts. This uses the recursively derived
line only once.

After canonicalizing paired literals, `H_u-R_u` is such a nonnegative
weighted literal sum. Start with

\[
 \bigvee_u(R_u-H_u\geq0),
\]

which is a weakening of the root equality. The split (14), combined with
`C_u`, replaces `R_u-H_u` by successor alternatives `R_u-d_e-H_v`. Under
(13), each is either the bottom alternative `R_v-H_v`, or lies strictly
below the lower bound for `H_v` and can be deleted. The equality edges
`R_u-d_e=R_v` are acyclic because every `d_e>=1`. Processing vertices in
topological order eliminates the entire line in polynomial treelike
Res(LP) size.

The canonical choice `R_u=min H_u` does not satisfy (13) edge by edge. For
the clause `x OR y`, the input
inequality is `x+y-1>=0`. Multiply it by `xbar+ybar`. The RHS monomial
`x+xbar+y+ybar` has Boolean minimum 2, whereas the LHS successor
`xbar+ybar` has minimum 0, and the edge gap is only 1. The propagated
successor bound is therefore `xbar+ybar<=1`, a genuine middle threshold.
This explicit example shows why choosing the evident minimum anchors does
not prove the full result. Whether some lower anchors satisfying (12)--(13)
always exist requires a separate global feasibility argument.

## 6. Quasipolynomial treelike Res(LP) simulation

Although a polynomial derivation of a general middle split remains missing,
there is a quasipolynomial treelike derivation when the weighted range is
polynomial. Let

\[
 S=\sum_{i=1}^n a_i\ell_i,\qquad 0\leq S\leq W,
\]

where the literals use distinct variables and the nonnegative integer weights
sum to `W`. Write

\[
 I_t(S):=(S-t\geq0)\vee(t-1-S\geq0).
\]

Thresholds outside `[1,W]` follow from unit bounds. With one variable, every
split follows by scaling its Boolean split and adding nonnegative constants.

For the induction step, partition the variables evenly and put `S=A+B`, with
`0<=A<=W_A`. Fix `a` in `[0,W_A]`. Combining the high sides of `I_a(A)` and
`I_{t-a}(B)` gives

\[
 (S-t\geq0)\vee(a-1-A\geq0)\vee(t-a-1-B\geq0). \tag{15}
\]

Combining the low sides of `I_{a+1}(A)` and a fresh `I_{t-a}(B)` gives

\[
 (t-1-S\geq0)\vee(A-a-1\geq0)\vee(B-t+a\geq0). \tag{16}
\]

The last alternatives of (15) and (16) sum to `-1`. Resolving them and
weakening by the other target alternative yields

\[
 I_t(S)\vee(a-1-A\geq0)\vee(A-a-1\geq0). \tag{17}
\]

At `a=0` the lower outside alternative is false, and at `a=W_A` the upper
outside alternative is false. Resolve (17) successively for
`a=0,1,...,W_A`: the current upper alternative `A-a-1` and the next lower
alternative `a-A` sum to `-1`. The result is exactly `I_t(S)`.

Every half-sum split is supplied by a fresh subtree. If `T(n,W)` bounds one
such derivation, then

\[
 T(n,W)\leq C(W+1)T(\lceil n/2\rceil,W)+\operatorname{poly}(n,W),
\]

so

\[
 T(n,W)=\exp(O(\log n\,\log(W+1))). \tag{18}
\]

Canonicalizing opposite literals in each `M_v` turns every split (9) into a
split of this form, and Section 2 shows that both `n` and `W` are polynomial
in the MP-NSR certificate size. Replacing every Res(CP) split in Section 3
by a fresh derivation above proves the verified intermediate theorem:

> MP-NSR is quasipolynomially simulated by treelike Res(LP).

This does not prove the requested polynomial simulation: for polynomial
`W`, (18) can still be `exp(O(log^2 n))`. Removing the factor `W` at every
level of the balanced recursion is the precise quantitative obstruction.
