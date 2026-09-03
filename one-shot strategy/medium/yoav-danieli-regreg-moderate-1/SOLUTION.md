# Proof of the data generalized star-height conjecture

## Theorem

Every symbolically regular data language has data generalized star height at most $1$.

## Proof

Let $D\subseteq A^*$ be symbolically regular. Choose a finite register set $I$ and a regular language

\[
K\subseteq \Gamma_I^*
\qquad\text{such that}\qquad
D=\operatorname{Inst}_I(K).
\]

Put $\Sigma=\Gamma_I$. We shall enlarge the register set and replace $K$ by a generalized-height-$1$ representation with the same instances.

### 1. Fresh reassignment markers do not change instances

We first isolate the semantic fact used in the construction.

**Lemma 1 (neutrality of fresh-register reassignments).** Let $J\supseteq I$ be finite. Suppose $z\in\Gamma_J^*$ is obtained from $w\in\Gamma_I^*$ by inserting symbols $\rho_j$ with $j\in J\setminus I$, and no output symbol $x_j$ with $j\in J\setminus I$ occurs in $z$. Then

\[
\operatorname{Inst}_J(z)=\operatorname{Inst}_I(w).
\]

**Proof.** First take a legal trace for $z$. Delete the inserted reassignment steps and restrict every valuation to $I$. An inserted $\rho_j$, with $j\notin I$, changes no old register. At an old reassignment $\rho_i$, freshness relative to all current $J$-registers implies freshness relative to the $I$-registers. Likewise, an $x_0$-output fresh relative to all current $J$-registers is fresh relative to the old registers. The restricted trace is therefore a legal trace for $w$, and its output is unchanged. This proves

\[
\operatorname{Inst}_J(z)\subseteq\operatorname{Inst}_I(w).
\]

Conversely, fix a legal trace for $w$. Let $S\subseteq A$ consist of

- every value of every register in $I$ at every time in this trace, and
- every atom chosen at an $x_0$-position.

The set $S$ is finite. There are also only finitely many scopes of the new registers in $z$. Since $A$ is infinite, assign to all those new-register scopes pairwise distinct atoms from $A\setminus S$. In particular, use distinct such atoms for all initial new-register values and for every value installed by an inserted reassignment.

The enlarged initial valuation is injective. At an inserted $\rho_j$, the new value differs from every current old value because it lies outside $S$, and it differs from every current new-register value because all chosen new-scope values are distinct. At an old $\rho_i$, the new old value lies in $S$, so it differs from every new-register value, while its freshness among old registers follows from the original trace. Finally, every prescribed $x_0$-output lies in $S$, and hence differs from every new-register value; its freshness among old registers again follows from the original trace. Thus we have a legal trace for $z$ with exactly the original output. Hence the reverse inclusion also holds. $\square$

The use of the whole finite set $S$, rather than only the values current when a marker is inserted, ensures that a dummy value can never collide with a future $x_0$-output.

### 2. Encode DFA transitions by fresh reassignment markers

Let

\[
\mathcal A=(Q,q_0,\delta,F)
\]

be a complete DFA over $\Sigma$ accepting $K$. Its transition set is

\[
T=\{(q,a,\delta(q,a)):q\in Q,\ a\in\Sigma\}.
\]

For $t\in T$, write $\operatorname{src}(t)$, $\operatorname{lab}(t)$, and $\operatorname{tgt}(t)$ for its source, label, and target. Choose pairwise distinct fresh register indices

\[
m_t\in\mathbb N_{>0}\setminus I \qquad(t\in T),
\]

and set

\[
M=\{m_t:t\in T\},\qquad J=I\cup M,\qquad r_t=\rho_{m_t}.
\]

For $w=a_1\cdots a_n$, let

\[
q_0\xrightarrow{a_1}q_1\xrightarrow{a_2}\cdots\xrightarrow{a_n}q_n
\]

be its unique run, and put $t_k=(q_{k-1},a_k,q_k)$. Define

\[
c(w)=r_{t_1}a_1r_{t_2}a_2\cdots r_{t_n}a_n,
\]

with $c(\varepsilon)=\varepsilon$, and let

\[
C=\{c(w):w\in K\}\subseteq\Gamma_J^*.
\]

Every $c(w)$ is obtained from $w$ by inserting only reassignments of registers in $J\setminus I$. Lemma 1 gives

\[
\operatorname{Inst}_J(c(w))=\operatorname{Inst}_I(w)
\quad\text{for every }w\in\Sigma^*.
\tag{1}
\]

It remains to show that $C$ has a generalized expression of height at most $1$.

### 3. The encoded accepting runs are 3-local

