# The sharp slope-one decay constant

Let

\[
F(p)=p\arctan p,
\qquad
N(f)=\int_{\mathbb T}F(f')\,dx,
\qquad
D(f)=\int_{\mathbb T}f^2\,dx.
\]

We prove

\[
\boxed{\lambda_*=\frac{8}{\pi^2}}
\]

and exhibit an optimizer.

## 1. Reduction to a one-dimensional level-density inequality

Fix a nonconstant admissible \(f\), and write

\[
m=\min_{\mathbb T}f<0<M=\max_{\mathbb T}f.
\]

The strict inequalities follow from continuity, nonconstancy, and the mean-zero condition. Let \(\mu=f_\#(dx)\) be the pushforward of Lebesgue measure under \(f\). By the one-dimensional area formula, the absolutely continuous part of \(\mu\) has, for almost every \(t\in(m,M)\), density

\[
w(t)=\sum_{x\in f^{-1}(t),\ f'(x)\ne0}\frac1{|f'(x)|}.
\]

The remaining part of \(\mu\) is a nonnegative singular measure, denoted by \(2\sigma\): indeed, the area formula implies that the image of \(\{f'=0\}\) has Lebesgue measure zero, and the image of the null set where \(f\) is not differentiable is also null because \(f\) is Lipschitz. The Banach indicatrix formula and the finite total variation of \(f\) show that almost every level has only finitely many crossings. For almost every \(t\in(m,M)\) outside the preceding null sets, periodicity forces at least one upward and one downward crossing, hence at least two. If the nonzero slopes at its preimages are \(p_1,\dots,p_n\), put

\[
r_i=\frac1{|p_i|}\ge1,
\qquad
v(t)=\frac{w(t)}2=\frac12\sum_{i=1}^n r_i\ge1.
\]

The function \(\phi(r)=\arctan(1/r)\) is strictly convex on \([1,\infty)\), since

\[
\phi''(r)=\frac{2r}{(1+r^2)^2}>0.
\]

Consequently,

\[
\sum_{i=1}^n\phi(r_i)
\ge n\phi\!\left(\frac{w(t)}n\right)
=n\arctan\!\left(\frac n{w(t)}\right)
\ge2\arctan\!\left(\frac2{w(t)}\right).
\]

The last inequality holds because \(s\mapsto s\arctan(s/w)\) is strictly increasing for \(s>0\). Applying the area formula once more, and observing that \(F(0)=0\), gives

\[
N(f)\ge 2\int_m^M\arctan(1/v(t))\,dt. \tag{1}
\]

The mass, first moment, and second moment of the pushforward measure give

\[
\int_m^M v(t)\,dt+\sigma([m,M])=\pi, \tag{2}
\]

\[
\int_m^M t v(t)\,dt+\int_{[m,M]}t\,d\sigma(t)=0, \tag{3}
\]

and

\[
\frac{D(f)}2
=\int_m^M t^2v(t)\,dt+\int_{[m,M]}t^2\,d\sigma(t). \tag{4}
\]

In particular, since \(v\ge1\),

\[
M-m\le\int_m^M v(t)\,dt\le\pi. \tag{5}
\]

The singular measure in (2)-(4) includes possible plateaus; hence no strict monotonicity or absence of flat pieces has been assumed.

## 2. A pointwise dual bound

For \(h\ge0\), define

\[
g(h)=\inf_{z\ge1}\left\{\arctan(1/z)+hz\right\}.
\]

Since

\[
\frac{d}{dz}\arctan(1/z)=-\frac1{1+z^2},
\]

the minimization is explicit:

\[
g(h)=
\begin{cases}
\arcsin\sqrt h+\sqrt{h(1-h)},&0\le h\le\tfrac12,\\[2mm]
\dfrac\pi4+h,&h\ge\tfrac12.
\end{cases} \tag{6}
\]

(At \(h=0\), the displayed value is the limiting infimum.) Put

\[
\lambda=\frac8{\pi^2},
\qquad
h(t)=\lambda(t-m)(M-t)\quad(m\le t\le M).
\]

Thus \(h\ge0\). From (2)-(4),

\[
\begin{aligned}
\int_{[m,M]}h(t)\bigl(v(t)\,dt+d\sigma(t)\bigr)
&=-\lambda\left(\int_m^M t^2v(t)\,dt+\int t^2\,d\sigma(t)\right)-\lambda\pi mM,
\end{aligned} \tag{7}
\]

because the linear term vanishes by (3). Combining (1), (6), and (7), and then dropping the nonnegative integral of \(h\) against \(\sigma\), yields

\[
\frac{N(f)-\lambda D(f)}2
\ge \int_m^M g\bigl(\lambda(t-m)(M-t)\bigr)\,dt+\lambda\pi mM. \tag{8}
\]

It remains to prove that the right-hand side is nonnegative.

## 3. The scalar calculus lemma

Define

\[
H(c)=\int_0^1g\bigl(c(1-x^2)\bigr)\,dx.
\]

We need the following sharp lemma.

**Lemma.** For every \(c>0\),

\[
H(c)\ge\sqrt{2c}, \tag{9}
\]

with equality if and only if \(c=1\).

**Proof.** Away from the immaterial transition point where \(c(1-x^2)=1/2\), let

\[
V_c(x)=g'\bigl(c(1-x^2)\bigr)
=
\begin{cases}
1,&c(1-x^2)\ge\tfrac12,\\[1mm]
\sqrt{\dfrac{1-c+cx^2}{c(1-x^2)}},&c(1-x^2)<\tfrac12.
\end{cases} \tag{10}
\]

The endpoint singularity in \(V_c\) is integrable. More explicitly, with \(c\) restricted to any compact subinterval of \((0,\infty)\), on the uncapped region

\[
(1-x^2)V_c(x)
=\sqrt{\frac{(1-x^2)(1-c(1-x^2))}{c}}
\le C\sqrt{1-x^2},
\]

while on the capped region it is at most \(1-x^2\). This supplies an integrable local majorant for differentiation under the integral. Moreover, \(x\mapsto g(c(1-x^2))\) is absolutely continuous, because its derivative \(-2cxV_c(x)\) is \(O((1-x)^{-1/2})\) near \(x=1\). Thus the following differentiation and integration by parts are legitimate.

Differentiation under the integral and integration by parts give

\[
H'(c)=\int_0^1(1-x^2)V_c(x)\,dx,
\qquad
H(c)=2c\int_0^1x^2V_c(x)\,dx. \tag{11}
\]

Therefore

\[
\left(\frac{H(c)}{\sqrt c}\right)'
=\frac1{\sqrt c}I(c),
\qquad
I(c)=\int_0^1(1-2x^2)V_c(x)\,dx. \tag{12}
\]

We show that \(I(c)<0\) for \(c<1\), \(I(1)=0\), and \(I(c)>0\) for \(c>1\).

First suppose \(0<c\le1/2\). There is no capped interval of positive length in (10). Setting \(x=\sin\theta\), and pairing \(\theta\) with \(\pi/2-\theta\), gives

\[
\begin{aligned}
I(c)
&=\frac1{\sqrt c}\int_0^{\pi/2}\cos(2\theta)\sqrt{1-c\cos^2\theta}\,d\theta\\
&=\frac1{\sqrt c}\int_0^{\pi/4}\cos(2\theta)
\left(\sqrt{1-c\cos^2\theta}-\sqrt{1-c\sin^2\theta}\right)d\theta<0. \tag{13}
\end{aligned}
\]

Now suppose \(1/2<c\le9/16\). Let \(\widetilde V_c\) denote the square-root expression in (10) on the whole interval and let \(\widetilde I(c)=\int_0^1(1-2x^2)\widetilde V_c(x)\,dx\). Rationalizing the difference in (13) gives

\[
-\widetilde I(c)
=\sqrt c\int_0^{\pi/4}
\frac{\cos^2(2\theta)}{\sqrt{1-c\cos^2\theta}+\sqrt{1-c\sin^2\theta}}\,d\theta
\ge\frac{\pi\sqrt c}{16}. \tag{14}
\]

The capped interval is \([0,a]\), where \(a=\sqrt{1-1/(2c)}\le1/3\). On it, \(1-2x^2>0\), \(\widetilde V_c\) is increasing, and hence

\[
0\le I(c)-\widetilde I(c)
\le a\left(1-\sqrt{\frac{1-c}{c}}\right)
\le\frac{3-\sqrt7}{9}<\frac1{18}. \tag{15}
\]

On the other hand, \(\pi\sqrt c/16\ge\pi/(16\sqrt2)>1/8\). Equations (14)-(15) imply \(I(c)<0\).

It remains to treat \(9/16\le c<1\). Put

\[
a=\sqrt{1-\frac1{2c}},
\qquad
r=\frac1{\sqrt2},
\qquad
P=r-\frac23r^3=\frac{\sqrt2}{3},
\qquad
Q(x)=x-\frac23x^3.
\]

Here \(1/3\le a<r\). On \([0,a]\), \(V_c=1\). On \([a,r]\), both \(1-2x^2\ge0\) and

\[
V_c(x)\le K:=\sqrt{\frac2c-1}.
\]

On \([r,1]\), \(1-2x^2\le0\) and

\[
V_c(x)\ge\frac1{\sqrt c}V_1(x).
\]

Since \(\int_r^1(1-2x^2)V_1(x)\,dx=-P\), these estimates imply

\[
I(c)\le (1-K)Q(a)+\left(K-\frac1{\sqrt c}\right)P. \tag{16}
\]

Both \(K>1/\sqrt c>1\), and rationalization gives

\[
\frac{K-1/\sqrt c}{K-1}
=\frac{K+1}{2(K+1/\sqrt c)}<\frac12. \tag{17}
\]

Moreover, \(Q\) is increasing on \([1/3,r]\), and

\[
\frac{Q(a)}P\ge\frac{Q(1/3)}P=\frac{25}{27\sqrt2}>\frac12. \tag{18}
\]

Equations (16)-(18) show \(I(c)<0\).

At \(c=1\), formula (10) becomes

\[
V_1(x)=
\begin{cases}
1,&0\le x\le r,\\
\dfrac{x}{\sqrt{1-x^2}},&r<x<1.
\end{cases}
\]

Direct integration gives

\[
I(1)=0,
\qquad
\int_0^1V_1(x)\,dx=\sqrt2. \tag{19}
\]

By (11) and (19), \(H(1)=\sqrt2\).

Finally, if \(c>1\), then \(V_c=V_1=1\) on \([0,r]\), while \(V_c\le V_1\) on \([r,1]\), with strict inequality on a set of positive measure. Since \(1-2x^2<0\) there, (19) gives \(I(c)>I(1)=0\). Thus \(H(c)/\sqrt c\) strictly decreases up to \(c=1\) and strictly increases afterwards. Its minimum is \(H(1)=\sqrt2\), proving (9). \(\square\)

## 4. Completion of the lower bound

Let

\[
L=M-m,
\qquad
\rho=-\frac mL\in(0,1),
\qquad
c=\frac{\lambda L^2}{4}.
\]

Changing variables first by \(t=m+Lz\) and then by \(x=2z-1\) gives

\[
\int_m^M g\bigl(\lambda(t-m)(M-t)\bigr)\,dt=L H(c). \tag{20}
\]

Also \(mM=-\rho(1-\rho)L^2\), so (8), (20), and \(\rho(1-\rho)\le1/4\) yield

\[
\frac{N(f)-\lambda D(f)}2
\ge L H(c)-\frac{\lambda\pi L^2}{4}.
\]

Because \(\lambda=8/\pi^2\) and \(c=\lambda L^2/4\),

\[
\frac{\lambda\pi L}{4}=\sqrt{2c}.
\]

The scalar lemma therefore gives

\[
N(f)-\frac8{\pi^2}D(f)\ge0. \tag{21}
\]

Thus \(\lambda_*\ge8/\pi^2\).

## 5. An optimizer and sharpness

Set

\[
A=\frac{\pi}{2\sqrt2},
\qquad
b=\frac\pi4=\frac A{\sqrt2}.
\]

Define \(f_*\) on \([0,\pi]\) by

\[
f_*(x)=
\begin{cases}
\sqrt{A^2-x^2},&0\le x\le b,\\[1mm]
\dfrac\pi2-x,&b\le x\le\pi-b,\\[1mm]
-\sqrt{A^2-(\pi-x)^2},&\pi-b\le x\le\pi,
\end{cases} \tag{22}
\]

and extend it by \(f_*(x+\pi)=-f_*(x)\). The values and first derivatives match at the two junctions; hence \(f_*\in W^{1,\infty}(\mathbb T)\), and \(\|f_*'\|_\infty=1\). Its anti-periodicity gives mean zero.

For a positive normalized level \(y=t/A\), its inverse-level density is

\[
v_*(y)=
\begin{cases}
1,&0\le y\le1/\sqrt2,\\[1mm]
\dfrac{y}{\sqrt{1-y^2}},&1/\sqrt2<y<1.
\end{cases}
\]

Writing \(r=1/\sqrt2\), the two elementary integrals needed are

\[
\int_0^1\arctan(1/v_*(y))\,dy=\frac1{\sqrt2},
\qquad
\int_0^1y^2v_*(y)\,dy=\frac1{\sqrt2}. \tag{23}
\]

Indeed, on \([r,1]\) one has \(\arctan(1/v_*)=\arccos y\), and therefore

\[
r\frac\pi4+\int_r^1\arccos y\,dy
=r\frac\pi4+r\left(1-\frac\pi4\right)=r.
\]

Also, by the substitution \(u=1-y^2\),

\[
\frac{r^3}{3}+\int_r^1\frac{y^3}{\sqrt{1-y^2}}\,dy
=\frac{r^3}{3}+r-\frac{r^3}{3}=r.
\]

There are exactly two preimages of each regular level, so the coarea formulas are equalities. Using symmetry in the level variable and (23),

\[
N(f_*)=4A\cdot\frac1{\sqrt2}=\pi,
\qquad
D(f_*)=4A^3\cdot\frac1{\sqrt2}=\frac{\pi^3}{8}. \tag{24}
\]

Therefore

\[
\frac{N(f_*)}{D(f_*)}=\frac8{\pi^2}.
\]

Together with (21), this proves

\[
\boxed{\lambda_*=\frac8{\pi^2}=0.810569469138702\ldots}.
\]

For completeness, the equality conditions also identify all optimizers. Equality in \(\rho(1-\rho)\le1/4\) and in the scalar lemma forces

\[
m=-A,\qquad M=A,\qquad c=1.
\]

Equality in the pointwise minimization (6) then forces

\[
v(t)=
\begin{cases}
1,&|t|\le A/\sqrt2,\\[1mm]
\dfrac{|t|}{\sqrt{A^2-t^2}},&A/\sqrt2<|t|<A.
\end{cases} \tag{25}
\]

The integral of (25) over \((-A,A)\) is already \(\pi\), so (2) forces \(\sigma=0\). Strictness in the two levelwise convexity inequalities in Section 1 forces exactly two crossings, with equal slope magnitudes, at almost every level. A continuous circle map with exactly two preimages at almost every intermediate level has one increasing and one decreasing branch between its extrema: any additional turn would give at least four preimages throughout a nonempty interval of levels. Since \(\sigma=0\), neither inverse branch has a singular length part. On the decreasing branch, (25) therefore gives

\[
x=\int_t^A v(s)\,ds=\sqrt{A^2-t^2}
\]

until \(t=A/\sqrt2\), followed by a slope-\(-1\) segment; the negative circular arc follows in the same way. Thus, apart from translation and multiplication by \(-1\), the optimizer is exactly (22).
