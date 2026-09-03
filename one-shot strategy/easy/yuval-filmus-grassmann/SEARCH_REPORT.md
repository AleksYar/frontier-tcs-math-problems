# Ternary degree-one functions on the binary Grassmann scheme

## Status

The requested complete classification was not obtained. This report records the proved results, exact counterexamples, audited computations, discarded claims, and the remaining obstruction after the requested search interval. Nothing labelled “candidate” or “promising route” below is asserted as a theorem.

The active-search clock ran from Unix time 1787820747 (2026-08-27 10:52:27+02:00) through Unix time 1787828241 (2026-08-27 12:57:21+02:00), a total of 7,494 seconds. A final adversarial read-through found and repaired the missing hypothesis documented in `WORKLOG.md`; a second consistency pass found no further unsupported inference in the results stated as proved. It did not supply the missing global rigidity theorem.

The problem asks for all degree-one functions
\[
f:J_2(n,k)\longrightarrow\{0,1,2\},\qquad \min(k,n-k)\ge2,
\]
where
\[
f(L)=\sum_{x\in L\setminus\{0\}}c_x.
\]
Over \(\mathbb F_2\), nonzero vectors and projective points are the same, so this notation is unambiguous.

## 1. The suggested Boolean-pair answer is false at every rank

Let \(V=\mathbb F_2^n\), let \(a,b\in V^*\) be independent, and choose a nonzero \(z\in\mathbb F_2^2\). Put
\[
A(x)=(a(x),b(x)),\qquad C_z=A^{-1}(z),
\]
and define
\[
F_z(L)=2^{2-k}|L\cap C_z|. \tag{1}
\]

### Proposition 1

For every \(k\ge2\), \(F_z\) is degree one and takes only the values \(0,1,2\).

### Proof

It is degree one because
\[
F_z(L)=\sum_{x\ne0}2^{2-k}\mathbf1_{C_z}(x)[x\in L].
\]
Let \(R=A(L)\le\mathbb F_2^2\). If \(z\notin R\), then \(L\cap C_z\) is empty. If \(R=\langle z\rangle\), then \(A|_L\) has rank one and the fiber of \(z\) has size \(2^{k-1}\). If \(R=\mathbb F_2^2\), that fiber has size \(2^{k-2}\). These are all possibilities, so (1) takes the values \(0,2,1\), respectively. ∎

For \(z=(1,1)\), this can also be written
\[
F_z=1-y_a-y_b+y_{a+b},\qquad y_r(L)=\mathbf1[L\subseteq\ker r]. \tag{2}
\]
The other nonzero cosets give the analogous signed formulas. Orthogonal duality gives point-triangle versions such as
\[
1-x_p-x_q+x_{p+q}. \tag{3}
\]

These examples persist when both \(k\) and \(n-k\) are arbitrarily large. Thus increasing the constant \(t\) cannot make the cube-like list of sums of two Boolean degree-one functions complete.

There are also rigorously verified compatible additions. Let \(g\) be a supplied Boolean degree-one function. Since \(F_z+g\) can exceed two only where \(F_z=2\), it is ternary exactly when
\[
g(L)=0\quad\text{whenever }A(L)=\langle z\rangle. \tag{C}
\]
Within the supplied Boolean classification, and when \(k,n-k\ge2\), the complete list satisfying (C) is:

- \(g=0\);
- \(g=x_p\) and \(A(p)\notin\langle z\rangle\);
- \(g=y_r\), where \(r=\lambda\circ A\) and \(\lambda(z)=1\);
- \(g=1-y_r\), where \(r=\lambda\circ A\ne0\) and \(\lambda(z)=0\);
- \(g=x_p+y_r\), where the conditions in the \(x_p\) and \(y_r\) bullets hold and \(r(p)=1\);
- \(g=1-x_p-y_r\), where \(r=\lambda\circ A\), \(\lambda(z)=0\), and \(r(p)=1\).

