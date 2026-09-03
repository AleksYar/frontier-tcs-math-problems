# Solution

Fix an integer $c>2$. Give $[n]$ its cyclic order

\[
1,2,\ldots,n,1.
\]

A **cyclic interval** is a consecutive set in this cyclic order (so it may be an ordinary interval, or a suffix together with a prefix). Let

\[
\mathcal I_n^{(c)}
 =\{\text{partitions of the cyclically ordered set }[n]
       \text{ into at most }c\text{ nonempty cyclic intervals}\}.
\]

This is a small, distribution-independent, natural inventory. A partition into $k$ cyclic intervals is determined by choosing its $k$ boundary gaps, so, regarding answer names as irrelevant,

\[
|\mathcal I_n^{(c)}|
 \le 1+\sum_{k=2}^{\min(c,n)}\binom nk
 =O_c(n^c).
\]

We prove that this inventory always gives expected cost strictly smaller than $H_c(\mu)+1$.

## 1. A shifted $c$-adic grid

We may discard zero-probability elements and retain the induced cyclic order, since $x\sim\mu$ always lies in the support. Any cyclic-interval partition of the support lifts to one of $[n]$: assign every intervening zero-probability element to either adjacent block. Thus the lifted questions still belong to $\mathcal I_n^{(c)}$. Write the positive probabilities as $p_1,\ldots,p_N$. Partition the unit circle consecutively into half-open arcs

\[
J_1,J_2,\ldots,J_N,
\qquad |J_i|=p_i,
\]

in the cyclic order of the corresponding elements.

For $u\in[0,1)$ and $k\ge0$, let

\[
\mathcal G_k(u)
 =\left\{
 \left[u+\frac{j}{c^k},u+\frac{j+1}{c^k}\right)
 \pmod 1:0\le j<c^k
 \right\}.
\]

These partitions are nested: every cell of $\mathcal G_k(u)$ has exactly $c$ children in $\mathcal G_{k+1}(u)$.

For every $i$, let $\ell_i(u)$ be the least $k$ for which some cell of $\mathcal G_k(u)$ is contained in $J_i$, and choose one such cell $K_i(u)\subseteq J_i$. Since the arcs $J_i$ are pairwise disjoint, the chosen cells $K_i(u)$ are pairwise disjoint. Cells in a nested grid are either disjoint or one contains the other, so no chosen cell contains another. Consequently the paths from the root grid cell to the cells $K_i(u)$ form a $c$-ary prefix code, with codeword lengths $\ell_i(u)$.

## 2. The code uses only questions in $\mathcal I_n^{(c)}$

Consider the trie of the chosen grid cells and suppress every unary vertex. At a remaining internal vertex, its nonempty children contain consecutive blocks of the chosen cells around the circle. Because $K_i(u)\subseteq J_i$, the cyclic order of the chosen cells is the original cyclic order of the symbols. Thus the nonempty children partition the currently possible symbols into at most $c$ consecutive cyclic blocks.

This local partition can be extended to a partition of all of $[n]$ into the same number of cyclic intervals: if the current candidate block is proper, merge its cyclic-interval complement into either end child. Hence every internal vertex is implemented by a question in $\mathcal I_n^{(c)}$. Suppressing unary vertices can only shorten codewords, so the resulting strategy has average cost at most

\[
L(u):=\sum_{i=1}^N p_i\ell_i(u).
\]

## 3. Expected length under a random shift

We need one elementary geometric fact.

**Lemma.** Let $J$ be a circle arc of length $p\in(0,1)$. Put

\[
m=\left\lceil\log_c\frac1p\right\rceil,
\qquad s=c^{-m},
\qquad r=\frac ps.
\]

Then $1\le r<c$. If $U$ is uniform on $[0,1)$, the first level of the shifted grid having a cell contained in $J$ satisfies:

