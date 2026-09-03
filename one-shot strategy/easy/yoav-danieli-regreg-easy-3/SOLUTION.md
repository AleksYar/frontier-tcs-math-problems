# Solution to Conjecture 1

We prove a stronger statement: **every symbolically regular data language has a generalized star-free symbolic representation**. Consequently, the requested decision algorithm can always answer **yes**.

Throughout, if `I` is a finite register set, write
\[
\Sigma_I=\Gamma_I=\{x_0\}\cup\{x_i,\rho_i:i\in I\}.
\]

## 1. A useful generalized star-free universe

The domain-dependent meaning of complement requires a small preliminary observation.

**Lemma 1.** Let \(J\subseteq\mathbb N_{>0}\) be finite. Every language over \(\Gamma_J\) described by a finite Boolean combination of conditions of the following forms has a generalized symbolic expression of height zero:

- the word has a prescribed prefix;
- the word has a prescribed suffix;
- the word contains a prescribed finite factor.

The same holds for complements of these conditions.

**Proof.** List \(J=\{j_1,\ldots,j_k\}\), and put
\[
 Z_J=\varnothing x_{j_1}\cdots x_{j_k},
\]
with \(Z_\varnothing=\varnothing\). Its language is empty, its support is exactly \(J\), and its height is zero. Hence
\[
 U_J:=\neg Z_J
\]
has height zero and denotes \(\Gamma_J^*\), because this particular complement is taken relative to \(\Gamma_J^*\).

If \(H\) is any height-zero expression using only registers in \(J\), define
\[
 C_J(H):=\neg(H\cup Z_J).
\]
Then \(C_J(H)\) has height zero and denotes \(\Gamma_J^*\setminus L_s(H)\). Thus relative complement and, by De Morgan's law, finite intersection are available without introducing a star. For a fixed word \(u\in\Gamma_J^*\), the expressions
\[
 uU_J,\qquad U_Ju,\qquad U_JuU_J
\]
respectively express the prefix, suffix, and factor conditions for \(u\). Finite Boolean combinations of them therefore have height zero. \(\square\)

## 2. Encoding an accepting run by invisible register updates

Let \(E\) be the input ordinary symbolic regular expression, let
\[
 I=\operatorname{supp}(E),\qquad K=L_s(E)\subseteq\Gamma_I^*,
\]
and let
\[
 \mathcal A=(Q,\Gamma_I,\delta,q_0,F)
\]
be a complete DFA recognizing \(K\). This DFA is effectively constructible from \(E\).

Regard each DFA transition as a triple
\[
 t=(q,a,\delta(q,a)).
\]
The finite transition set is denoted by \(T\). For every \(t\in T\), choose a distinct fresh register index \(r_t\notin I\), and set
\[
 R=\{r_t:t\in T\},\qquad J=I\cup R,\qquad m_t=\rho_{r_t}.
\]
The symbols \(m_t\) are pairwise distinct, produce no output, and do not reassign any original register.