Here is the converse argument. Write \(H=A^{-1}(\langle z\rangle)\) and \(K=\ker A\); the core-level-two spaces are exactly the \(k\)-spaces in \(H\) not contained in \(K\). Such a space contains \(p\) for some choice precisely when \(p\in H\), proving the \(x_p\) criterion and ruling out \(1-x_p\). The condition that no such space lie in \(\ker r\) is \(H\cap\ker r=K\), equivalently \(r=\lambda A\) with \(\lambda(z)=1\). The condition that all such spaces lie in \(\ker r\) is \(H\subseteq\ker r\), equivalently \(r=\lambda A\ne0\) with \(\lambda(z)=0\). Since the two events in the supplied union are disjoint, these facts give its condition. For the complemented union, if \(y_r\) is not identically one on the level-two family, one can choose a level-two space avoiding \(p\) on which \(y_r=0\); hence only the last listed case survives. This proves completeness within the supplied Boolean types and produces the examples \(F_z+g\) and their value complements.

In fact all compatible additions in this list except \(x_p\) collapse to Boolean pair sums. Let \(r,s\in\operatorname{row}(A)\) be the two functionals taking value one at \(z\), and put \(t=r+s\), the nonzero functional annihilating \(z\). Then
\[
F_z=1-y_r-y_s+y_t.
\]
Consequently
\[
F_z+y_r=(1-y_s)+y_t,\qquad
F_z+(1-y_t)=(1-y_r)+(1-y_s).
\]
If a compatible union also contains \(x_p\), its conditions imply that \(r(p),s(p)\) are different and \(t(p)=1\), so \(x_p+y_t\) is one supplied Boolean function; the displayed decomposition again has two Boolean summands. The complemented-union case is analogous, pairing \(x_p\) with whichever of \(y_r,y_s\) is disjoint from it.

Thus the only new compatible form is
\[
F_z+x_p\quad\text{with }A(p)\notin\langle z\rangle, \tag{E}
\]
along with its orthogonal dual and value complement. Form (E) is not a Boolean pair sum for \(n\ge5\). Indeed, if it were, move its one point delta and the at most two deltas from the putative pair sum to one side. The remaining difference between the four-character expansion (6) and at most three characters would have physical support at most three and Fourier support at most seven, contradicting the same uncertainty inequality used in Proposition 2; equality to zero is again excluded by Fourier uniqueness.

Two cores do not yield another primitive. More precisely, suppose \(n-k\ge2\), and let \(F_{A,z}\), \(F_{B,w}\) be two cores. Put
\[
S_{A,z}=A^{-1}(\langle z\rangle),\qquad
S_{B,w}=B^{-1}(\langle w\rangle).
\]
If \(B^{-1}(w)\cap S_{A,z}\ne\varnothing\), a point in this intersection can be extended to a \(k\)-space \(L\le S_{A,z}\) with \(A(L)=\langle z\rangle\); then \(F_{A,z}(L)=2\) and \(F_{B,w}(L)\ge1\). Thus ternarity of the sum forces both
\[
B^{-1}(w)\cap S_{A,z}=\varnothing,\qquad
A^{-1}(z)\cap S_{B,w}=\varnothing. \tag{D}
\]
Let \(U\) and \(W\) be the two-dimensional row spaces of \(A\) and \(B\). The first condition in (D) says that the nonzero functional in \(U\) annihilating \(z\) is constant one on \(B^{-1}(w)\); hence it lies in \(U\cap W\). The second produces a different element of \(U\cap W\) (their values on \(B^{-1}(w)\) are one and zero). Therefore \(U=W\). The two cores are then distinct nonzero cosets of the same codimension-two linear subspace. Their union is an affine hyperplane, and
\[
F_{A,z}+F_{B,w}=2(1-y_r)
\]
for the appropriate \(r\). Conversely this doubled Boolean function is ternary. Hence compatible sums of two cores collapse to the already-known Boolean-pair family.

A dual core cannot be added either once \(n-k\ge3\). A point-triangle core has the form
\[
G(L)=1-x_p(L)-x_q(L)+x_{p+q}(L)
\]
for the 2-space \(P=\langle p,q\rangle\), and \(G(L)=1\) whenever \(L\cap P=0\). The level-two spaces of \(F_{A,z}\) are the \(k\)-spaces \(L\) contained in the hyperplane \(S=A^{-1}(\langle z\rangle)\) but not in \(\ker A\). Since \(\dim S=n-1\), \(\dim(P\cap S)\le2\), and \(k\le n-3\), elementary complementation produces such an \(L\) with \(L\cap P=0\): take a complement of \(P\cap S\) in \(S\) which is not contained in \(\ker A\), and then a \(k\)-subspace of that complement not contained in \(\ker A\). For this \(L\), \(F_{A,z}(L)+G(L)=3\). Thus a sum of a dual affine core and a point-triangle core is never ternary in the high-rank regime.

