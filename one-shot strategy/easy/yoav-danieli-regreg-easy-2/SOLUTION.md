# The proposed decision problem is undecidable

The statement called Conjecture 1 in the PDF is false. In fact, undecidability
already holds when the input number is fixed to `n = 1`.

Throughout, `h(L)` denotes the ordinary star height of a regular language over a
finite alphabet, and `h_data(D)` is Definition 11 of the PDF.

## 1. Three elementary lemmas

### Lemma 1 (quotients do not raise ordinary star height)

If `L` is regular and `h(L) <= n`, then, for every language `R` (not necessarily
regular),

\[
 h(R^{-1}L)\le n,\qquad h(LR^{-1})\le n,
\]

where

\[
R^{-1}L=\{v:\exists u\in R,\ uv\in L\},\qquad
LR^{-1}=\{u:\exists v\in R,\ uv\in L\}.
\]

Also, homomorphic images and finite unions do not raise ordinary star height.

**Proof.** Let `E` be an expression of height at most `n` for `L`. The usual
left derivative by one letter is given recursively by

\[
\begin{aligned}
a^{-1}(E\cup F)&=a^{-1}E\cup a^{-1}F,\\
a^{-1}(EF)&=(a^{-1}E)F\ \cup\
  \begin{cases}a^{-1}F,&\varepsilon\in L(E),\\ \varnothing,&\text{otherwise},\end{cases}\\
a^{-1}(E^*)&=(a^{-1}E)E^*.
\end{aligned}
\]

These formulas never increase height. Induction on a word therefore gives an
expression of height at most `n` for every word quotient `u^{-1}L`. A regular
language has only finitely many distinct left quotients, so `R^{-1}L`, which is
the union of those quotients `u^{-1}L` with `u in R`, is a finite union of
height-at-most-`n` languages. The right-quotient assertion is symmetric.
Substitution of a fixed word (possibly the empty word) for every letter in an
expression proves the homomorphism assertion. The union assertion is immediate.
\(\square\)

### Lemma 2 (rigidity of forced equality)

Fix a symbolic word `w`. Two distinct output positions have the same atom in **every**
member of `Inst(w)` if and only if both positions are occurrences of the same
`x_i` in the same scope of register `i`.

**Proof.** The reverse implication is the definition of a scope. For the forward
implication, assign a globally new atom to every initial register and every later
register scope, and choose a globally new atom at every `x_0` occurrence. This is
a legal trace because the word is finite and the atom set is infinite. In this
trace, outputs belonging to different scopes, and all `x_0` outputs, are pairwise
different. Thus equality in every trace is possible only inside one register
scope. \(\square\)

### Lemma 3 (fixed sections do not raise the height of a rigid pair language)

Let `Sigma` and `C={c_1,...,c_m}` be finite alphabets. Introduce finitely many
*anchor roles*: one label role `a_sigma` for each `sigma in Sigma`, a boundary
role `b`, and the code roles `c_1,...,c_m`. A formatted pair has the form

\[
 z_1\cdots z_s\;
 (z_{a_{\sigma_1}}d_1)\cdots(z_{a_{\sigma_\ell}}d_\ell)\;z_b\;
 z_{c_{i_1}}\cdots z_{c_{i_q}}\;
 z_1\cdots z_s,                                      \tag{1}
\]

where the anchor atoms `z_1,...,z_s` are pairwise different and every `d_j`
differs from every anchor. The first component is the labeled data word
`u=(sigma_1,d_1)...(sigma_ell,d_ell)`; the second component is the
finite-alphabet word `v=c_{i_1}...c_{i_q}`. Let `P` be the set of all words of
form (1), and let `F subseteq P` be symbolically regular.

For a fixed first component `u` (more precisely, a fixed equality orbit), put

\[
 F_u=\{v\in C^*:(u,v)\text{ has a formatted representative in }F\}.
\]

Then

\[
 h(F_u)\le h_{data}(F).                               \tag{2}
\]

**Proof.** It is enough to prove that if `K subseteq Gamma_J^*` represents `F`,
then `h(F_u) <= h(K)`.

Every `w in K` is *safe*: `Inst_J(w) subseteq F subseteq P`. In every instance
of `w`, its first `s` outputs and last `s` outputs are the two copies of the
anchor list in (1). Lemma 2 therefore gives an injective tuple

\[
 \bar r=(r_1,\ldots,r_s)\in J^s
\]

such that the two occurrences of anchor `z_i`, and every forced occurrence of
that anchor between them, are outputs from one unchanged scope of register
`r_i`.