- if $2\le r<c$, then $\ell(U)=m$ with probability $1$;
- if $1\le r<2$, then
  \[
  \Pr(\ell(U)=m)=r-1,
  \qquad
  \Pr(\ell(U)=m+1)=2-r.
  \]

**Proof.** A level-$m$ cell has length $s$, while a level-$(m-1)$ cell has length $cs>p$, so no coarser level can work. The distance from the left endpoint of $J$ to the next level-$m$ grid boundary is uniform modulo $s$. A full length-$s$ cell lies in $J$ exactly when this distance is at most $p-s$. For $p<2s$, this event therefore has probability

\[
\frac{p-s}{s}=r-1.
\]

For $p\ge2s$, every translate of the length-$s$ grid has a full cell in $J$. Finally, a level-$(m+1)$ cell has length $s/c$, and

\[
p\ge s=c(s/c)\ge3(s/c)>2(s/c).
\]

Thus level $m+1$ always works when level $m$ does not. $\square$

For $p=p_i$, retain the notation $m_i,s_i,r_i$. Since

\[
\log_c\frac1{p_i}=m_i-\log_c r_i,
\]

the lemma gives the following expected pointwise excess over self-information.

If $2\le r_i<c$, then

\[
\mathbb E\ell_i(U)-\log_c\frac1{p_i}
=\log_c r_i<1.
\]

If $1<r_i<2$, then

\[
\mathbb E\ell_i(U)-\log_c\frac1{p_i}
=2-r_i+\log_c r_i<1.
\]

Indeed, because $c\ge3$, we have $\ln c>1$, and for $r>1$,

\[
\log_c r=\frac{\ln r}{\ln c}<\ln r<r-1.
\]

If $r_i=1$, the expected excess is exactly $1$. Notice that $r_i=1$ is equivalent to $p_i=c^{-m_i}$.

By linearity of expectation,

\[
\mathbb E L(U)
=\sum_i p_i\,\mathbb E\ell_i(U).
\]

Therefore, if at least one positive $p_i$ is not an integral power of $c$, then

\[
\mathbb E L(U)
<\sum_i p_i\left(\log_c\frac1{p_i}+1\right)
=H_c(\mu)+1.
\]

It follows that some deterministic shift $u$ satisfies $L(u)<H_c(\mu)+1$.

## 4. The $c$-adic exceptional case

Suppose every positive probability is an integral power of $c$. If the support has one point, no question is needed and the result is immediate. Otherwise write

\[
p_i=c^{-m_i},\qquad m_i\ge1.
\]

Choose one index $i_0$, and choose the shift $u$ to be the left endpoint of $J_{i_0}$. Then $J_{i_0}$ itself is a level-$m_{i_0}$ grid cell, so

\[
\ell_{i_0}(u)\le m_{i_0}.
\]

For every other $i$, the final part of the lemma's proof, which did not use randomness, shows that

\[
\ell_i(u)\le m_i+1.
\]

Consequently

\[
\begin{aligned}
L(u)
&\le p_{i_0}m_{i_0}
   +\sum_{i\ne i_0}p_i(m_i+1)\\
&=\sum_i p_i m_i+1-p_{i_0}\\
&=H_c(\mu)+1-p_{i_0}\\
&<H_c(\mu)+1.
\end{aligned}
\]

The associated trie strategy uses only questions in $\mathcal I_n^{(c)}$, by Section 2. This completes the proof.

## Remark on the statement's Gilbert--Moore sentence

The displayed claim in the supplied PDF that interval questions give $H_c(\mu)+\log_c2$ cannot be correct literally: for $c=3$ and $\mu=(\varepsilon,1-2\varepsilon,\varepsilon)$, every strategy costs at least one question while $H_3(\mu)+\log_3 2\to\log_3 2<1$. The standard midpoint/Gilbert--Moore ceiling calculation gives $H_c(\mu)+1+\log_c2$. The proof above is independent of that sentence and establishes the requested strict $H_c(\mu)+1$ bound.