Signed differences of two dual cores give nothing new either when \(k,n-k\ge3\). If
\(1+F_{A,z}-F_{B,w}\) is ternary, every level-two space of \(F_{A,z}\) must meet the affine fiber \(D=B^{-1}(w)\), since otherwise the two core values are \((2,0)\). Inside
\[
H=A^{-1}(\langle z\rangle),\qquad K=\ker A,
\]
the set \(D\cap H\), when nonempty, is an affine subspace of codimension one or two. The following elementary blocking observation applies: the only such affine subspace meeting every \(k\)-space of \(H\) not contained in \(K\) is \(H\setminus K\). For an affine hyperplane this follows by taking a \(k\)-space in its parallel hyperplane; for an affine codimension-two set, one takes a \(k\)-space in one of the other hyperplanes through its direction. The inequalities \(2\le k\le\dim H-2\) ensure these choices exist. Hence
\[
D\cap H=H\setminus K=A^{-1}(z).
\]
Both sides already have \(2^{n-2}\) points, the full size of \(D\), so \(D=A^{-1}(z)\) and the two cores are identical. Thus \(1+F_{A,z}-F_{B,w}=1\). Together with the preceding sum analysis, all affine cube-like combinations of two dual cores either fail to be ternary or collapse to constants/doubled Boolean functions.

### Proposition 2

If \(n\ge5\) and \(2\le k\le n-2\), then \(F_z\) is not a sum of two Boolean degree-one functions.

### Proof

First, canonical point coefficients are unique. Indeed, if \(M\) is the point-versus-\(k\)-space incidence matrix, then
\[
MM^{\mathsf T}=(r-\lambda)I+\lambda J,
\]
where \(r>\lambda\ge0\); hence this Gram matrix is positive definite.

The supplied Boolean classification and the identity
\[
y_r=1-2^{1-k}\sum_{r(x)=1}x_x
\]
show that the canonical coefficient function of one Boolean degree-one function has the form
\[
B_0+B_1\chi_r+D\delta_p,\qquad \chi_r(x)=(-1)^{r(x)}, \tag{4}
\]
where the character or delta term may be absent. A sum of two such functions therefore has, away from at most two points, the form
\[
B_0+B_1\chi_r+B_2\chi_s. \tag{5}
\]

On the other hand,
\[
2^{2-k}\mathbf1_{C_z}(x)
=2^{-k}\bigl(1+\epsilon_1\chi_a(x)+\epsilon_2\chi_b(x)
+\epsilon_1\epsilon_2\chi_{a+b}(x)\bigr), \tag{6}
\]
where \((-1)^{z_i}=\epsilon_i\). All four Fourier coefficients in (6) are nonzero.

Subtract (5) from (6), extending the functions to \(x=0\). If the result \(D\) is nonzero, then its physical support has size at most three (the two exceptional points and possibly zero), while its Fourier support has size at most seven. The finite-group uncertainty inequality
\[
|\operatorname{supp}D|\,|\operatorname{supp}\widehat D|\ge2^n
\]
would give \(2^n\le21\), impossible for \(n\ge5\). For completeness, this inequality follows from Parseval and
\(
\|\widehat D\|_\infty\le |\operatorname{supp}D|^{1/2}\|D\|_2
\).
If instead \(D=0\), Fourier uniqueness contradicts the fact that (6) has four nonzero characters whereas (5) has at most three. ∎

## 2. Further exact counterexamples in the small ranks

### 2.1 Minimum rank two

For \(k=2\), every projective cap \(S\subseteq V\setminus\{0\}\) gives
\[
f_S(L)=|L\cap S|\in\{0,1,2\}. \tag{7}
\]
There are already very broad families: every subset of an affine hyperplane is a cap, because the sum of two vectors in that coset lies in the parallel linear hyperplane. Consequently, the case \(\min(k,n-k)=2\) cannot have a short finite list of the suggested kind.

