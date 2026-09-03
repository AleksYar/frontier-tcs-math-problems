# Proof-search worklog

- **1787778616 (Unix start time):** Began active proof search. Located `daniel-goldberg-relative-periodic-coupled-graphs.pdf`; next step is full text extraction plus visual inspection of the final section.
- **1787778695:** Extracted the complete one-page PDF and visually checked the rendered page. The problem is to classify smooth periodic solutions of
  \(u_t=(u_x/\sqrt{1+u_x^2})_x-(u-v)\), \(v_t=(v_x/\sqrt{1+v_x^2})_x+(u-v)\)
  satisfying a common horizontal/vertical relative-return condition at some \(T>0\).
- **1787778695 — verified route 1 (Lyapunov identity):** Direct differentiation and periodic integration by parts give
  \[
  \frac{d}{dt}\mathcal L(u,v)=-\int_{\mathbb T}(u_t^2+v_t^2)\,dx.
  \]
  At the relative endpoint, both derivative terms and \(u-v\) are merely translated, so \(\mathcal L(T)=\mathcal L(0)\). Hence the integrated nonnegative dissipation vanishes and smoothness implies \(u_t=v_t=0\) pointwise on \(\mathbb T\times[0,T]\).
- **1787778695 — verified route 2 (critical-point rigidity):** For a stationary pair, the Euler equations are
  \(A_x-(u-v)=0\), \(B_x+(u-v)=0\), with \(A=u_x/\sqrt{1+u_x^2}\), \(B=v_x/\sqrt{1+v_x^2}\). Multiplying by \(u-c\) and \(v-c\), integrating, and adding yields
  \[
  0=-\int_{\mathbb T}\left(\frac{u_x^2}{\sqrt{1+u_x^2}}+
  \frac{v_x^2}{\sqrt{1+v_x^2}}+(u-v)^2\right)dx.
  \]
  Thus \(u_x=v_x=0\) and \(u=v\), so every critical pair is a common constant.
- **1787778695 — alternative route retained for audit:** The same rigidity follows from convexity of \(\mathcal L\): any critical point is a global minimizer, while the pointwise/Jensen lower bound is \(\mathcal L\ge 4\pi\), with equality only for common constants. The multiplier proof is more elementary and avoids needing to state an infinite-dimensional convexity theorem.
- **1787778695 — discarded possible families:** Common vertical drifts \(u=v=c+kt\) fail the PDE unless \(k=0\). Unequal spatial constants satisfy a decaying two-dimensional ODE but cannot return with a common vertical shift at positive time. Nonzero affine spatial slopes are excluded by periodicity. These checks agree with the rigidity identity.
- **1787778695 — provisional classification:** \(u(x,t)=v(x,t)=c\), where \(c\in\mathbb R\); the endpoint condition then forces \(b=0\), while every \(a\in\mathbb T\) and every \(T>0\) work. A separate line-by-line adversarial audit remains before accepting this as final.
- **1787778806:** Wrote the candidate proof to `SOLUTION.md` and began a separate adversarial audit of the written argument.
- **1787778829 — audit of the Lyapunov calculation:** Recomputed both variational signs from scratch. For the \(u\)-component, \(\delta\mathcal L/\delta u=-\partial_xF(u_x)+(u-v)=-u_t\). For the \(v\)-component, \(\delta\mathcal L/\delta v=-\partial_xF(v_x)-(u-v)=-v_t\). Thus there is no missing factor or sign in the squared-dissipation identity.
- **1787778829 — audit of endpoint invariance:** Differentiating the endpoint equations in \(x\) eliminates \(b\), and subtracting them eliminates the common \(b\). All three terms of the integrand at time \(T\) are therefore the corresponding time-zero terms composed with \(x\mapsto x+a\). Haar/Lebesgue measure on \(\mathbb T\) is translation invariant for every \(a\in\mathbb T\). No assumption that \(a\) has finite order is used.
- **1787778829 — audit of the zero-dissipation inference:** Since \(T>0\) and \(u_t,v_t\) are continuous, zero integral of \(u_t^2+v_t^2\) on the compact spacetime cylinder implies pointwise vanishing. This would be false without an appropriate a.e.-to-pointwise regularity argument, but smoothness supplies it.
- **1787778829 — audit of stationary rigidity:** Re-expanded the multiplier identity with \(w=u-v\): the coupling contribution is \(-wu+wv=-w^2\), not \(+w^2\); the two integration-by-parts contributions are \(-F(u_x)u_x\) and \(-F(v_x)v_x\). After moving the common minus sign outside, all three displayed terms are nonnegative. Their simultaneous zero set is exactly \(u_x=v_x=0\) and \(u=v\). Periodicity removes all boundary terms.
- **1787778829 — independent proof route:** A stationary pair is a critical point of the convex functional \(\mathcal L\). The elementary bound \(\sqrt{1+p^2}\ge1\) gives \(\mathcal L\ge4\pi\), with equality exactly for common constants; testing the critical equation toward a common constant reproduces the nonnegative multiplier identity. This independently matches the rigidity conclusion.
- **1787778829 — independent parameter checks:** Conservation of \(\int_{\mathbb T}(u+v)\,dx\) forces \(4\pi b=0\) directly. Substitution verifies that every common constant solves both PDEs for every \(a\) and every \(T>0\) when \(b=0\). The exclusion \(T=0\) is essential and is already part of the hypothesis.
- **1787778829 — hidden-domain audit and repair:** The first draft could be read as asserting constancy at negative times outside the interval constrained by the problem. The proof directly classifies the restriction to \([0,T]\); it also proves constancy on every larger forward interval starting at \(0\), using \(\mathcal L\ge4\pi\). `SOLUTION.md` was revised to state exactly this and not invoke unproved backward uniqueness.
- **1787778829 — adversarial audit result:** No unsupported inference remains in the scoped theorem. The Lyapunov route, the stationary multiplier route, the convexity/lower-bound cross-check, and the conserved-mean cross-check all agree; attempted nonconstant or drifting families fail. Candidate accepted as a complete proof.
- **1787778863 (completion):** Re-read the final proof after the scope correction and verified the written theorem, converse, parameter set, and audit record. Condition 1 of the requested stopping rule is met.
