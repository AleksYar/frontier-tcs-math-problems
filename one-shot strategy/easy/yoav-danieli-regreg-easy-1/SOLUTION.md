# Solution: the data star-height hierarchy is infinite

Write `sh(L)` for the ordinary star height of a regular language `L`. Thus, when `K` is a symbolic language, `sh(K)` is exactly `h_sym(K)` from Definition 10. We prove the following stronger transfer statement.

> **Transfer theorem.** For every regular language `L` over the binary alphabet `Sigma={a,b}`, there is a symbolically regular data language `D(L)` such that
> 
> `h_data(D(L)) = sh(L)`.

The conjecture then follows immediately from the classical ordinary star-height hierarchy.

## 1. Two elementary lemmas

### Lemma 1 (operations that do not raise ordinary star height)

Let `M` be regular.

1. If a monoid morphism maps every letter to a word (possibly the empty word), then `sh(theta(M)) <= sh(M)`.
2. For every fixed word `v`, `sh(v^{-1}M) <= sh(M)`, where
   `v^{-1}M={z:vz in M}`.
3. A finite union has star height at most the maximum of the heights of its terms. A bijective renaming of letters preserves star height.

**Proof.** For (1), take an expression for `M` and replace each letter by the finite word that is its image. This introduces no star.

For (2), it is enough to consider quotient by one letter and iterate. The usual left derivative of an expression satisfies

```text
d_c(empty)=empty,              d_c(epsilon)=empty,
d_c(d)=epsilon if c=d, else empty,
d_c(E union F)=d_c(E) union d_c(F),
d_c(EF)=d_c(E)F union d_c(F)  if epsilon is in L(E),
d_c(EF)=d_c(E)F               otherwise,
d_c(E*)=d_c(E)E*.
```

An induction on `E` shows that the displayed derivative has height at most `h(E)`. In the last clause, for example, its height is at most
`max(h(E),h(E*))=h(E*)`. Its language is `c^{-1}L(E)`, proving (2). Part (3) follows directly by taking a union of expressions and by renaming their literals. ∎

### Lemma 2 (a trace separating all distinct scopes)

For a fixed symbolic word `w`, tag an occurrence of `x_i` by the scope of register `i` containing that occurrence, and give every occurrence of `x_0` its own tag. Two output positions have the same output atom in every legal trace of `w` if and only if they have the same tag.

**Proof.** Equal tags can only arise from two occurrences of the same `x_i` in one scope, so equality in every trace is immediate.

Conversely, construct one legal trace as follows. Give all initial register scopes pairwise distinct atoms. At each reassignment, give the new scope an atom never used anywhere earlier in the construction. At each `x_0`, also choose an atom never used earlier. This is possible because `w` is finite and `A` is infinite. It is legal: a globally new register value differs from every current register value, and a globally new `x_0` value is not current. In this trace, outputs with different tags are distinct. Thus equality in every trace forces equal tags. ∎

## 2. The dictionary encoding

For distinct atoms `alpha,beta` and a word `u=u_1...u_m in {a,b}*`, put

```text
enc_{alpha,beta}(u)
  = alpha beta alpha beta c_1...c_m,

where c_j=alpha if u_j=a, and c_j=beta if u_j=b.
```

Define

```text
D(L)={enc_{alpha,beta}(u): alpha,beta in A, alpha != beta, u in L}.
```

If `L` is empty, then `D(L)` is empty and both sides of the transfer theorem are 0. Henceforth suppose `L` is nonempty.

Let `phi(a)=x_1` and `phi(b)=x_2`, and set

```text
K_0=x_1 x_2 x_1 x_2 phi(L).
```

Here `phi(L)` denotes the letterwise image of `L`. Because an initial valuation is injective and there are no reassignments in these words,

```text
Inst_{ {1,2} }(K_0)=D(L).
```

Thus `D(L)` is symbolically regular. Replacing `a,b` in a minimum-height expression for `L` by `x_1,x_2` and adjoining the fixed prefix introduces no star, so

```text
h_data(D(L)) <= sh(L).                                      (1)
```

## 3. Every symbolic representation retains the height of `L`

Let `I` be any finite register set and let a regular `K subseteq Gamma_I*` satisfy