An exact enumeration of \(J_2(4,2)\) reconstructed all coefficient vectors from Fano-plane incidence. It found:

- 71,469 ternary degree-one functions;
- 37,113 distinct sums of two Boolean degree-one functions;
- 49 orbits under \(\mathrm{GL}(4,2)\) and value complementation, of which 13 are not Boolean-pair orbits.

One explicit non-pair coefficient vector, with points represented by the nonzero 4-bit integers, is
\[
c_1=c_2=-\tfrac12,\quad c_3=1,
\quad c_p=\tfrac12\ (p\in\{5,6,9,10,13,14\}),
\]
with all other coefficients zero. Its 35 line sums have level multiplicities \((17,15,3)\). The enumeration checked it against the complete supplied Boolean list.

### 2.2 Minimum rank three

Let
\[
Q(x)=x_1x_2+x_3x_4+x_5+x_5x_6+x_6
\]
on \(\mathbb F_2^6\), and define, for \(x\ne0\),
\[
c_x=\frac5{28}+\frac14(-1)^{Q(x)}. \tag{8}
\]
Then every 3-space \(L\) satisfies
\[
f(L)=\sum_{x\in L\setminus\{0\}}c_x
=1+\frac14\sum_{x\in L}(-1)^{Q(x)}. \tag{9}
\]
The form \(Q\) is the orthogonal sum of two hyperbolic planes and one anisotropic plane, so its Witt index is two. The polar form restricted to a 3-space has rank zero or two. If \(Q\) is nonzero on the radical, pairing along a radical vector makes the Walsh sum zero. Otherwise rank two gives Walsh sum \(\pm4\). Rank zero with \(Q|_L=0\) would make \(L\) a 3-dimensional totally singular space, contradicting Witt index two; rank zero with nonzero linear \(Q|_L\) again gives zero. Thus (9) lies in \(\{0,1,2\}\).

This function is not a Boolean pair sum. If it were, (4) would make \((-1)^Q\) constant, outside at most two exceptional nonzero points, on
\(K=\ker r\cap\ker s\), where \(\dim K\ge4\). After allowing the origin as a third possible exception, either \(Q|_K\) or \(Q|_K+1\) would have support at most three. A nonzero degree-at-most-two multilinear polynomial on \(\mathbb F_2^d\) has support at least \(2^{d-2}\ge4\) (an immediate induction on \(d\)). The relevant polynomial must therefore vanish identically. It cannot be \(Q|_K+1\), since \(Q(0)=0\); hence \(Q\) vanishes identically on \(K\), contradicting the Witt index.

Exact enumeration of all 1,395 three-spaces independently found restricted Walsh sums \(-4,0,4\) with multiplicities \(270,855,270\), and checked non-splitting against all 4,286 supplied Boolean functions.

## 3. A complete theorem for quotient-invariant coefficients

The strongest general classification proved during the search is the following.

### Theorem 3

Let \(A:V\twoheadrightarrow E=\mathbb F_2^d\), assume \(d\le k\) and \(\dim\ker A\ge k\), and suppose the canonical coefficient \(c_x\) depends only on \(A(x)\). If
\(f(L)=\sum_{x\in L\setminus\{0\}}c_x\) is ternary, then \(f\) is either

1. a sum of two Boolean degree-one functions built from the hyperplane indicators \(y_r\); or
2. an affine-codimension-two function \(F_z\) from (1), after composing with a quotient of \(E\), or its value complement \(2-F_z\).

### Proof

Write the fiber coefficient as \(w_z\), and put
\[
\phi(z)=2^kw_z-w_0. \tag{10}
\]
Every subspace \(R\le E\) occurs as \(A(L)\): lift a basis of \(R\) and add \(k-\dim R\) independent vectors of \(\ker A\), which is possible because \(d\le k\) and \(\dim\ker A\ge k\). If \(A(L)=R\), direct fiber counting gives
\[
f(L)=\frac1{|R|}\sum_{z\in R}\phi(z). \tag{11}
\]
Thus every linear-subspace average of \(\phi\) belongs to \(\{0,1,2\}\). In particular \(\phi(0)\in\{0,1,2\}\).