There is a small point here that is important. A code position is required to be
*some* code anchor, not a preassigned one. Apply the globally-injective trace used
in Lemma 2: every scope other than the `s` spanning anchor scopes, and every
`x_0`, receives an atom different from all anchors. Hence an output outside the
spanning anchor scopes would be a non-anchor in that trace, contradicting
`Inst(w) subseteq P`. It follows that every label, boundary, code, and trailer
output is `x_{r_i}` for one uniquely determined role `i`. Because data atoms in
(1) are forbidden to equal any anchor, this also makes the parsing of every
instance unique. Thus the whole structural suffix is syntactically rigid once
`bar r` is fixed. Assignments after the last output cause no problem.

For such a tuple `bar r`, let `R_{bar r,u}` be the set of all symbolic prefixes
which have a legal trace producing the header, the encoded copy of `u`, and the
boundary in (1), with header tuple `bar r`, and which end immediately after the
symbol producing the boundary. No regularity assumption on this prefix language
is needed.

Define a word homomorphism `phi_{bar r}` as follows. It erases every assignment
symbol `rho_j`; it maps `x_{r_i}` to a finite letter naming anchor role `i`; and
it maps `x_0` and every `x_j` outside the tuple to a junk letter `#`. Let `T` be
the fixed finite word naming the trailer `z_1...z_s`.

We claim

\[
 F_u=
 \bigcup_{\bar r}
 \left(\phi_{\bar r}(R_{\bar r,u}^{-1}K)\right)T^{-1}. \tag{3}
\]

For the forward inclusion, take a formatted `(u,v) in F`, a word `w in K`, and
a trace of `w` producing it. Cut `w` immediately after the boundary-producing
symbol. The prefix belongs to one `R_{bar r,u}`. Safety and Lemma 2 force the
remaining outputs to be exactly the code for `v` followed by the trailer, so the
right side of (3) contains `v`.

Conversely, suppose `p in R_{bar r,u}`, `ps in K`, and
`phi_{bar r}(s)=vT`. Extend the witnessing legal trace of `p` through `s`; this
is always possible because at each reassignment or `x_0` occurrence a fresh atom
can be chosen from the infinite atom set. Since `ps in K` is safe, the resulting
data word lies in `F subseteq P`. Its fixed prefix is the chosen copy of `u`, and
rigidity forces the suffix decoded by `phi_{bar r}` to be the code for `v` and
the trailer. Hence `v in F_u`. The same argument shows that every word on the
right of (3) automatically belongs to `C^*`; no intersection or other filtering
operation is being used in (3).

There are only finitely many tuples `bar r`. By Lemma 1, arbitrary left quotient,
homomorphic image, fixed right quotient, and finite union do not increase ordinary
star height. Equation (3) proves (2). \(\square\)

## 2. The undecidable source problem

Universality of one-way nondeterministic register automata over finite labeled
data words `(Sigma times A)^*` is undecidable (even with two registers). We use
the standard model in which every source register initially has value `perp`; a
transition reads one pair `(sigma,d)`, tests the equality type of `d` against the
old register values, and updates each register either by keeping its old value or
by storing `d`. General equality constraints can effectively be split according
to the finitely many old-register partitions and input equality types, yielding
this normal form. The countably infinite equality domains `A` and `N` are
isomorphic. This precise labeled-data model and the classical undecidability
boundary are recalled, for example, in Sections 1-2 of Czerwinski, Mottet, and
Quaas, *New Techniques for Universality in Unambiguous Register Automata* (ICALP
2021).

We now give the effective simulation needed here, including the minor mismatch
between possibly duplicate/empty source registers and the PDF's always-filled,
injective registers.

The finite control maintains the equality partition of the non-`perp` logical
source registers and an injection from its blocks to *physical* PDF registers.
Every unused physical register contains a junk atom. Consider a source transition
on `(sigma,d)`.

- First output the label anchor `x_{a_sigma}`.
- If `d` equals an existing logical block represented by physical register `p`,
  output `x_p`. Update the finite partition by merging into that block every
  logical register which the source transition sets to `d`.
- If `d` is fresh and no logical register stores it, output `x_0`.
- If `d` is fresh and some logical registers store it, choose a physical register
  `p` which is unused or whose old logical block is completely overwritten, and
  output `rho_p x_p`. Such a `p` always exists: otherwise all physical registers
  represent surviving blocks, leaving no room for the new block, contrary to the
  fact that there are only as many logical registers as physical ones.

Whenever an old logical block disappears and its physical register was not reused,
append a silent `rho_p` and mark `p` unused. This replaces its stale old value by
junk. All these choices depend only on the finite logical partition and the source
transition, so the set of simulated accepting runs is a regular language; an NFA
for it, and hence a DFA, is effective.

