# A Coupled H^{-1} Gradient Flow - complete proof

All five assertions are true. Throughout, spatial integrals are normalized by
`1/(2 pi)`, and constants may change from line to line. Vector-valued Sobolev
norms are understood componentwise.

## 1. Vector form and local well-posedness

Put

\[
 w=\binom uv,\qquad
 K=\begin{pmatrix}1&-1\\-1&1\end{pmatrix},\qquad
 N(w)=Kw+|w|^2w.
\]

Then the system is

\[
 w_t+\partial_x^4w=\partial_x^2N(w). \tag{12}
\]

We first record the standard linear estimate which is needed below. If

\[
 z_t+\partial_x^4z=f,\qquad z(0)=z_0,
\]

and `z_0` and `f` have zero spatial mean, then

\[
 \|z\|_{C([0,T];H^2)}+\|z\|_{L^2(0,T;H^4)}
 +\|z_t\|_{L^2(0,T;L^2)}
 \leq C\bigl(\|z_0\|_{H^2}+\|f\|_{L^2(0,T;L^2)}\bigr), \tag{13}
\]

For completeness, this follows directly by taking Fourier coefficients. For
each nonzero mode,

\[
 \dot z_n+n^4z_n=f_n.
\]

Multiplication by `n^4 \overline{z_n}`, summation, and Young's inequality give
the `C H^2` and `L^2 H^4` bounds; the equation then gives the `L^2 L^2`
bound for `z_t`. On mean-zero functions, the corresponding homogeneous and
inhomogeneous Sobolev norms are equivalent. The same modewise calculation
also gives continuity into `H^2`. In particular, the constant in (13) can be
taken independent of `T`, which is what the contraction argument below uses.

In one dimension, `H^2(T)` is a Banach algebra. Consequently, on every
`H^2` ball of radius `R`,

\[
 \|\partial_x^2N(a)-\partial_x^2N(b)\|_{L^2}
 \leq C_R\|a-b\|_{H^2}. \tag{14}
\]

Applying (13) to the Duhamel map associated with (12), (14) supplies a factor
`T^{1/2}` in `L^2(0,T;L^2)`. Thus, for sufficiently small `T`, that map is a
contraction on a ball in

\[
 X_T=C([0,T];H^2)^2\cap L^2(0,T;H^4)^2
       \cap H^1(0,T;L^2)^2. \tag{15}
\]

This proves local existence and uniqueness in precisely the class asserted
in (6)-(7). It also gives the continuation criterion

\[
 T_*<\infty\quad\Longrightarrow\quad
 \limsup_{t\uparrow T_*}\|w(t)\|_{H^2}=\infty. \tag{16}
\]

Integrating (12) in space shows that the mean of each component is conserved.
In particular, both components remain mean zero.

## 2. Energy identity and global continuation

The first variation of the energy is

\[
 \mathcal E'(w)h=\langle \mu(w)\mathbin{\cdot}h\rangle,
 \qquad
 \mu(w)=-w_{xx}+Kw+|w|^2w. \tag{17}
\]

The regularity in (15) justifies the Sobolev chain rule and periodic
integration by parts. Hence, for almost every time in the local interval,

\[
 \frac{d}{dt}\mathcal E(w(t))
 =\langle\mu\mathbin{\cdot}w_t\rangle
 =\langle\mu\mathbin{\cdot}\partial_x^2\mu\rangle
 =-\langle|\partial_x\mu_u|^2+|\partial_x\mu_v|^2\rangle. \tag{18}
\]

Indeed, in (15) one has `\mu in L^2(0,T;H^2)^2`, so every term above lies in
`L^1(0,T)`. The energy is absolutely continuous. Integrating (18) therefore
gives, for every time for which the solution exists,

\[
 \mathcal E(t)+\int_0^t
 \langle|\partial_x\mu_u|^2+|\partial_x\mu_v|^2\rangle\,d\tau
 =\mathcal E(0). \tag{19}
\]

It remains to exclude finite-time loss of `H^2`. Let
`S_0(t)=\exp(-t\partial_x^4)`. A Fourier-multiplier estimate gives

\[
 \|S_0(s)\partial_x^2 f\|_{H^2}
 \leq C s^{-3/4}\|f\|_{H^1},\qquad s>0. \tag{20}
\]

The exponent follows from
`\sup_{n\ne0}|n|^3\exp(-n^4s)\leq Cs^{-3/4}`.
By mean-zero Poincare and (19),

\[
 \sup_{t<T_*}\|w(t)\|_{H^1}
 \leq C\mathcal E(0)^{1/2}=:M. \tag{21}
\]

Since `H^1(T)` is also a Banach algebra,

\[
 \|N(w(t))\|_{H^1}\leq C(M+M^3). \tag{22}
\]

The mild form of (12), (20), and (22) yield, for every `t<T_*`,

\[
 \begin{aligned}
 \|w(t)\|_{H^2}
 &\leq \|w_0\|_{H^2}
 +C(M+M^3)\int_0^t(t-s)^{-3/4}\,ds\\
 &\leq \|w_0\|_{H^2}+C(M+M^3)t^{1/4}. \tag{23}
 \end{aligned}
\]