#### Case \(\phi(0)=0\)

For \(x\ne0\), the average on \(\{0,x\}\) gives
\(t(x)=\phi(x)/2\in\{0,1,2\}\). The average on every plane \(\{0,x,y,x+y\}\) shows
\[
t(x)+t(y)+t(x+y)\equiv0\pmod2.
\]
Hence \(t\bmod2\) is a linear functional \(\ell\).

If \(\ell=0\), write \(t=2\mathbf1_S\). Every subspace \(R\) then satisfies
\[
|S\cap R|\in\{0,|R|/4,|R|/2\}. \tag{12}
\]
The plane case says that \(S\) is sum-free. Let \(H=\langle S\rangle\). If \(|S|=|H|/4\), all hyperplane character sums of \(\mathbf1_S\) are \(0\) or \(\pm|S|\). Parseval forces exactly four nonzero Fourier coefficients. At a point of \(S\), equality in Fourier inversion forces their adjusted signs all to agree; hence their characters span a two-dimensional subgroup and \(S\) is an affine codimension-two coset in \(H\). Such a coset spans only a hyperplane of \(H\), a contradiction. Therefore \(|S|=|H|/2\). A half-sized sum-free subset is an affine hyperplane of \(H\): for \(s\in S\), the disjoint set \(s+S\) is the complement of \(S\), and that complement is a subgroup. Applying (12) after adjoining vectors outside \(H\) shows \(\operatorname{codim}_E H\le1\). Thus \(S\) is an affine hyperplane of \(E\), giving twice a Boolean function, or an affine codimension-two coset of \(E\), giving (1).

If \(\ell\ne0\), then \(t=1\) on the affine hyperplane \(\ell=1\), while \(t=2\mathbf1_T\) on \(K=\ker\ell\). For every \(K_0\le K\), apply (11) to \(R=\langle K_0,x\rangle\), where \(\ell(x)=1\). It follows that
\[
|T\cap K_0|\in\{0,|K_0|/2\}. \tag{13}
\]
If \(T\ne\varnothing\), (13) makes it a half-sized sum-free set in its span, and adjoining a vector outside that span shows the span is all of \(K\). Hence \(T\) is an affine hyperplane in \(K\). The resulting \(\phi\) is the sum of the two patterns
\(2\mathbf1_{r=1}\), which correspond through (11) to Boolean functions \(1-y_r\). The case \(T=\varnothing\) is one such Boolean function.

#### Case \(\phi(0)=2\)

Replace \(\phi\) by \(2-\phi\) and use the preceding case. This is value complementation.

#### Case \(\phi(0)=1\)

Put \(\psi=(\phi-1)/2\). Line averages give
\(\psi(0)=0\) and \(\psi(x)\in\{-1,0,1\}\). Plane parity shows that the support of \(\psi\) is either empty or an affine hyperplane \(\ell=1\). In the latter case, intersecting a 3-dimensional linear subspace with this support gives an affine 2-plane. Its average forces an even number of negative signs on every such affine 2-plane. Equivalently, all affine second derivatives of the sign exponent vanish, so the sign is an affine character. Therefore, for some \(m\),
\[
\phi=1+\epsilon(\chi_m-\chi_{m+\ell}).
\]
Averaging a character over \(R\) gives \(1\) exactly when its defining functional annihilates \(R\). (For \(d\le2\), the same affine-character conclusion follows directly, since the support has at most two points.) Consequently (11) becomes
\[
1+\epsilon(y_m-y_{m+\ell}),
\]
a sum of two Boolean degree-one functions. This completes all cases. ∎

Two independent exact enumerations support and audit this proof:

- quotient dimension two: 39 patterns, comprising 33 Boolean pair sums and the three \(F_z\) plus their complements;
- quotient dimension three: 171 patterns, comprising 129 Boolean pair sums and 42 lifts of affine codimension-two cores or their complements.

An exhaustive direct audit of the auxiliary subspace-average lemma in dimension four found exactly the analytically predicted patterns for both \(\phi(0)=0\) and \(\phi(0)=1\).

### Corollary 3.1 (low Fourier span)