For completeness, fix an accepting source run on a finite word and choose all
initial and subsequently refreshed junk atoms successively, pairwise distinctly,
outside all data atoms of that word and outside all anchor atoms. This makes the
initial valuation injective and every silent refresh legal, so the displayed
simulation is a legal PDF trace.
For soundness, `x_p` can only read the data value of the logical block represented
by `p`, while `rho_p x_p` and `x_0` output a datum different from every PDF
register and therefore from every current logical source value. Silent refreshes
touch only physical registers marked unused. Hence every generated trace projects
to a valid source run. The simulation is exact.

## 3. Reduction to data star height one

Fix once and for all a finite-alphabet regular language `H subseteq C^*` of
ordinary star height exactly 2. Such an `H` exists by the strict ordinary
star-height hierarchy. Since `H` is fixed, a DFA or expression for it is a fixed
part of the reduction.

Let `B` over `Sigma times A` be an instance of the undecidable register-automaton universality
problem. From `B` construct a symbolic regular data language `F_B` of formatted
pairs by

\[
 F_B=(L(B)\times C^*)\ \cup\ (U\times H),              \tag{4}
\]

using format (1). Here `U=(Sigma times A)^*`; format (1) chooses its finitely many
anchor atoms outside the finitely many data atoms in the particular first
component.

This construction is effective. Use disjoint registers for source-register
simulation and for all anchors. Output the anchor header, then:

- for the first term of (4), run the regular symbolic simulation of `B`, with
  `x_{a_sigma}` before every simulated datum having label `sigma`, output `x_b`, generate an arbitrary
  code word by `(x_{c_1} union ... union x_{c_m})^*`, and output the trailer;
- for the second term, generate the arbitrary first component by

  \[
  \bigl((\bigcup_{\sigma\in\Sigma}x_{a_\sigma})x_0\bigr)^*,
  \]

  output `x_b`, generate `H` with the code-anchor registers, and output the
  trailer.

The union is regular over a finite `Gamma_I`; converting its finite automaton to
a DFA gives a valid input to Conjecture 1.

If `B` is universal, the first term of (4) already equals the whole formatted
pair universe `P`. Moreover `P` has the height-1 symbolic expression

\[
 (\text{header})\;
 \bigl((\bigcup_{\sigma\in\Sigma}x_{a_\sigma})x_0\bigr)^*\;
 x_b\;(x_{c_1}\cup\cdots\cup x_{c_m})^*\;
 (\text{trailer}).                                    \tag{5}
\]

Expression (5) uses only the anchor registers. Given any word in `P`, initialize
them with its anchor tuple and choose the independent `x_0` outputs to be its
data entries; hence (5) represents exactly `P`.
Thus

\[
 B\text{ universal}\quad\Longrightarrow\quad
 h_{data}(F_B)\le1.                                    \tag{6}
\]

If `B` is not universal, choose a rejected source word `u` and choose the
finitely many formatting anchors outside its data atoms. A constant-free
equality register automaton is equivariant under every permutation of the data
domain; consequently it rejects every representative of the equality orbit of
`u`. Taking that orbit's `u`-section of (4) therefore gives

\[
 (F_B)_u=H.                                             \tag{7}
\]

Lemma 3 and `h(H)=2` imply

\[
 h_{data}(F_B)\ge2.                                    \tag{8}
\]

Combining (6)-(8),

\[
 h_{data}(F_B)\le1
 \quad\Longleftrightarrow\quad
 B\text{ is universal}.                                \tag{9}
\]

The construction of the DFA for `F_B` is effective, whereas universality of `B`
is undecidable. Therefore no algorithm can decide the predicate in Conjecture 1,
even for the fixed input value `n=1`.

## Conclusion

Conjecture 1 is false: the stated problem is undecidable (already at data star
height threshold 1).

## References

- F. Neven, T. Schwentick, and V. Vianu, [Finite State Machines for Strings over
  Infinite Alphabets](https://citeseerx.ist.psu.edu/document?doi=03387186e5eeb9a47c67845cf6997b9236b19abd&repid=rep1&type=pdf),
  Theorem 18.
- W. Czerwinski, A. Mottet, and K. Quaas, [New Techniques for Universality in
  Unambiguous Register Automata](https://drops.dagstuhl.de/opus/volltexte/2021/14198/pdf/LIPIcs-ICALP-2021-129.pdf),
  Sections 1-2 (standard labeled-data model and the classical undecidability
  boundary for unrestricted register automata).
- L. C. Eggan, [The Star-Height of Regular Expressions](https://deepblue.lib.umich.edu/items/4741cb45-110f-4293-b07b-e39b3b14da8f),
  and the strict ordinary star-height hierarchy.
