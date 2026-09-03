# Davenport-Schinzel Sequences in the Critical Regime

## Result

For every fixed constant \(c>0\),

\[
\boxed{\lambda_{\lfloor c\sqrt n\rfloor}(n)=\Theta_c(n^{5/2}).}
\]

More explicitly, define

\[
a=\min\{1,c/4\},\qquad \delta=c-3a>0.
\]

Then, for all sufficiently large \(n\),

\[
\frac{\delta a^4}{64}n^{5/2}
\le \lambda_{\lfloor c\sqrt n\rfloor}(n)
\le \frac c2n^{5/2}+1.
\]

## 1. Pairwise runs and the upper bound

For distinct symbols \(a,b\), project a word \(U\) onto the alphabet \(\{a,b\}\), and let \(\rho_{a,b}(U)\) be the number of runs in this binary projection. Its longest alternating subsequence has length exactly \(\rho_{a,b}(U)\). Hence

\[
U\in\mathrm{DS}(n,s)
\quad\Longrightarrow\quad
\rho_{a,b}(U)\le s+1.
\]

Let \(t_{a,b}\) count the indices \(i\) for which

\[
\{u_i,u_{i+1}\}=\{a,b\}.
\]

Every such adjacency produces a distinct change of run in the \(\{a,b\}\)-projection. Therefore

\[
t_{a,b}\le \rho_{a,b}(U)-1\le s.
\]

Every adjacent pair of \(U\) belongs to exactly one unordered symbol pair, and consequently

\[
|U|-1
=\sum_{\{a,b\}}t_{a,b}
\le \binom n2s.
\]

Thus, for \(s=\lfloor c\sqrt n\rfloor\),

\[
\lambda_s(n)
\le \binom n2s+1
\le \frac c2n^{5/2}+1.
\tag{1}
\]

## 2. A base construction

We construct long order-\(h\) sequences on \(r\) symbols whenever \(h\ge r\ge2\).

Define \(R(h,r)\) recursively as follows.

- \(R(h,2)\) is the alternating word \(1,2,1,2,\ldots\) of length \(h+1\).
- \(R(2,r)=1,2,1,3,1,\ldots,1,r,1\).
- For \(h,r\ge3\), put

  \[
  \ell=\left\lceil\frac{h-2}{2}\right\rceil
  \]

  and

  \[
  A_{h,r}=(1,2)^\ell(1,3)^\ell\cdots(1,r)^\ell\,1.
  \]

  Append to \(A_{h,r}\) a copy of \(R(h-1,r-1)\) in which each symbol \(j\) is relabelled as \(r-j+1\). The suffix therefore uses the symbols \(r,r-1,\ldots,2\) in decreasing first-occurrence order.

We prove by induction that \(R(h,r)\) has no immediate repetitions, starts with \(1\), has first occurrences in the order \(1,2,\ldots,r\), and belongs to \(\mathrm{DS}(r,h)\). The assertions are immediate in the two base cases. In the recursive case, the boundary between the prefix and suffix is \(1,r\), so it creates no immediate repetition.

Consider first a pair \(\{1,j\}\). The projection of \(A_{h,r}\) onto this pair has exactly \(2\ell+1\) runs. The suffix contains \(j\) but not \(1\), so it adds at most one run. Thus

\[
\rho_{1,j}(R(h,r))
\le 2\ell+2
\le h+1.
\]

Now consider \(2\le i<j\le r\). The projection of \(A_{h,r}\) consists of two runs, \(i,j\). By induction, the suffix is order \(h-1\), so its \(\{i,j\}\)-projection has at most \(h\) runs. Its first run is a \(j\)-run because first occurrences in the suffix are decreasing. This run merges with the terminal \(j\)-run of the prefix. Consequently

\[
\rho_{i,j}(R(h,r))
\le 2+h-1
=h+1.
\]

This proves that \(R(h,r)\in\mathrm{DS}(r,h)\).

Let \(L(h,r)=|R(h,r)|\). We claim that, whenever \(h\ge r\ge2\),

\[
L(h,r)\ge \binom r2(h-r)+r.
\tag{2}
\]

For \(r=2\), this says \(h+1\ge h\). For \(r\ge3\), the recurrence is

\[
L(h,r)
=2(r-1)\left\lceil\frac{h-2}{2}\right\rceil+1
+L(h-1,r-1).
\]

Using the induction hypothesis and

\[
2\left\lceil\frac{h-2}{2}\right\rceil\ge h-r,
\]

