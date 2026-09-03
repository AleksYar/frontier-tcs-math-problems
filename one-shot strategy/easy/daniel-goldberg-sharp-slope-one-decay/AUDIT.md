# Adversarial audit of `PROOF.md`

- Audit started: Unix time `1787777838` (2026-08-26, Europe/Paris).
- Source checked: the complete one-page PDF and the current on-disk version of
  `PROOF.md` (including the later additions concerning null critical images and
  equality reconstruction).
- Claimed result: \(\lambda_*=8/\pi^2\).

## Verdict

**No fatal gap or counterexample was found.** The proof of
\(\lambda_*=8/\pi^2\) is correct. I independently checked the measure/coarea
reduction for arbitrary periodic \(W^{1,\infty}\) functions, every factor of
two, the dual algebra, all ranges of the scalar lemma, the optimizer, and the
two exact integrals.

The two terse points identified below under "Repairable presentation gaps"
have standard short justifications and do not affect correctness. They would
only be worth expanding if the intended audience requires every analytic
regularity detail and the uniqueness assertion to be completely self-contained.

## Fatal gaps

None.

## Repairable presentation gaps (nonfatal)

1. **Differentiation and integration by parts in (11) are terse.** The endpoint
   \(x=1\) has \(g'(c(1-x^2))\to\infty\), so it is not literally enough to say
   the transition point is immaterial. The formulas are nevertheless valid.
   For \(c\) in a compact subinterval of \((0,\infty)\), on the uncapped region,
   \[
   (1-x^2)V_c(x)
   =\sqrt{\frac{(1-x^2)(1-c(1-x^2))}{c}}
   \le C\sqrt{1-x^2},
   \]
   while on the capped region it is at most \(1-x^2\). This supplies an
   integrable local dominating function for differentiating \(H\). Likewise
   \(x\mapsto g(c(1-x^2))\) is absolutely continuous: its derivative is
   \(-2cxV_c(x)=O((1-x)^{-1/2})\) near \(1\). Hence the integration by parts in
   (11) is legitimate. Adding these two sentences would remove the only
   analytic regularity omission in the scalar lemma.

2. **The final uniqueness reconstruction suppresses one topological sentence.**
   From exactly two preimages for almost every level, a continuous circle map
   with range \([-A,A]\) has one decreasing and one increasing branch between
   its extrema; any additional turn would create at least four preimages on a
   nonempty interval of levels. Since \(\sigma=0\), neither branch has a
   singular inverse-length part. Equal reciprocal slopes then make the inverse
   length on each branch exactly \(\int v\). This justifies the phrase "on a
   decreasing branch" and completes the classification. The value and
   existence proof do not depend on uniqueness, and the assertion itself is
   correct.

## Detailed verification

### 1. Statement and normalizations

The PDF defines \(\mathbb T=\mathbb R/(2\pi\mathbb Z)\), imposes mean zero and
\(\|f'\|_\infty\le1\), and minimizes
\[
\frac{\int_{\mathbb T}f'\arctan(f')\,dx}
     {\int_{\mathbb T}f^2\,dx}
\]
over nonzero functions. `PROOF.md` uses exactly this normalization. The claimed
number satisfies the PDF's certified bracket:
\[
\frac\pi4=0.785398\ldots
<\frac8{\pi^2}=0.810569\ldots
<2(\sqrt2-1)=0.828427\ldots.
\]

Mean zero and nonconstancy do imply \(m<0<M\), so no endpoint sign case was
lost.

### 2. Pushforward measure for arbitrary Lipschitz functions

Let \(E=\{x:f'(x)\text{ exists and }f'(x)\ne0\}\). Applying the one-dimensional
area formula to \(1_E/|f'|\) gives
\[
(f_\#(1_Edx))(dt)
=\left(\sum_{x\in E\cap f^{-1}(t)}\frac1{|f'(x)|}\right)dt.
\]
The differentiability exceptional set has zero measure and its image is null
because a Lipschitz map has property \(N\). For the differentiable critical set
\(Z=\{f'=0\}\), the area formula gives
\(\int \#(Z\cap f^{-1}(t))dt=\int_Z|f'|dx=0\), hence \(f(Z)\) is null. Thus the
remaining pushforward is singular. This validates the decomposition
\[
f_\#dx=2v(t)dt+2\sigma.
\]

The Banach indicatrix formula gives
\(\int \# f^{-1}(t)dt=\int|f'|dx<\infty\), so almost every regular level has
finitely many preimages. For every level strictly between the minimum and
maximum, the two arcs of the circle joining a minimum to a maximum each contain
a preimage. Outside the images of the exceptional and critical sets, these are
genuine nonzero-slope crossings. Therefore \(n\ge2\) almost everywhere. This
remains valid for flat plateaus, infinitely many oscillations, and pathological
positive-measure critical sets.

### 3. Numerator and the factor of two

At a nonzero-slope preimage with \(r=1/|p|\),
\[
\frac{F(p)}{|p|}=\frac{p\arctan p}{|p|}
=\arctan|p|=\arctan(1/r).
\]
The set \(f'=0\) contributes zero because \(F(0)=0\). Thus the area formula gives
an equality before Jensen:
\[
N(f)=\int_m^M\sum_{i=1}^{n(t)}\arctan(1/r_i(t))\,dt.
\]
Strict convexity of \(\phi(r)=\arctan(1/r)\) yields
\[
\sum_i\phi(r_i)\ge n\arctan(n/w),
\]
and \(s\mapsto s\arctan(s/w)\) has derivative
\[
\arctan(s/w)+\frac{sw}{w^2+s^2}>0.
\]
Since \(n\ge2\), this proves (1). There is no missing orientation sign because
\(p\arctan p\) is even.

The normalization \(w=2v\) and singular part \(2\sigma\) is consistent with
the circle length \(2\pi\):
\[
\int vdt+\sigma=\pi,
\quad
\int tvdt+\int t\,d\sigma=0,
\quad
D/2=\int t^2vdt+\int t^2d\sigma.
\]
As a check, for \(f(x)=\sin x\), \(v(t)=1/\sqrt{1-t^2}\), and the last identity
gives \(D=2\int_{-1}^1t^2/\sqrt{1-t^2}\,dt=\pi\), the correct full-period
denominator.

### 4. Pointwise minimization and dual identity

For \(\phi(z)=\arctan(1/z)\),
\(\phi'(z)=-1/(1+z^2)\). If \(0<h<1/2\), the unique minimizer of
\(\phi(z)+hz\) over \(z\ge1\) is
\(z=\sqrt{1/h-1}\), giving
\[
g(h)=\arcsin\sqrt h+\sqrt{h(1-h)}.
\]
For \(h\ge1/2\), the minimizer is \(z=1\), giving \(g(h)=\pi/4+h\). At
\(h=0\), the infimum is the limit \(0\). Thus (6) is exact.

Expanding
\[
h(t)=\lambda[-t^2+(m+M)t-mM]
\]
and using mass \(\pi\), first moment \(0\), and second moment \(D/2\) gives
\[
\int h(vdt+d\sigma)=-\lambda D/2-\lambda\pi mM,
\]
with both signs and the factor \(1/2\) correct. Consequently
\[
\begin{aligned}
(N-\lambda D)/2
&\ge\int(\phi(v)+hv)dt+\int h\,d\sigma+\lambda\pi mM\\
&\ge\int g(h)dt+\lambda\pi mM,
\end{aligned}
\]
because \(h\ge0\). This is precisely (8).

### 5. Scalar lemma

Differentiating the two branches of \(g\) gives
\[
g'(h)=1\quad(h\ge1/2),
\qquad
g'(h)=\sqrt{(1-h)/h}\quad(0<h<1/2),
\]
so (10) is correct. With the analytic endpoint justification noted above,
integration by parts yields
\[
H'=\int(1-x^2)V_c,
\qquad
H=2c\int x^2V_c,
\]
and therefore the derivative in (12) has exactly the sign of
\(I(c)=\int(1-2x^2)V_c\).

I checked every range in the sign argument:

- For \(0<c\le1/2\), after \(x=\sin\theta\), pairing \(\theta\) and
  \(\pi/2-\theta\) gives the displayed negative integrand in (13). It is
  strictly negative on \((0,\pi/4)\).

- For \(1/2<c\le9/16\), rationalization gives (14) exactly. Since each square
  root in its denominator is at most \(1\),
  \(\int_0^{\pi/4}\cos^2(2\theta)d\theta=\pi/8\), and hence the lower bound is
  \(\pi\sqrt c/16\). The cap endpoint satisfies \(a\le1/3\), and both factors in
  \(a(1-\sqrt{(1-c)/c})\) increase with \(c\), giving the endpoint value
  \((3-\sqrt7)/9<1/18\). Since \(\pi/(16\sqrt2)>1/8\), the negative uncapped
  contribution dominates.

- For \(9/16\le c<1\), \(Q'(x)=1-2x^2\ge0\) up to
  \(r=1/\sqrt2\). On \([a,r]\), monotonicity of the square-root branch gives
  \(V_c\le V_c(r)=K\). On \([r,1]\), direct squaring gives
  \[
  V_c(x)^2-\frac1cV_1(x)^2=\frac{1-c}{c}\ge0,
  \]
  so the sign reversal caused by \(1-2x^2\le0\) is handled correctly. Also
  \[
  \int_r^1(1-2x^2)V_1(x)dx=-\frac{\sqrt2}{3}=-P.
  \]
  These facts give (16). The rationalization in (17) is exact, and
  \(25/(27\sqrt2)>1/2\), so its positive term is strictly smaller than its
  negative term.

- At \(c=1\),
  \[
  \int_0^r(1-2x^2)dx=P,
  \quad
  \int_r^1(1-2x^2)\frac{x}{\sqrt{1-x^2}}dx=-P,
  \]
  hence \(I(1)=0\). Moreover
  \[
  \int_0^1V_1dx=r+\sqrt{1-r^2}=\sqrt2.
  \]
  From \(I(1)=0\) and (11), \(H(1)=\sqrt2\).

- For \(c>1\), the cap of \(V_c\) extends past \(r\), and
  \(V_c\le V_1\) on \([r,1]\), strictly on a set of positive measure. On the
  uncapped portion this follows from
  \[
  V_1^2-V_c^2=\frac{c-1}{c(1-x^2)}>0.
  \]
  Multiplication by the negative weight \(1-2x^2\) reverses the comparison,
  proving \(I(c)>0\).

Thus \(H(c)/\sqrt c\) has its unique global minimum at \(c=1\), and (9) is
fully verified. An independent endpoint-regularized numerical integration at
\(c=0.001,0.01,0.1,0.49,0.50001,0.55,9/16,0.8,0.99,1,1.01,2,10,100\) agreed
with the strict signs and equality at \(1\); this was only a falsification check,
not used as proof.

### 6. Completion and asymmetry

With \(L=M-m\), \(t=m+Lz\), and \(x=2z-1\),
\[
h=c(1-x^2),\qquad dt=(L/2)dx,
\]
and evenness in \(x\) gives \(\int_m^Mg(h)dt=LH(c)\), with no missing factor
of two. Since \(mM=-\rho(1-\rho)L^2\) and
\(\rho(1-\rho)\le1/4\), asymmetry can only increase the lower bound. Finally,
\[
\sqrt{2c}=L\sqrt{\lambda/2}=\frac{\lambda\pi L}{4}
\quad\text{when }\lambda=8/\pi^2.
\]
Therefore
\((N-\lambda D)/2\ge L[H(c)-\sqrt{2c}]\ge0\). The lower bound is valid for
every admissible nonzero function.

### 7. Optimizer and exact integrals

For \(A=\pi/(2\sqrt2)\) and \(b=A/\sqrt2=\pi/4\), the values at each junction
in (22) are \(\pm b\), and the one-sided derivatives are all \(-1\). The arc
slopes range from \(0\) to \(-1\). At \(x=0,\pi\) the derivative is \(0\), so
the anti-periodic extension is \(C^1\) there as well. Hence the extension is
\(2\pi\)-periodic, lies in \(W^{1,\infty}\), and has slope norm \(1\). Its
anti-periodicity makes its mean exactly zero.

For \(y=t/A\), the two reciprocal slopes agree and equal
\[
v_*(y)=1\ (0\le y\le r),
\qquad
v_*(y)=\frac{y}{\sqrt{1-y^2}}\ (r<y<1).
\]
The first exact integral is
\[
r\frac\pi4+\int_r^1\arccos y\,dy
=r\frac\pi4+\left[ y\arccos y-\sqrt{1-y^2}\right]_r^1=r.
\]
For the second,
\[
\int_r^1\frac{y^3}{\sqrt{1-y^2}}dy
=r-\frac{r^3}{3},
\]
so adding \(\int_0^ry^2dy=r^3/3\) gives \(r=1/\sqrt2\). Therefore the full
circle integrals are
\[
N=2\int_{-A}^A\arctan(1/v(t))dt=4A/\sqrt2=\pi,
\]
\[
D=2\int_{-A}^At^2v(t)dt=4A^3/\sqrt2=\pi^3/8.
\]
Thus the quotient is exactly \(8/\pi^2\), proving sharpness.

### 8. Equality conditions

If equality holds globally, the chain
\[
0=(N-\lambda D)/2\ge
LH(c)-\lambda\pi L^2/4\ge0
\]
forces \(\rho=1/2\) and \(c=1\). Hence the range is symmetric with
\(A=1/\sqrt\lambda=\pi/(2\sqrt2)\). The unique pointwise minimizer gives (25).
Its mass is
\[
2\left(\frac A{\sqrt2}
+\int_{A/\sqrt2}^A\frac{t}{\sqrt{A^2-t^2}}dt\right)
=2\left(\frac A{\sqrt2}+\frac A{\sqrt2}\right)=\pi,
\]
so no endpoint atom or other singular mass can remain. Equality in Jensen and
in the \(n\ge2\) reduction forces two equal-slope crossings almost everywhere.
The inverse branch integral then reconstructs the two circular caps and the
central slope-one segment. This confirms the optimizer classification, modulo
the minor topological sentence noted above.

## Counterexample search and hostile edge cases

- **Flat interior plateau:** its pushforward atom lies where \(h>0\), so the
  discarded term \(\int h\,d\sigma\) is strictly positive. It cannot invalidate
  the inequality or attain equality.

- **Plateau at an extremum:** here \(h=0\), so it is not penalized at the dropping
  step. However, in the equality case the absolutely continuous density (25)
  already has total half-mass \(\pi\); (2) then forces the endpoint atom to be
  zero. Symmetric slope-one ramps with endpoint plateaus were also checked
  directly and remained above \(8/\pi^2\).

- **Many oscillations:** almost every traversed level then has \(n\ge4\), and the
  strict increase of \(s\arctan(s/w)\) makes (1) strict. A \(k\)-fold triangular
  wave has quotient \(3k^2/\pi\), not a counterexample.

- **Unequal branch speeds:** strict convexity of \(\phi\) increases the numerator
  for fixed total inverse density. Equality is possible only for equal speeds.

- **Asymmetric positive and negative amplitudes:** this is exactly the slack
  \(1/4-\rho(1-\rho)\ge0\). No assumption of oddness or symmetric rearrangement
  was made in the lower-bound proof.

- **Fat critical set or Cantor-like level behavior:** all length carried by
  \(f'=0\) becomes the singular measure \(2\sigma\), supported on a null set of
  levels. The argument retains it through the moment identities and only drops
  a nonnegative term.

- **Random falsification:** 100,000 random periodic piecewise-linear functions
  (4 to 40 segments, slopes normalized to \([-1,1]\), exact piecewise-linear
  mean and \(L^2\) integrals) produced no quotient below \(8/\pi^2\); the smallest
  observed quotient was approximately \(0.904962\). This numerical search is
  not part of the proof, but it did not expose a hidden factor or asymmetry bug.

## Final conclusion

The current `PROOF.md` passes the adversarial audit. The exact value
\[
\boxed{\lambda_*=\frac8{\pi^2}}
\]
and the optimizer (22) are independently verified. No unsupported step affects
the theorem. The two presentation points above have explicit repairs and are
not fatal.

## Post-repair confirmation

- Re-audited at Unix time `1787778372` after both suggested repairs were added
  to `PROOF.md`.

The added majorant before (11) is correct and locally uniform for \(c\) in a
compact subset of \((0,\infty)\). On the uncapped region the differentiated
integrand is bounded by \(C\sqrt{1-x^2}\), and on the capped region by
\(1-x^2\). The claimed endpoint behavior
\(-2cxV_c(x)=O((1-x)^{-1/2})\) is also correct and integrable. Since the
composition is piecewise \(C^1\) away from the endpoint (with matching
derivatives at the cap transition), this proves absolute continuity and makes
both operations in (11) rigorous. No sign, branch, or boundary term was
introduced by the repair.

The added equality paragraph is also correct. An additional turn on either arc
between the extrema would traverse a nonempty interval of values twice on that
arc, producing at least four total preimages there; a positive-length constant
piece is excluded by \(\sigma=0\). Thus there are precisely two monotone inverse
branches. Their singular length measures are nonnegative summands of the total
singular pushforward, so \(\sigma=0\) eliminates them individually. Equality of
the two reciprocal slopes then assigns density \(v\) to each inverse branch,
justifying \(x=\int_t^A v(s)ds\) and the reconstruction of (22).

**Final post-repair verdict:** the patches introduce no error, close both terse
points identified in the first audit, and leave no unsupported inference in the
final proof.
