# Solution

We prove the stronger statement that every symbolically regular data language has data generalized star height zero. Consequently, the decision procedure in Conjecture 1 always returns **yes**.

## A height-zero expression for the full symbolic alphabet

Let `J` be a nonempty finite register set and put `Delta = Gamma_J`. Define the generalized expression

\[
 Z_J=\bigcup_{j\in J}(\varnothing x_j).
\]

Its language is empty, its support is exactly `J`, and its height is zero. Therefore

\[
 U_J=\neg Z_J
\]

also has height zero and, crucially using the domain-dependent definition of complement,

\[
 L_s(U_J)=\Gamma_J^*=\Delta^*.
\]

It follows that every language over `Delta` specified by a finite Boolean combination of conditions of the following forms has a generalized expression of height zero:

- a fixed word `u` occurs as a factor;
- a word starts with `u`;
- a word ends with `u`.

Indeed, the three positive conditions are denoted respectively by

\[
 U_JuU_J,\qquad uU_J,\qquad U_Ju.
\]

All these expressions have support `J`. Complements therefore have universe `Delta^*`, finite unions use the given union operation, and intersections are obtained by De Morgan's law. If the condition involving the empty word is needed, `epsilon union Z_J` denotes `{epsilon}` while having support `J`. Thus every language described by finitely many forbidden factors together with finite sets of allowed prefixes and suffixes has generalized star height zero. This argument explicitly respects the local support convention for every complement.

## Encoding accepting runs by erased register updates

Let

\[
 \mathcal A=(Q,\Sigma,\delta,q_0,F),\qquad \Sigma=\Gamma_I,
\]

be the input DFA. For each pair `(q,a) in Q x Sigma`, choose a distinct fresh register index `c_(q,a)` not in `I`. Let

\[
 C=\{c_{q,a}:q\in Q, a\in\Sigma\},\qquad J=I\mathbin{\dot\cup}C,
\]

and use

\[
 \mu_{q,a}=\rho_{c_{q,a}}
\]

as a transition marker. These markers are not in `Sigma` and produce no output.

For a word `w=a_1...a_m in Sigma^*`, let `q_r=delta(q_(r-1),a_r)` and define

\[
 e(w)=\mu_{q_0,a_1}a_1\,\mu_{q_1,a_2}a_2\cdots
       \mu_{q_{m-1},a_m}a_m,
\]

with `e(epsilon)=epsilon`. Set

\[
 B=\{e(w):w\in L(\mathcal A)\}\subseteq\Gamma_J^*.
\]

### The language `B` has generalized star height zero

This can be checked using only bounded local conditions. Write

\[
 M=\{\mu_{q,a}:q\in Q, a\in\Sigma\}.
\]

Apart from the possible word `epsilon`, a word `v` is in `B` exactly when all of the following hold:

1. every letter of `v` lies in `Sigma union M`;
2. its first letter is one of `mu_(q_0,a)`;
3. letters alternate between `M` and `Sigma`;
4. every factor `mu_(q,a)b`, with `b in Sigma`, satisfies `b=a`;
5. every factor `mu_(q,a)a mu_(r,b)` satisfies `r=delta(q,a)`;
6. its last two letters are `mu_(q,a)a` with `delta(q,a) in F`.

The empty word is included exactly when `q_0 in F`. Each displayed requirement is a finite Boolean combination of forbidden one-, two-, or three-letter factors and allowed prefixes or suffixes. By the first section, `B` is denoted by a generalized expression of height zero. Hence

\[
 h_{\mathrm{gsym}}(B)=0.
\]

For completeness, the six conditions really characterize `B`: conditions 2, 3, and 6 force a nonempty word to have the form

\[
 \mu_{r_0,a_1}a_1\cdots\mu_{r_{m-1},a_m}a_m.
\]

Condition 2 gives `r_0=q_0`; condition 4 identifies the letter attached to every marker; condition 5 inductively gives `r_i=delta(r_(i-1),a_i)` for `i>=1`; and condition 6 says that the state after the final letter is accepting.

## The markers do not change the generated data words

We show

\[
 \operatorname{Inst}_J(B)=\operatorname{Inst}_I(L(\mathcal A)). \tag{1}
\]

First take a legal `J`-trace for some `e(w) in B`. Delete the marker positions and restrict every valuation to `I`. A marker changes only a register in `C`, so the compressed valuations have the required behavior at every symbol of `w`. Injectivity and every freshness inequality remain true after restricting from `J` to `I`. At an `x_i` or `x_0` position the output is unchanged. This proves

\[
 \operatorname{Inst}_J(e(w))\subseteq\operatorname{Inst}_I(w).
\]

Conversely, fix a legal `I`-trace for `w`, including its chosen output atom at every `x_0` occurrence. Let `S` contain every atom that occurs in any valuation of an original register at any time in this finite trace, together with every chosen `x_0` atom. The set `S` is finite.

Extend the initial valuation to the registers in `C` by choosing pairwise distinct atoms outside `S`. Whenever a marker `rho_c` occurs, reassign `c` to an atom outside `S` and outside the finite set of all currently stored `J`-register values. Such an atom exists because the atom set is infinite. Keep the prescribed original trace at the positions belonging to `w`.

Every marker reassignment is now legal by construction. Every prescribed reassignment of an original register remains legal because its new value belongs to `S`, whereas all current control-register values lie outside `S`. Similarly, each prescribed `x_0` atom belongs to `S` and therefore differs from all current control values; it already differs from all current original-register values by legality of the given trace. Thus the extended trace is legal and has exactly the same output word. Therefore

\[
 \operatorname{Inst}_I(w)\subseteq\operatorname{Inst}_J(e(w)),
\]

which proves (1) after taking unions over accepted `w`.

## Decision procedure

Let

\[
 D=\operatorname{Inst}_I(L(\mathcal A)).
\]

The regular language `B subseteq Gamma_J^*` is a symbolic representation of `D`, and it has generalized symbolic star height zero. Since heights are nonnegative,

\[
 h_{\mathrm{gdata}}(D)=0.
\]

Therefore, for every input `n in N`,

\[
 h_{\mathrm{gdata}}(\operatorname{Inst}_I(L(\mathcal A)))\le n.
\]

The required decision algorithm is the constant algorithm that returns **yes** on every well-formed input. This proves Conjecture 1.
