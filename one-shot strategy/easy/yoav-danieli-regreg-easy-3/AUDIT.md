# Adversarial Audit of `SOLUTION.md`

Audit begun at **2026-08-27 08:44:47 CEST** (Unix `1787813087`). This is a separate pass over the candidate proof, organized as attempts to break it rather than as a restatement of it.

## A. Claims deliberately rejected

1. **Rejected shortcut:** "Star-free languages are closed under erasing homomorphic images, so simply project a local path language."

   This closure claim is false. For example, `(ab)*` is locally testable (hence star-free), but mapping both `a` and `b` to the unary letter `c` gives the non-star-free unary even-length language. The proof in `SOLUTION.md` does not invoke this closure. It builds a local symbolic language and separately proves equality of its data instances.

2. **Rejected shortcut:** "Adding unused live registers plainly has no semantic effect."

   An arbitrary fixed extended trace can fail because an added register may currently contain an atom selected by an original reassignment or by `x0`. The valid statement is existential: every finite original trace can be lifted by choosing all auxiliary atoms outside the finite set occurring in that trace. This is the argument used in Section 4.

3. **Rejected shortcut:** `neg emptyset` denotes the full alphabet universe.

   Under Definition 8 this is false: `supp(emptyset)` is empty, so `neg emptyset` denotes only `Gamma_emptyset* = {x0}*`. Lemma 1 repairs this by using the empty-language expression `Z_J`, which syntactically mentions every register in `J`; consequently `neg Z_J` really denotes `Gamma_J*`.

## B. Audit of the automata/local-language part

- `supp(E)` is finite because `E` is a finite syntax tree. Therefore `Gamma_I`, the DFA, its transition set, and the auxiliary register set are all finite.
- Fresh auxiliary indices exist because the register indices are infinite and only finitely many are forbidden.
- Marker symbols and payload symbols are disjoint: each marker is `rho_(r_t)` with `r_t` outside `I`, whereas every payload lies in `Gamma_I`.
- Extra alphabet symbols `x_(r_t)` are not silently admitted. Local condition 3 excludes every symbol of `Gamma_J` outside `M union Gamma_I`.
- Conditions 1-4 force every nonempty admitted word to have even length and the form marker/payload/marker/payload/.../marker/payload.
- Condition 5 forces the payload following a marker to be that transition's label.
- Condition 6 forces the target of every encoded transition to equal the source of the next one.
- Conditions 1 and 2 force the run to start at `q_0` and end in `F`. Thus the six conditions are sufficient, not merely necessary.
- The empty word is admitted exactly if `q_0 in F`, exactly matching DFA acceptance of the empty word.
- Empty unions (for example if `F` is empty) can be represented by `Z_J`, retaining full syntactic support.
- Every local condition uses only finitely many length-1, length-2, or length-3 exclusions and finitely many allowed prefixes/suffixes. Lemma 1 translates each Boolean operation using complement padded by `Z_J`, so every complement has the intended `Gamma_J*` domain and no Kleene star is introduced.
- Mechanical sanity check: all two-state, two-letter deterministic transition functions, all final-state subsets, all payloads of length at most four, and all alternating marker/payload strings of the corresponding lengths were exhaustively checked. The six local conditions accepted exactly the canonical codes of accepted payloads. This check is supporting evidence only; the preceding argument is the proof.

## C. Audit of instance-language preservation

### Extended trace to original trace

- Deleting a marker time step is legitimate because `rho_(r_t)` changes only its auxiliary register and outputs the empty word.
- Restricting an injective `J`-valuation to `I` remains injective.
- Freshness relative to all current `J`-values implies freshness relative to the subset of current `I`-values, both for an original reassignment and for `x0`.
- An original output symbol sees the same original-register valuation after marker steps are deleted, because marker steps never change an original register.

Hence restriction cannot create a data word outside `Inst_I(K)`.

### Original trace to extended trace

- A trace of a finite word over finitely many original registers uses finitely many atoms across all valuations and all `x0` choices. Calling this set `S` is justified.
- `A \ S` is infinite because `A` is countably infinite and `S` is finite.
- There are only finitely many auxiliary initial assignments and marker occurrences. They can therefore be assigned pairwise distinct elements of `A \ S`.
- Initial injectivity holds: original initial values lie in `S`; auxiliary initial values lie outside `S` and are pairwise distinct.
- At an auxiliary reassignment, the globally new auxiliary atom differs from its own old value, every other auxiliary current value, and every original current value.
- At an original reassignment, the chosen original atom lies in `S`, while all current auxiliary atoms lie outside `S`; legality among original registers is inherited from the original trace.
- At `x0`, the chosen atom also lies in `S`, so it differs from every auxiliary current value; avoidance of original current values is inherited.
- All added symbols erase, so the output data word is unchanged.
- Edge case `w = epsilon`: an injective initial valuation for the finitely many auxiliary registers exists, and no transition step is required.

Hence every original data word has an extended producing trace.

## D. Decision claim

The preceding construction applies uniformly to every valid ordinary expression. Therefore the property being decided is universal, so the constant algorithm returning `yes` is total and correct. Moreover, the DFA, fresh indices, finite local constraints, and their height-zero expression are all effectively constructible, so the existence proof does not hide a non-effective choice (choosing numerical register indices outside a finite set is effective).

## Verdict

No counterexample or unsupported inference remains. The proof covers empty languages, the empty word, expressions with empty support, original `x0` symbols, original reassignment symbols, repeated use of the same marker transition, additional unused alphabet letters, and the local-complement domain convention.