```text
Inst_I(K)=D(L).                                             (2)
```

Every symbolic word has a legal trace (use fresh atoms), and (2) implies, for each `w in K`,

```text
Inst_I(w) subseteq D(L).                                   (3)
```

Fix `w in K` and number its output positions. Every word in (3) has its first and third atoms equal, its second and fourth atoms equal, and its first two atoms distinct. By Lemma 2, output positions 1 and 3 are occurrences of some register `r` in one scope, and positions 2 and 4 are occurrences of some register `s` in one scope. Moreover `r != s`: if `r=s`, the equality of the tags at positions 1 and 3 says that no `rho_r` occurs between them, so position 2 would have the same tag as position 1, contradicting the forced inequality of the first two outputs.

Every later output in every member of `D(L)` equals either the first or the second atom. Apply the separating trace from Lemma 2. The tag of each later output must therefore equal the tag at position 1 or the tag at position 2. Hence every later output is, structurally, either `x_r` in the same scope as positions 1 and 3, or `x_s` in the same scope as positions 2 and 4. In particular, no output of `w` is `x_0`.

It follows that `w` uniquely determines a word `u(w) in {a,b}*`: write `a` for each later output carrying the first tag and `b` for each carrying the second. Every trace of `w` has equality pattern `enc_{alpha,beta}(u(w))`. By (3), and because `w` has a legal trace,

```text
u(w) in L.                                                 (4)
```

Now use a fresh finite alphabet `B_I={X_i:i in I} union {Z}` and the morphism

```text
eta(x_i)=X_i,       eta(rho_i)=epsilon,       eta(x_0)=Z.
```

For each ordered pair `(r,s)` of distinct registers, let

```text
L_{r,s}={u(w): w in K and the first two output scopes use registers r,s}.
```

If `phi_{r,s}(a)=X_r` and `phi_{r,s}(b)=X_s`, the structural conclusion above gives the exact decomposition

```text
eta(K)
 = union_{r,s in I, r != s}
     X_r X_s X_r X_s phi_{r,s}(L_{r,s}).                   (5)
```

By (4), every `L_{r,s}` is contained in `L`. Conversely, take `u in L` and any distinct atoms `alpha,beta`. The word `enc_{alpha,beta}(u)` lies in `D(L)` and hence, by (2), is produced by some `w in K`. Its equality pattern uniquely decodes to `u`, so the preceding analysis puts `u` into one of the `L_{r,s}`. Therefore

```text
L = union_{r,s in I, r != s} L_{r,s}.                      (6)
```

For a fixed pair `(r,s)`, all words on the right side of (5) have a four-letter prefix identifying their pair. Consequently,

```text
(X_r X_s X_r X_s)^{-1} eta(K)=phi_{r,s}(L_{r,s}).          (7)
```

Lemma 1, first for the morphism `eta`, then for the quotient in (7), and finally for the inverse letter-renaming `phi_{r,s}^{-1}`, yields

```text
sh(L_{r,s}) <= sh(eta(K)) <= sh(K).                        (8)
```

There are only finitely many ordered pairs because `I` is finite. Equations (6), (8), and Lemma 1(3) now give

```text
sh(L) <= sh(K).                                            (9)
```

This holds for every symbolic representation `(I,K)` of `D(L)`. Taking the minimum in the definition of data star height, and combining (9) with (1), proves

```text
h_data(D(L))=sh(L).                                        (10)
```

## 4. The hierarchy

For every `n>=1`, take

```text
L_n={u in {a,b}*: |u|_a-|u|_b = 0 modulo 2^n}.
```

The classical theorem of Dejean and Schützenberger says that `sh(L_n)=n`; see F. Dejean and M. P. Schützenberger, [*On a Question of Eggan*](https://monge.univ-mlv.fr/~berstel/Mps/Travaux/A/1966-6QuestionEgganIC.pdf), *Information and Control* 9 (1966), 23-25. For `n=0`, instead take the finite language `L_0={epsilon}`, which has ordinary star height 0.

Finally set `D_n=D(L_n)`. Equation (10) gives, for every `n in N`,

```text
h_data(D_n)=n.
```

This proves the data star-height hierarchy conjecture. ∎