For an accepting run
\[
 q_0\mathrel{\xrightarrow{a_1}}q_1
 \mathrel{\xrightarrow{a_2}}\cdots
 \mathrel{\xrightarrow{a_n}}q_n\in F,
\]
where \(t_k=(q_{k-1},a_k,q_k)\), define its code to be
\[
 m_{t_1}a_1m_{t_2}a_2\cdots m_{t_n}a_n.
\]
Let \(K'\subseteq\Gamma_J^*\) be the set of all such codes, together with \(\varepsilon\) exactly when \(q_0\in F\).

## 3. The run-code language is generalized star-free

For a transition \(t=(q,a,q')\), write
\[
 \operatorname{src}(t)=q,\qquad \operatorname{lab}(t)=a,
 \qquad \operatorname{tgt}(t)=q'.
\]
Let \(M=\{m_t:t\in T\}\) and \(P=\Gamma_I\). A nonempty word \(z\in\Gamma_J^*\) belongs to \(K'\) if and only if all of the following finite local conditions hold:

1. its first letter is some \(m_t\) with \(\operatorname{src}(t)=q_0\);
2. its last two letters are \(m_t\operatorname{lab}(t)\) for some \(t\) with \(\operatorname{tgt}(t)\in F\);
3. every letter lies in \(M\cup P\);
4. no two consecutive letters both lie in \(M\), and no two consecutive letters both lie in \(P\);
5. for every factor \(m_ta\) with \(t\in T\) and \(a\in P\), one has \(a=\operatorname{lab}(t)\);
6. for every factor \(m_t a m_u\), one has
   \(\operatorname{tgt}(t)=\operatorname{src}(u)\).

These conditions are necessary for a run code. Conversely, conditions 1, 3, and 4 force the word to alternate between a marker and an original symbol, beginning with a marker; condition 2 forces it to end with an original symbol. Condition 5 makes every marker-symbol pair encode its named transition, condition 6 makes consecutive transitions composable, condition 1 gives the initial state, and condition 2 gives an accepting final state. Thus the conditions are also sufficient.

Each condition is a finite Boolean combination of prescribed prefix, suffix, and forbidden-factor conditions of lengths at most three. Lemma 1 therefore yields a generalized height-zero expression for the nonempty part of \(K'\). Adding \(\varepsilon\) when \(q_0\in F\) does not increase its height. Hence
\[
 h_{\mathrm{gsym}}(K')=0.
\]

## 4. Inserting the markers preserves the instance language

We prove
\[
 \operatorname{Inst}_J(K')=\operatorname{Inst}_I(K).
\]

### Inclusion \(\operatorname{Inst}_J(K')\subseteq\operatorname{Inst}_I(K)\)

Take \(z\in K'\), and delete all marker symbols \(m_t\). By the definition of \(K'\), the resulting word is some \(w\in K\). Consider any legal assignment trace for \(z\) over \(J\). At marker positions only an auxiliary register in \(R\) is reassigned, so the values of all registers in \(I\) remain unchanged. Restrict all valuations to \(I\) and delete the marker time steps.

The resulting trace is legal for \(w\): injectivity is preserved by restriction; every original reassignment that was fresh relative to all current \(J\)-register values is certainly fresh relative to the current \(I\)-register values; and every \(x_0\)-choice that avoided all current \(J\)-register values also avoids all current \(I\)-register values. The markers output \(\varepsilon\), and every original symbol has the same output before and after the restriction. Thus every data word generated by \(z\) belongs to \(\operatorname{Inst}_I(w)\).

### Inclusion \(\operatorname{Inst}_I(K)\subseteq\operatorname{Inst}_J(K')\)

Take \(w=a_1\cdots a_n\in K\) and a legal assignment trace over \(I\) producing a data word \(d\). Let \(z\in K'\) be the code of the unique DFA run on \(w\).

Only finitely many atoms occur anywhere in the given trace: namely, in its register valuations and in its choices at \(x_0\)-positions. Call this finite set \(S\). Since the atom set is infinite, choose all initial values and all successive reassignment values of the auxiliary registers in \(R\) to be pairwise distinct atoms in \(A\setminus S\). Keep the original registers and all \(x_0\)-choices exactly as in the given trace.

This gives a legal trace for \(z\). Initially, the auxiliary values are distinct from one another and from every original value. Each marker assigns its auxiliary register a globally new value outside \(S\), hence a value different from every current register value. Each original reassignment remains legal because its new value lies in \(S\), while every current auxiliary value lies outside \(S\); its legality relative to the other original registers was already part of the given trace. Likewise, every original \(x_0\)-choice lies in \(S\), avoids the current original values by hypothesis, and avoids all auxiliary values because those lie outside \(S\). Finally, markers output nothing, so this lifted trace still produces \(d\).

This proves the reverse inclusion and hence the desired equality.

## 5. Decision algorithm

The language \(K'\) is a generalized star-free symbolic representation of the same data language generated by \(E\). Since the construction applies to every ordinary symbolic regular expression \(E\), the following algorithm decides Conjecture 1:

> On every valid input \(E\), return **yes**.

The DFA and marker construction above is effective and, if desired, also computes a generalized height-zero witness rather than merely deciding its existence. Therefore Conjecture 1 holds. \(\blacksquare\)