This is bounded on every finite interval and contradicts (16) if `T_*` is
finite. Thus the solution is global. Applying the local maximal-regularity
result on successive bounded intervals proves (6)-(7) globally in the stated
local-in-time sense. This proves assertion 1, while (19) proves assertion 3.

## 3. Local Lipschitz dependence in H^2

Fix `T<\infty` and an `H^2`-bounded neighborhood of initial data. The
energies of those data are uniformly bounded, so (21)-(23) give a number
`R_T` such that every corresponding solution satisfies

\[
 \sup_{0\leq t\leq T}\|w(t)\|_{H^2}\leq R_T. \tag{24}
\]

For two such solutions, set `z=w-\widetilde w`. On the ball in (24), the
algebra estimate gives

\[
 \|N(w)-N(\widetilde w)\|_{H^2}
 \leq C_{R_T}\|z\|_{H^2}. \tag{25}
\]

Another Fourier-multiplier estimate is

\[
 \|S_0(s)\partial_x^2 f\|_{H^2}
 \leq Cs^{-1/2}\|f\|_{H^2}. \tag{26}
\]

Thus Duhamel's formula implies

\[
 \|z(t)\|_{H^2}\leq \|z(0)\|_{H^2}
 +C_{R_T}\int_0^t(t-s)^{-1/2}\|z(s)\|_{H^2}\,ds. \tag{27}
\]

The fractional Gronwall inequality now gives

\[
 \sup_{0\leq t\leq T}\|z(t)\|_{H^2}
 \leq C_{R_T,T}\|z(0)\|_{H^2}. \tag{28}
\]

One can see this without invoking a black box: substitute (27) into itself
once and use

\[
 \int_s^t(t-r)^{-1/2}(r-s)^{-1/2}\,dr=\pi;
\]

ordinary Gronwall then proves (28). This is assertion 2 on the mean-zero
initial-data subspace specified in the problem. If the phrase "from
`H^2\times H^2`" is instead read as including nonzero means, the same proof
works: on the finite-measure torus the quartic term controls `\|w\|_{L^2}`
through `\|w\|_{L^4}`, while the quadratic gradient term controls `w_x`, so
bounded initial energy still gives the uniform `H^1` bound used in (23)-(24).

## 4. Exact energy decay

Let `\dot H^{-1}(T)` denote the mean-zero `H^{-1}` space. For a mean-zero
vector `h`, define

\[
 \|h\|_{-1}^2
 :=\left\langle h\mathbin{\cdot}(-\partial_x^2)^{-1}h\right\rangle.
\]

The second variation of the energy is

\[
 \mathcal E''(w)[h,h]
 =\left\langle
 |h_x|^2+|h_1-h_2|^2+|w|^2|h|^2+2(w\mathbin{\cdot}h)^2
 \right\rangle. \tag{29}
\]

All terms after the first are nonnegative. Also, by Fourier series,

\[
 \langle|h_x|^2\rangle
 =\sum_{n\ne0}n^2|h_n|^2
 \geq\sum_{n\ne0}n^{-2}|h_n|^2
 =\|h\|_{-1}^2. \tag{30}
\]

Thus `\mathcal E` is `1`-strongly convex in the `H^{-1}` metric. Taylor's
formula along the segment from `w` to zero gives

\[
 \mathcal E(w)
 \leq \langle\mu(w)\mathbin{\cdot}w\rangle
       -\frac12\|w\|_{-1}^2. \tag{31}
\]

At almost every solution time, `\mu_x in L^2`. If
`p=(-\partial_x^2)^{-1}w`, periodic integration by parts and Cauchy-Schwarz
give

\[
 \langle\mu\mathbin{\cdot}w\rangle
 =\langle\mu_x\mathbin{\cdot}p_x\rangle
 \leq D(w)^{1/2}\|w\|_{-1}, \tag{32}
\]

where

\[
 D(w):=\langle|\partial_x\mu_u|^2+|\partial_x\mu_v|^2\rangle.
\]

Combining (31)-(32) and maximizing
`D^{1/2}r-r^2/2` over `r\geq0` proves the sharp
Polyak-Lojasiewicz inequality

\[
 D(w)\geq2\mathcal E(w). \tag{33}
\]

There is also a useful independent check of the constant in (33). Set

\[
 A=\left\langle\frac{|w_x|^2+|u-v|^2}{2}\right\rangle,
 \qquad B=\left\langle\frac{|w|^4}{4}\right\rangle.
\]

Then `\mathcal E=A+B` and
`\langle\mu\mathbin{\cdot}w\rangle=2A+4B`. Moreover,
`\|w\|_{-1}^2\leq\langle|w_x|^2\rangle\leq2A`. Thus dual
Cauchy-Schwarz gives, when `w\ne0`,

\[
 D\geq\frac{(2A+4B)^2}{\|w\|_{-1}^2}
 \geq\frac{(2A+4B)^2}{2A}
 =2\frac{(A+2B)^2}{A}\geq2(A+B).
\]