Let $B=\Gamma_J$, the full enlarged symbolic alphabet. The marker letters $r_t$ are pairwise distinct and none belongs to $\Sigma$. Define the following finite languages:

\[
P=\{r_t:\operatorname{src}(t)=q_0\},
\]

\[
E=\{r_t\operatorname{lab}(t):\operatorname{tgt}(t)\in F\},
\]

and let the permitted length-two factors be

\[
G_2=
\{r_t\operatorname{lab}(t):t\in T\}
\;\cup\;
\{a r_t:a\in\Sigma,\ t\in T\}.
\]

Put

\[
N_2=B^2\setminus G_2
\]

and define the set of incompatible length-three factors by

\[
N_3=
\{r_t\operatorname{lab}(t)r_u:
t,u\in T,\ \operatorname{tgt}(t)\ne\operatorname{src}(u)\}.
\]

We claim that the nonempty part $C_+=C\setminus\{\varepsilon\}$ is exactly

\[
C_+
=PB^*
\cap B^*E
\cap\bigl(B^*\setminus B^*N_2B^*\bigr)
\cap\bigl(B^*\setminus B^*N_3B^*\bigr).
\tag{2}
\]

Indeed, the code of an accepting nonempty run plainly satisfies all four conditions. Conversely, take a word satisfying the right-hand side of (2). Its first symbol is a marker $r_{t_1}$ with source $q_0$. Avoidance of $N_2$ forces every marker $r_t$ to be followed by precisely $\operatorname{lab}(t)$, forces every following symbol (if any) to be another marker, and excludes all other enlarged-alphabet letters, including every unwanted $x_{m_t}$. The final condition $B^*E$ ensures that the word ends after a complete marker-label block. Consequently it has a unique factorization

\[
r_{t_1}\operatorname{lab}(t_1)
r_{t_2}\operatorname{lab}(t_2)\cdots
r_{t_n}\operatorname{lab}(t_n).
\]

Avoidance of $N_3$ says exactly that

\[
\operatorname{tgt}(t_k)=\operatorname{src}(t_{k+1})
\qquad(1\le k<n).
\]

Thus the blocks form a run beginning at $q_0$, and membership in $B^*E$ says that its last transition enters $F$. This is an accepting run, proving (2).

### 4. A generalized expression of height at most 1

For a finite language $L\subseteq B^*$, write $[L]$ for the ordinary star-free expression obtained by taking the finite union of the literal concatenations spelling the words of $L$; take $[\varnothing]=\varnothing$. Let

\[
U_J=x_0\;\cup\!\bigcup_{j\in J}(x_j\cup\rho_j).
\]

Then $L_s(U_J)=B$, $\operatorname{supp}(U_J)=J$, and $U_J^*$ has height $1$. Consider

\[
H_1=[P]U_J^*,
\qquad
H_2=U_J^*[E],
\]

\[
H_3=\neg\bigl(U_J^*[N_2]U_J^*\bigr),
\qquad
H_4=\neg\bigl(U_J^*[N_3]U_J^*\bigr).
\]

Each $H_i$ has support exactly $J$ because it contains $U_J^*$, even if one of the displayed finite languages is empty. Thus every displayed complement is taken relative to $B^*=\Gamma_J^*$, exactly as required by the domain-dependent complement definition. Each $H_i$ has height at most $1$.

For expressions $R,S$ of support $J$, define the usual Boolean intersection by

\[
R\wedge S:=\neg(\neg R\cup\neg S).
\]

All three complements here again have universe $\Gamma_J^*$, so $L_s(R\wedge S)=L_s(R)\cap L_s(S)$. Complement and finite union do not raise height. Therefore the iterated intersection

\[
H_+=H_1\wedge H_2\wedge H_3\wedge H_4
\]

has support $J$, height at most $1$, and by (2) denotes $C_+$. Finally set

\[
H=
\begin{cases}
H_+\cup\varepsilon,&q_0\in F,\\
H_+,&q_0\notin F.
\end{cases}
\]

Because $q_0\in F$ exactly when $\varepsilon\in K$, we have $L_s(H)=C$ and $h(H)\le1$. Hence

\[
h_{\mathrm{gsym}}(C)\le1.
\tag{3}
\]

Finally, using (1),

\[
\operatorname{Inst}_J(C)
=\bigcup_{w\in K}\operatorname{Inst}_J(c(w))
=\bigcup_{w\in K}\operatorname{Inst}_I(w)
=D.
\]

Thus $C\subseteq\Gamma_J^*$ is a symbolic representation of $D$, and (3) implies

\[
h_{\mathrm{gdata}}(D)\le1.
\]

Since $D$ was arbitrary, the conjecture follows. $\blacksquare$
