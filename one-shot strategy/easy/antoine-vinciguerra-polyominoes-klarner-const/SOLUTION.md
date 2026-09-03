# A rigorous improvement of the upper bound for Klarner's constant

## Result

Let \(A(n)\) be the number of fixed \(n\)-cell polyominoes and

\[
\lambda=\lim_{n\to\infty}A(n)^{1/n}.
\]

Then

\[
\boxed{\lambda\le 4.5235<4.5238.}
\]

Thus this strictly improves the upper bound requested in the problem.

The combinatorial input is the 17-neighborhood recurrence lemma of V. Bui,
[*A convolutional approach to bounding the number of polyominoes*, Lemma 4](https://arxiv.org/html/2511.00461v2#S4.SS0.SSS0.Px1).
The improvement itself is a new exact rational certificate at
\(\zeta=1/4.5235\).

## 1. The neighborhood recurrences

For clarity, here is the complete recurrence statement used below. A neighborhood
is a finite pattern in which a square denotes a cell required to belong to the
polyomino, a cross denotes a position required not to belong to it, and every
unshown position is unrestricted. For a neighborhood type \(N\), let \(N(n)\)
be the number of occurrences of that pattern among all fixed \(n\)-cell
polyominoes. All sums below are over positive indices, and every sequence is
defined to be zero at nonpositive indices.

There are seventeen types

\[
C,D,E,F,G,H,P,Q,R,S,T,U,V,W,X,Y,Z.
\]

The six one-cell types have

\[
C(1)=D(1)=E(1)=F(1)=G(1)=H(1)=1,
\]

and the eleven types containing at least two required cells have value zero at
\(n=1\). For every \(n\ge2\), Bui's local-decomposition lemma gives

\[
\begin{aligned}
C(n)&\le E(n-1),&D(n)&\le G(n-1),&E(n)&\le F(n-1),\\
F(n)&\le G(n)+P(n),&G(n)&\le E(n)+Q(n),&H(n)&\le D(n)+S(n),\\
P(n)&\le \sum_{i+j=n}\!\big(E(i)H(j)+Q(i)D(j)+X(i)R(j)+V(i)Y(j)\big)
       +\sum_{i+j+k=n}U(i)Y(j)Z(k),\\
Q(n)&\le G(n-1)+\sum_{i+j=n-1}G(i)E(j)+U(n-2)
       +\sum_{i+j=n-2}\!\big(T(i)G(j)+R(i)U(j)\big),\\
R(n)&\le Y(n)+W(n),\\
S(n)&\le G(n-1)+\sum_{i+j=n-1}E(i)E(j)+T(n-2)
       +\sum_{i+j=n-2}\!\big(X(i)G(j)+Y(i)U(j)\big),\\
T(n)&\le X(n)+V(n),\\
U(n)&\le \sum_{i+j=n}\!\big(D(i)H(j)+S(i)D(j)+Y(i)R(j)+W(i)Y(j)\big)
       +\sum_{i+j+k=n}U(i)Z(j)Z(k),\\
V(n)&\le S(n-1)+\sum_{i+j=n-2}\!\big(G(i)G(j)+T(i)E(j)+R(i)T(j)\big),\\
W(n)&\le S(n-1)+\sum_{i+j=n-2}\!\big(E(i)G(j)+X(i)E(j)+Y(i)T(j)\big),\\
X(n)&\le D(n-1)+G(n-2)+U(n-2),\\
Y(n)&\le C(n-1)+G(n-2)+T(n-2),\\
Z(n)&\le C(n-1)+E(n-2)+X(n-2).
\end{aligned}\tag{1}
\]

These inequalities come from partitioning according to the occupancy of the
few unspecified cells immediately above the displayed neighborhood and then
cutting the resulting occurrence into two or three smaller marked polyominoes.
The products in (1) count the resulting ordered tuples. This is a finite local
case decomposition; the cited lemma gives every pattern and every case diagram.

The type \(G\) has one required cell, with its left neighbor and the three
positions immediately below it forbidden. In every polyomino, the leftmost cell
of the bottommost occupied row is an occurrence of \(G\). Conversely, an
\(n\)-cell polyomino has at most \(n\) possible marked cells. Hence

\[
A(n)\le G(n)\le nA(n).\tag{2}
\]

## 2. Majorants and the certificate criterion

Define \(\widehat C(n),\ldots,\widehat Z(n)\) by the same initial values as
above and by replacing every inequality in (1) by equality. These sequences
are well-defined: for a fixed \(n\), first compute

\[
\widehat C,\widehat D,\widehat E,\widehat Q,\widehat S,
\widehat V,\widehat W,\widehat X,\widehat Y,\widehat Z,
\widehat P,\widehat U
\]

at index \(n\) from smaller indices, and then compute
\(\widehat G,\widehat F,\widehat H,\widehat T,\widehat R\) at index \(n\).
Induction in this order and (1) give

\[
G(n)\le \widehat G(n)\qquad(n\ge1).\tag{3}
\]

Let the capital letters now denote the generating functions of the majorants;
for example \(G(t)=\sum_{n\ge1}\widehat G(n)t^n\). As identities of formal
power series they obey

\[
\begin{aligned}
C&=t+tE,&D&=t+tG,&E&=t+tF,&F&=G+P,&G&=E+Q,&H&=D+S,\\
P&=EH+QD+XR+VY+UYZ,\\
Q&=tG+tGE+t^2(U+TG+RU),&R&=Y+W,\\
S&=tG+tE^2+t^2(T+XG+YU),&T&=X+V,\\
U&=DH+SD+YR+WY+UZ^2,\\
V&=tS+t^2(G^2+TE+RT),\\
W&=tS+t^2(EG+XE+YT),\\
X&=tD+t^2(G+U),\\
Y&=tC+t^2(G+T),\\
Z&=tC+t^2(E+X).
\end{aligned}\tag{4}
\]

Write \(\Phi_t\) for the nonnegative polynomial map given by the right-hand
sides of (4).

**Certificate lemma.** If \(t>0\) and a finite nonnegative vector
\(a=(c,d,\ldots,z)\) satisfies

\[
a\ge \Phi_t(a)\tag{5}
\]

componentwise, then every series in (4) converges at \(t\), with its value at
most the corresponding component of \(a\).

**Proof.** Start at the zero vector and iterate \(a^{(k+1)}=\Phi_t(a^{(k)})\).
The map is coordinatewise nondecreasing and \(\Phi_t(0)\ge0\), so these
iterates are increasing. Moreover, (5) implies inductively

\[
0\le a^{(k)}\le a\qquad(k\ge0).
\]

Run the same iteration with the indeterminate \(t\) in the semiring of formal
power series with nonnegative coefficients. Every coefficient in (4) is
determined from lower-degree coefficients, followed by the acyclic same-degree
order displayed before (3). Consequently, for every fixed degree, the iterates
eventually stabilize at the coefficient of the unique formal solution of (4).
After substituting the positive real value of \(t\), monotone convergence shows
that each full series is the supremum of the corresponding iterates. It is thus
bounded by the corresponding component of \(a\). This proves the lemma. \(\square\)

## 3. Exact rational certificate at \(4.5235\)

Set

\[
t=\frac{10000}{45235}=\frac1{4.5235}.
\]

Use the following rational vector:

|coordinate|value|coordinate|value|
|---:|---:|---:|---:|
|\(c\)|\(1740517/5000000\)|\(d\)|\(1077131/2500000\)|
|\(e\)|\(5746453/10000000\)|\(f\)|\(99963/62500\)|
|\(g\)|\(1186201/1250000\)|\(h\)|\(1477811/2000000\)|
|\(p\)|\(813059/1250000\)|\(q\)|\(748631/2000000\)|
|\(r\)|\(1194337/5000000\)|\(s\)|\(3080531/10000000\)|
|\(t_0\)|\(22649/78125\)|\(u\)|\(1260813/2500000\)|
|\(v\)|\(1236361/10000000\)|\(w\)|\(1013683/10000000\)|
|\(x\)|\(1662711/10000000\)|\(y\)|\(1374991/10000000\)|
|\(z\)|\(565819/5000000\)| | |

Here \(t_0\) is the coordinate corresponding to the generating function \(T\),
whereas \(t=10000/45235\) remains the series argument.

Substitution in (5) is exact rational arithmetic. To make the numerical part
fully checkable, the following table lists every margin
``left side minus right side'' in the order of (4):

|coordinate|exact margin|coordinate|exact margin|
|---:|---:|---:|---:|
|\(c\)|\(4299/45235000000\)|\(d\)|\(157/22617500000\)|
|\(e\)|\(291/90470000000\)|\(f\)|\(0\)|
|\(g\)|\(0\)|\(h\)|\(0\)|
|\(p\)|\(4727987932623/125000000000000000000\)|\(q\)|\(667046423/63943913281250000\)|
|\(r\)|\(0\)|\(s\)|\(126730157177/4092410450000000000\)|
|\(t_0\)|\(0\)|\(u\)|\(3776731826307/62500000000000000000\)|
|\(v\)|\(70275629/4092410450000000\)|\(w\)|\(100883017/4092410450000000\)|
|\(x\)|\(44178599/818482090000000\)|\(y\)|\(1545119/818482090000000\)|
|\(z\)|\(29170171/409241045000000\)| | |

Every margin is nonnegative. The five zero margins are the deliberate exact
equalities \(f=g+p\), \(g=e+q\), \(h=d+s\), \(r=y+w\), and \(t_0=x+v\).
Thus (5) holds, so the certificate lemma gives

\[
\sum_{n\ge1}\widehat G(n)t^n<\infty.
\]

By the Cauchy-Hadamard formula,

\[
\limsup_{n\to\infty}\widehat G(n)^{1/n}\le \frac1t=4.5235.
\]

Finally, (2) and (3) imply

\[
\lambda=\lim_{n\to\infty}A(n)^{1/n}
\le \limsup_{n\to\infty}\widehat G(n)^{1/n}
\le4.5235<4.5238.
\]

This proves the claimed improvement. \(\blacksquare\)

## 4. Reproducibility checks

The exact fractions above are independently machine-checkable with
`python3 verify_certificate.py`. The separate script `brute_audit.py` enumerates
all fixed polyominoes through size 10 and checks all seventeen combinatorial
recurrences on those instances; that finite test is supplementary and is not
used as a substitute for the all-\(n\) neighborhood lemma.