The last inequality is equivalent to `3AB+4B^2\geq0`; the case `w=0` is
immediate. This reproduces (33) without the strong-convexity argument.

Equations (18) and (33) imply

\[
 \frac{d}{dt}\mathcal E(t)\leq-2\mathcal E(t)
\]

almost everywhere. Therefore

\[
 \boxed{\mathcal E(t)\leq e^{-2t}\mathcal E(0)} \tag{34}
\]

with prefactor exactly one.

The exponent is sharp. First, a short local-in-time test already proves
sharpness for prefactor one. Take

\[
 u_0=v_0=\varepsilon\cos x.
\]

A direct calculation gives

\[
 \mathcal E(0)=\frac{\varepsilon^2}{2}
                 +\frac{3\varepsilon^4}{8},\qquad
 D(0)=\varepsilon^2+3\varepsilon^4+\frac92\varepsilon^6. \tag{35}
\]

Hence `D(0)/\mathcal E(0)\to2` as `\varepsilon\to0`. If (34) held with any
uniform exponent `alpha>2`, differentiating it at `t=0` for these smooth data
would force `D(0)\geq alpha\mathcal E(0)`, contradicting (35) for small
`\varepsilon`.

In fact the exponent is sharp even asymptotically. By uniqueness, the
subspace `u=v=q` is invariant, and there

\[
 q_t=-q_{xxxx}+2\partial_x^2(q^3). \tag{36}
\]

Let `P_1` be the orthogonal projection onto the first Fourier eigenspace.
Duhamel's formula gives

\[
 e^tP_1q(t)=P_1q_0-2\int_0^t e^sP_1(q(s)^3)\,ds. \tag{37}
\]

For `q_0=\varepsilon\cos x`, (34) and Poincare imply
`\|q(s)\|_{H^1}\leq C|\varepsilon|e^{-s}` when `|\varepsilon|\leq1`.
The integral in (37) therefore converges, and its norm is at most

\[
 C\int_0^\infty e^s\|q(s)\|_{H^1}^3\,ds\leq C|\varepsilon|^3. \tag{38}
\]

For all sufficiently small nonzero `\varepsilon`, the limit of
`e^tP_1q(t)` is consequently nonzero. Since
`\mathcal E(q,q)\geq\langle|q_x|^2\rangle`, this gives
`\mathcal E(t)\geq c_\varepsilon e^{-2t}` for all sufficiently large `t`.
Thus no exponent larger than `2` is a uniform decay exponent, even if one
allows a finite data-dependent prefactor. This completes assertion 4.

## 5. H^2 decay

Now absorb the linear coupling into

\[
 L=-\partial_x^4+K\partial_x^2.
\]

The eigenvalues of `K` are `0` and `2`. On a nonzero Fourier mode `n`, the
eigenvalues of `L` are therefore

\[
 -n^4\quad\hbox{and}\quad-(n^4+2n^2). \tag{39}
\]

It follows that, on mean-zero functions,

\[
 \|e^{sL}f\|_{H^2}\leq e^{-s}\|f\|_{H^2}, \tag{40}
\]

and

\[
 \|e^{sL}\partial_x^2f\|_{H^2}
 \leq Ce^{-s}(1+s^{-3/4})\|f\|_{H^1}. \tag{41}
\]

Again (41) is a direct Fourier estimate: after factoring out `e^{-s}`, the
relevant multiplier is bounded by
`C(1+s^{-3/4})`.

From (34), mean-zero Poincare, and the `H^1` algebra property,

\[
 \|w(s)\|_{H^1}\leq C\mathcal E(0)^{1/2}e^{-s},
 \qquad
 \||w(s)|^2w(s)\|_{H^1}
 \leq C\mathcal E(0)^{3/2}e^{-3s}. \tag{42}
\]

Fix `s_0=1/2`. Global well-posedness gives
`w(s_0) in H^2`. Duhamel's formula, now with the generator `L`, yields for
`t\geq1`

\[
 \begin{aligned}
 \|w(t)\|_{H^2}
 &\leq e^{-(t-s_0)}\|w(s_0)\|_{H^2}\\
 &\quad+C\mathcal E(0)^{3/2}
 \int_{s_0}^t e^{-(t-s)}(1+(t-s)^{-3/4})e^{-3s}\,ds. \tag{43}
 \end{aligned}
\]

The integral is at most `Ce^{-t}`: after taking out `e^{-t}`, the remaining
integral

\[
 \int_{s_0}^t(1+(t-s)^{-3/4})e^{-2s}\,ds
\]

is bounded uniformly for `t\geq1` (split it into `s\leq t-1` and
`s\geq t-1`). Thus

\[
 \|w(t)\|_{H^2}\leq C(w_0)e^{-t},\qquad t\geq1. \tag{44}
\]

Finally,
`\|u(t)\|_{H^2}+\|v(t)\|_{H^2}\leq\sqrt2\|w(t)\|_{H^2}`,
so (44) is exactly assertion 5.

All five assertions are proved.