Choose an extension of the canonical coefficient function to \(x=0\). If the indices of its nonzero Fourier coefficients span a subspace of \(V^*\) of dimension at most \(\min(k,n-k)\), then Theorem 3 applies: the function is a Boolean hyperplane-pair sum, an affine-codimension-two core, or its complement.

Indeed, a Fourier expansion supported on \(R\le V^*\) depends only on the quotient
\(V\to R^*\); the two displayed dimension bounds are exactly the two hypotheses of Theorem 3. In particular, when \(\min(k,n-k)\ge4\), every coefficient function whose Fourier indices span dimension at most four is completely covered. Applying the Fourier duality formula (15) below gives the symmetric low-span statement on the point side.

### Corollary 3.2 (one point delta plus a quotient)

Suppose
\[
f=h+d x_p,
\]
where the canonical coefficients of \(h\) factor through a surjection \(A:V\twoheadrightarrow E\), with \(\dim E\le k\) and \(\dim\ker A\ge k+1\). Then \(h\) itself is ternary and is classified by Theorem 3.

To see this, for every \(R\le E\) choose a \(k\)-space \(L\) with \(A(L)=R\) and \(p\notin L\). The extra kernel dimension lets one choose the kernel part of \(L\) avoiding the single vector which would put \(p\) in \(L\). Hence \(h(L)=f(L)\in\{0,1,2\}\) for every possible image \(R\), and (11) invokes Theorem 3. Once \(h\) is known, \(d\) is restricted by the elementary condition
\[
\{h(L):p\in L\}+d\subseteq\{0,1,2\}.
\]
This finite compatibility test yields (E) when \(h\) is a core and \(d=1\), and the supplied-Boolean cases checked above regroup into Boolean pair sums. Thus the “low Fourier span plus one point delta” regime is reduced to an explicit finite compatibility table. The reduction still does not force an arbitrary coefficient vector into this regime.

## 4. Exact local cubic reformulation

There is a useful necessary-and-sufficient local system which does not assume quotient invariance. Let
\(P(X)=X(X-1)(X-2)\). For a line \(\ell\) and 3-space \(T\), set
\[
B_\ell=\left(\sum_{p\in\ell}c_p\right)^3-\sum_{p\in\ell}c_p^3,
\qquad
D_\ell=\left(\sum_{p\in\ell}c_p\right)^2-\sum_{p\in\ell}c_p^2,
\]
and
\[
C_T=\left(\sum_{p\in T}c_p\right)^3
-\sum_{\ell\le T}B_\ell-\sum_{p\in T}c_p^3.
\]

### Proposition 4

If \(3\le k\le n-3\), then \(f\) is ternary if and only if every 3-space \(T\) satisfies
\[
C_T+\frac1{2^{k-2}-1}\sum_{\ell\le T}(B_\ell-3D_\ell)
+\frac1{\genfrac{[}{]}{0pt}{}{k-1}{2}_2}\sum_{p\in T}(c_p^3-3c_p^2+2c_p)=0. \tag{14}
\]

### Proof

Expand \(P(f)\) and group ordered tuples of points by whether they span a point, line, or 3-space. The corresponding coefficients are, respectively,
\[
c_p^3-3c_p^2+2c_p,\qquad B_\ell-3D_\ell,\qquad C_T.
\]
On \(J_2(n,k)\), lift lower incidence functions by
\[
x_\ell=\frac1{2^{k-2}-1}\sum_{T\supseteq\ell}x_T,\qquad
x_p=\frac1{\genfrac{[}{]}{0pt}{}{k-1}{2}_2}\sum_{T\supseteq p}x_T.
\]
The 3-space-to-\(k\)-space incidence matrix has full row rank over \(\mathbb R\) when \(3\le\min(k,n-k)\). One quick justification is the standard real-rank lemma for the subspace lattice: the \(i\)-space-to-\(j\)-space inclusion matrix has full row rank whenever \(i\le j\le n-i\). It follows from the up/down identity
\[
D_{r+1}U_r-U_{r-1}D_r=([n-r]_2-[r]_2)I
\]
by decomposing the \(r\)-th level into the orthogonal harmonic spaces \(U^{r-s}\ker D_s\); iteration shows that inclusion to level \(j\le n-i\) is nonzero on every summand. Taking \(i=3\) gives the claim. Hence \(P(f)=0\) is equivalent to the vanishing of every lifted coefficient, which is (14). Finally, \(P(f(L))=0\) over the reals is equivalent to \(f(L)\in\{0,1,2\}\). ∎

