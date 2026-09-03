# Relative-periodic coupled graphs: complete classification

Let
\[
F(p)=\frac{p}{\sqrt{1+p^2}}
\]
and let \(|\mathbb T|=2\pi\). We first regard the solution on the time
interval \([0,T]\) appearing in the hypothesis; the usual forward-time
interpretation is addressed explicitly below.

## Theorem

Every smooth periodic solution satisfying
\[
u(x,T)=u(x+a,0)+b,\qquad v(x,T)=v(x+a,0)+b
\]
restricts on \(\mathbb T\times[0,T]\) to a common constant:
\[
u(x,t)=v(x,t)=c
\]
for some \(c\in\mathbb R\). If the solution is defined for all \(t\ge0\), it
is this same constant for all \(t\ge0\). Consequently,
the complete set of possible triples is
\[
(a,b,T)\in \mathbb T\times\{0\}\times(0,\infty).
\]
Conversely, for every such triple and every \(c\in\mathbb R\), the common
constant pair is a solution satisfying the relative-return condition.

## Proof

Define
\[
\mathcal L(u,v)=\int_{\mathbb T}
\left(\sqrt{1+u_x^2}+\sqrt{1+v_x^2}+\frac12(u-v)^2\right)\,dx.
\]
Smoothness and periodicity permit differentiation under the integral and
integration by parts. Thus
\[
\begin{aligned}
\frac{d}{dt}\mathcal L(u,v)
&=\int_{\mathbb T}\bigl(
 F(u_x)u_{xt}+F(v_x)v_{xt}+(u-v)(u_t-v_t)
 \bigr)\,dx\\
&=\int_{\mathbb T}\bigl(
 [-\partial_xF(u_x)+(u-v)]u_t
 +[-\partial_xF(v_x)-(u-v)]v_t
 \bigr)\,dx.
\end{aligned}
\]
The two equations in the problem say precisely that the two expressions in
square brackets are \(-u_t\) and \(-v_t\), respectively. Hence the exact
dissipation identity is
\[
\boxed{\displaystyle
\frac{d}{dt}\mathcal L(u,v)
=-\int_{\mathbb T}(u_t^2+v_t^2)\,dx.}
\tag{1}
\]

The endpoint relation gives
\[
u_x(x,T)=u_x(x+a,0),\qquad v_x(x,T)=v_x(x+a,0),
\]
and
\[
(u-v)(x,T)=(u-v)(x+a,0),
\]
because the two vertical shifts are equal. Translation invariance of the
integral on \(\mathbb T\) therefore yields
\[
\mathcal L(u(\cdot,T),v(\cdot,T))
=\mathcal L(u(\cdot,0),v(\cdot,0)).
\tag{2}
\]
Integrating (1) from \(0\) to \(T\) and using (2), we obtain
\[
\int_0^T\int_{\mathbb T}(u_t^2+v_t^2)\,dx\,dt=0.
\]
The integrand is continuous and nonnegative, so
\[
u_t=v_t=0\qquad\text{on }\mathbb T\times[0,T].
\tag{3}
\]

It remains to identify the stationary pairs. Write \(w=u-v\). By (3), at
any time in \([0,T]\) the equations reduce to
\[
\partial_xF(u_x)-w=0,
\qquad
\partial_xF(v_x)+w=0.
\tag{4}
\]
Multiply the first equation by \(u\), the second by \(v\), integrate over
\(\mathbb T\), and add. Periodic integration by parts gives
\[
\begin{aligned}
0
&=-\int_{\mathbb T}\left(
F(u_x)u_x+F(v_x)v_x+w(u-v)
\right)\,dx\\
&=-\int_{\mathbb T}\left(
\frac{u_x^2}{\sqrt{1+u_x^2}}
+\frac{v_x^2}{\sqrt{1+v_x^2}}
+(u-v)^2
\right)\,dx.
\end{aligned}
\tag{5}
\]
Every summand in the last integrand is nonnegative. Its integral can vanish
only if
\[
u_x=v_x=0,\qquad u-v=0.
\]
Hence \(u=v=c\) for a common spatial constant, and (3) shows that the same
\(c\) is independent of time on \([0,T]\). If the solution is defined on a
larger forward interval, this conclusion persists there as well: pointwise
\(\sqrt{1+p^2}\ge 1\) gives \(\mathcal L\ge4\pi\), while the common constant
state has \(\mathcal L=4\pi\); applying (1) after time zero forces zero
dissipation for all later times.

Finally, substituting the common constant into the endpoint relation gives
\(c=c+b\), and therefore \(b=0\). There is no restriction on \(a\), since a
spatial translation fixes a constant, and no restriction on \(T\) beyond the
given condition \(T>0\). Conversely, if \(b=0\), any common constant pair
solves the system and satisfies the endpoint relation for every
\(a\in\mathbb T\) and every \(T>0\). This proves both the classification and
its converse. ∎

## Independent consistency check for the vertical shift

Adding the two PDEs and integrating over \(\mathbb T\) shows that
\[
\frac{d}{dt}\int_{\mathbb T}(u+v)\,dx=0.
\]
On the other hand, the endpoint relation changes this conserved integral by
\(4\pi b\). Thus \(4\pi b=0\), independently confirming \(b=0\).