we obtain

\[
\begin{aligned}
L(h,r)
&\ge (r-1)(h-r)+1
  +\binom{r-1}{2}(h-r)+(r-1)\\
&=\binom r2(h-r)+r.
\end{aligned}
\]

This proves (2).

## 3. The finite-field lift

Let \(q\) be a power of two and work over \(\mathbb F_q\). Use the \(q^2\) affine functions

\[
f_{c_0,c_1}(x)=c_0+c_1x,
\qquad (c_0,c_1)\in\mathbb F_q^2,
\]

as symbols. For every \((x,v)\in\mathbb F_q^2\), define

\[
C_{x,v}=\{f:f(x)=v\}.
\]

These supports satisfy:

1. \(|C_{x,v}|=q\), since after choosing \(c_1\), the coefficient \(c_0\) is uniquely determined;
2. every affine function belongs to exactly \(q\) supports, one for each \(x\in\mathbb F_q\);
3. two distinct affine functions belong together to at most one support, because two distinct affine functions agree at at most one value of \(x\).

On each support \(C_{x,v}\), place a relabelled copy of \(R(h,q)\), and concatenate the resulting \(q^2\) blocks in any order. If the last symbol of one block equals the first symbol of the next block, delete the first symbol of the later block. Since each block has no immediate repetitions, this repairs every boundary and deletes at most \(q^2-1\) symbols. Moreover, deletion cannot create a new alternating subsequence.

Fix two distinct affine functions \(f,g\).

If they share a support, then their common block contributes at most \(h+1\) runs. Outside that block, there are \(q-1\) blocks containing \(f\) but not \(g\), and \(q-1\) containing \(g\) but not \(f\). Each such block contributes at most one run. Hence

\[
\rho_{f,g}\le h+1+2(q-1)=h+2q-1.
\]

If they share no support, there are at most \(2q\) nonempty projected blocks, each contributing at most one run. Thus

\[
\rho_{f,g}\le2q\le h+2q-1,
\]

where the last inequality uses \(h\ge1\).

The lifted sequence therefore has order at most

\[
h+2q-2.
\tag{3}
\]

By (2), its length is at least

\[
\begin{aligned}
q^2L(h,q)-(q^2-1)
&\ge q^2\left[\binom q2(h-q)+q\right]-(q^2-1)\\
&\ge q^2\binom q2(h-q).
\end{aligned}
\tag{4}
\]

## 4. Choice of parameters

Fix \(c>0\) and set

\[
s=\lfloor c\sqrt n\rfloor,
\qquad
a=\min\{1,c/4\},
\qquad
\delta=c-3a.
\]

The number \(\delta\) is positive: if \(c\le4\), then \(\delta=c/4\), while if \(c\ge4\), then \(\delta=c-3\ge1\).

Let \(q\) be the largest power of two satisfying

\[
q\le a\sqrt n.
\]

For all sufficiently large \(n\),

\[
\frac{a\sqrt n}{2}<q\le a\sqrt n,
\qquad q^2\le n.
\tag{5}
\]

Set

\[
h=s-2q+2.
\]

Then

\[
\begin{aligned}
h-q
&=\lfloor c\sqrt n\rfloor-3q+2\\
&\ge c\sqrt n-1-3a\sqrt n+2\\
&=\delta\sqrt n+1.
\end{aligned}
\tag{6}
\]

In particular, \(h\ge q\), so the base construction applies. By (3), the lifted sequence has order at most

\[
h+2q-2=s.
\]

Its alphabet has \(q^2\le n\) symbols, so it may be regarded as a sequence over \([n]\). From (4), (5), (6), and

\[
\binom q2\ge\frac{q^2}{4}\qquad(q\ge2),
\]

we obtain

\[
\begin{aligned}
\lambda_s(n)
&\ge q^2\binom q2(h-q)\\
&\ge \frac{q^4}{4}\,\delta\sqrt n\\
&\ge \frac{\delta a^4}{64}n^{5/2}.
\end{aligned}
\tag{7}
\]

Combining (1) and (7) proves

\[
\lambda_{\lfloor c\sqrt n\rfloor}(n)=\Theta_c(n^{5/2}).
\]

This determines the asymptotic order of growth. It does not assert the existence or value of a sharper normalized limit

\[
\lim_{n\to\infty}n^{-5/2}\lambda_{\lfloor c\sqrt n\rfloor}(n).
\]