Exact rational evaluation checked (14) on all 97,155 three-spaces of \(\mathbb F_2^8\) for (1), with no failure. This converts the missing classification into a cubic compatibility problem on overlapping Fano planes. The same system can be applied after orthogonal duality to the Fourier-transformed coefficient vector.

## 5. Other approaches tested and discarded

1. **Universal Boolean splitting.** Falsified by the exact \(J_2(4,2)\) enumeration, by the elliptic \(J_2(6,3)\) example, and by Proposition 2 in arbitrary rank.

2. **Thresholding.** The indicators \(\mathbf1[f\ge1]\) and \(\mathbf1[f=2]\) need not have degree one. Algebraically,
   \[
   \mathbf1[f=2]=\frac{f(f-1)}2,\qquad
   \mathbf1[f=0]=\frac{(f-1)(f-2)}2
   \]
   have degree at most two, not one.

3. **Reduction to arbitrary Boolean degree two.** The two indicators above have the same top-degree component because their difference is \(f-1\). This is exact, but current degree-two Grassmann examples are broad, and no classification of disjoint Boolean degree-two pairs with equal top component was found.

4. **Nondegenerate quadratic phases at rank four.** On all 200,787 four-spaces of \(\mathbb F_2^8\), an elliptic nondegenerate quadratic phase has restricted Walsh values \(-8,-4,0,4,8\), so no affine rescaling is ternary. All tested one- and two-quadratic-character combinations still had at least five values. Within the complete one-phase affine-rescaling ansatz, an audit over every quadratic rank and type showed that only rank-two hyperbolic forms give the affine-coset core; rank-two elliptic values are not in arithmetic progression, and higher ranks give at least five levels.

5. **Other algebraic phase searches.** Two thousand random cubic phases, 500 structured Maiorana–McFarland phases, 80 random quadratic pairs, and rank-six quadratic-plus-linear representatives all produced at least five or six restricted sums. These are falsification searches, not theorems.

6. **Single matrix chart.** On graph charts \(L=\Gamma_A\), the Fourier support of \(f(\Gamma_A)\) consists only of rank-at-most-one matrix frequencies. Exact classification on \(2\times2\) matrices nevertheless found 192 ternary exceptions beyond Boolean pair sums. Therefore compatibility among different projective charts is essential.

7. **Symmetric and decomposition-invariant rank-four ansatzes.** The full \(S_8\)-invariant coefficient subspace on \(J_2(8,4)\) has exactly 19 ternary solutions, all expected constants/Boolean pairs. Coefficients invariant under \(\mathrm{GL}(4,2)\times\mathrm{GL}(4,2)\) give only constants. These are exact invariant-subspace classifications, not a global result.

8. **Adjacency/eigenvalue equations.** Since degree one is \(V_0\oplus V_1\), the weighted neighbor sum is determined by \(f(L)\). For three levels this gives only one weighted equation for the two nontrivial neighbor counts and does not force an equitable 3-partition.

9. **Ramsey quantization.** Restriction to every \((k+1)\)-space puts each canonical coefficient in a finite set, and projective Ramsey yields a large homogeneous subspace. A \(k\)-space inside it forces the common coefficient to be \(0\), \((2^k-1)^{-1}\), or \(2(2^k-1)^{-1}\). Around a zero-coefficient homogeneous subspace, each affine coset coloring itself has ternary sums on lower-dimensional affine flats. The unresolved issue is making the many affine Ramsey witnesses compatible with one common quotient; quantization alone does not do this.

10. **Local cubic Jacobian.** An optimized exact modular computation found full rank 255 at the \(J_2(8,4)\) affine core. This initially looked like rigidity, but it is automatic at every ternary solution: before incidence lifting, the Jacobian is
    \[
    \operatorname{diag}(P'(f(L)))M^{\mathsf T},
    \]
    where \(P'(0)=P'(2)=2\), \(P'(1)=-1\), and \(M\) has full row rank. Thus nonsingularity only restates that the finite set of ternary value assignments is discrete; it contributes no classification and was discarded.

11. **Convex/integrality formulation.** A Boolean splitting would amount to finding a Boolean degree-one \(g\) with \(0\le g\le f\). The hope that the corresponding degree-one slice of the cube was integral is refuted by the exact non-splitting examples; no valid separator or total-unimodularity statement survived.

12. **Spread and code constructions.** Natural functions obtained from a binary spread and its completely regular code quotient were checked spectrally. Their characteristic vectors have components in \(V_0,V_2,V_4\), not just \(V_0,V_1\), so they do not produce degree-one counterexamples.

13. **Unweighted support geometry.** For \(k\ge3\), a point set meeting every \(k\)-space in at most two points has at most two points globally, because any three points lie in a subspace of dimension at most three and can be extended to a \(k\)-space. This kills the direct cap construction beyond rank two, but not weighted three-intersection sets, which remain part of the obstruction in Section 6.

14. **Stability/FKN route.** Exact Boolean degree-one stability results apply to Boolean targets. The natural level indicators of a ternary \(f\) have degree at most two, and the available degree-one result therefore cannot be applied without precisely the missing degree-two structural input.

## 6. Exact remaining obstruction

The quotient theorem would finish a large and natural class, but an arbitrary canonical coefficient function need not be constant on the fibers of any low-dimensional quotient. The elliptic rank-three example has high Fourier support and proves that such a reduction is false at small rank. What remains unproved for high rank is a rigidity theorem of the following general shape:

> after removing the permitted point-delta terms, every ternary degree-one coefficient vector either has bounded-dimensional Fourier span (so Theorem 3 applies), or its orthogonal dual has that property.

The duality here is completely explicit. Extend \(c\) to \(V\) by choosing \(c_0\), and use the unnormalized Fourier transform
\(\widehat c(r)=\sum_{x\in V}c_x(-1)^{r(x)}\). Character orthogonality gives
\[
f(L)=2^{k-n}\sum_{r\in L^\perp}\widehat c(r)-c_0. \tag{15}
\]
The \(r=0\) term and \(-c_0\) are constant and can be distributed uniformly over the nonzero points of \(L^\perp\). Thus (15) gives the canonical point coefficients of the orthogonal-dual degree-one function, and Proposition 4 applies to them with \(k\) replaced by \(n-k\).

No sparse-or-low-Fourier-span statement was proved. Equation (14), applied through (15) on the dual side, gives exact constraints, but a classification of their common real solutions on overlapping Fano planes is still missing. This is the precise point at which the proof search stops; it is not legitimate to assert that the affine-coset family and compatible Boolean additions are exhaustive.

Even the nonnegative equal-weight subcase contains a finite-geometric intersection problem. If \(c_x=\alpha\mathbf1_S(x)\), then every \(k\)-space must meet \(S\) in one of the three cardinalities \(0,1/\alpha,2/\alpha\). At \(k=2\) this already contains arbitrary projective caps, as in (7). For larger \(k\), proving that the relevant three-intersection sets reduce to affine codimension-two fibers is itself an unproved part of the required global rigidity statement.

## 7. Most promising next route

The strongest route is to combine (14) with its orthogonal dual and prove a sparse-or-low-Fourier-span dichotomy. Concretely:

1. subtract constants and at most two point deltas, as suggested by the supplied Boolean classification;
2. compare (14) on two 3-spaces sharing a line, obtaining equations for coefficient patterns on parallel affine 2-flats;
3. apply the dual equations to the Fourier coefficient function;
4. prove that a solution with both large physical support and large Fourier span forces at least four values on some \(k\)-space;
5. invoke Theorem 3 once a bounded Fourier span is obtained, then perform the finite compatibility analysis for added Boolean functions.

After the compatibility simplifications in Section 1, the verified high-rank examples are: sums of two supplied Boolean functions; the affine cores (1); the core-plus-point forms (E); their orthogonal duals; and value complements. Their exhaustiveness is a candidate classification only, not a proved statement.

## 8. Reproducibility

All exact scripts are in `tmp/`. The full chronological record, including false claims and their repairs, is in `WORKLOG.md`. The source PDF was extracted with Poppler and visually checked from a rendered page before proof search began.
