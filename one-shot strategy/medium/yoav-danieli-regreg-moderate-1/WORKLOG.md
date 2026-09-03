# Worklog: Data generalized star-height conjecture

## 2026-08-28

- **Unix start time:** `1787913012`.
- **Problem source inspected:** `yoav-danieli-regreg-moderate-1.pdf` (3 pages). Target is Conjecture 1: every symbolically regular data language `D` satisfies `hgdata(D) <= 1`.
- **Proof standard:** no early completion until a full candidate proof is followed by a separate adversarial audit checking every inference, hidden assumption, and possible counterexample.
- **Initial structural observations:** We may change the finite register set and the regular symbolic representation. Complement is domain-dependent and local to an expression's support, so any use of Boolean closure must explicitly arrange a common support/alphabet.

### 2026-08-28 12:34 CEST - Route 1: transition markers / local run language

- Let a DFA for the given regular representation `K` have transition set `T`. Give every transition `t` a fresh dummy register `m_t`, and encode it as the two-letter block `rho_(m_t) lambda(t)`, where `lambda(t)` is its original symbolic label.
- **Candidate semantic lemma:** inserting arbitrary reassignment operations on fresh, never-output dummy registers preserves the set of data-word instances after projection. Forward inclusion is immediate by restricting any expanded trace. For reverse inclusion, fix an original finite trace and choose every initial/reassigned dummy value outside the finite set of all atoms ever used by that original trace (including all `x0` outputs), also choosing dummy values globally fresh. Countable infinitude of `A` supplies enough choices. This also makes every original reassignment and `x0` output legal in the expanded trace.
- **Candidate language lemma:** encoded accepting runs are 3-local. A nonempty encoded word must (a) begin with a marker whose transition leaves the DFA's initial state; (b) end in a block whose transition enters a final state; (c) have only marker/label and label/marker adjacent pairs of the correct form; and (d) have no factor `marker(t) lambda(t) marker(u)` with `target(t) != source(u)`. These conditions are exact.
- A finite-alphabet language described by finitely many permitted prefixes/suffixes and forbidden factors is generalized-star-height at most 1: use `Sigma*` only unnested, finite unions/concatenations, complement, and Boolean intersection. Must pad expressions to full register support before complementing, or make every complemented operand contain the full-alphabet expression `Sigma`.
- **Potential pitfall recorded:** symbols available over the enlarged register set include the unwanted output letters `x_(m_t)` as well as marker letters `rho_(m_t)`. They must be excluded by the forbidden adjacent-pair list / exact local alphabet conditions. Because the final suffix has length 2 and all allowed pairs alternate, even one-letter unwanted words are excluded.
- **Potential edge cases to audit:** `K` empty; `K={epsilon}`; empty original register set; unreachable DFA transitions; one-transition words; `x0` payloads; payload reassignments; repeated use of the same marker register; local-complement support.

### 2026-08-28 12:35 CEST - Separate adversarial audit, pass 1

- Treated the transition-marker construction as untrusted and checked the two inclusions of the semantic lemma separately.
- **Expanded trace -> original trace:** restrict valuations to the old registers at the payload boundaries and discard marker steps. A dummy reassignment never changes an old register; an old reassignment fresh relative to all expanded registers is in particular fresh relative to all old registers; and an expanded `x0` output fresh relative to all expanded registers is fresh relative to the old ones. Hence projection is always a legal original trace with identical output.
- **Original trace -> expanded trace:** let `S` contain every old-register value at every time and every chosen `x0` output in the fixed original trace. `S` is finite. Choose all dummy initial values and every value later assigned at a marker from `A \ S`, globally distinct. This establishes expanded initial injectivity, dummy freshness, old-reassignment freshness against dummies (old values lie in `S`), and `x0` freshness against dummies (`x0` outputs lie in `S`). Output is unchanged.
- Checked the subtle future-output issue: choosing dummy values merely fresh *at insertion time* would be insufficient, since a persistent dummy could equal a future `x0` output. Excluding the global finite set `S` repairs this completely.
- Exhaustively compared the proposed 2/3-factor predicate with the exact encoded accepting-run predicate for all complete two-state DFAs over payload alphabet `{x0}`, all final-state sets, all words of length at most 8 over the full enlarged alphabets (including unwanted `x_j` letters). Result: `PASS: 7812496 exhaustive local-vs-run cases`.
- **Edge cases verified:**
  - `K=empty`: the final-block condition is empty, so the constructed nonempty code language is empty; epsilon is not added.
  - `K={epsilon}` (or epsilon membership generally): add epsilon exactly when the DFA initial state is final. Since finite registers always admit an injective initial valuation, `Inst(epsilon)={epsilon}` for both old and enlarged register sets.
  - `I=empty`: `Gamma_I={x0}`; transition markers still give a nonempty enlarged support. The semantic finite-avoidance argument works unchanged.
  - One-block code words are exactly two symbols; the start-marker and final-block tests correctly enforce both endpoints.
  - Payload `rho_i`: the dummy marker precedes it, and dummy values were chosen outside every old trace value, so the old reassignment remains legal.
  - Payload `x0`: dummy values avoid every fixed `x0` output globally.
  - Repeated marker use: globally distinct values for all dummy scopes are stronger than the required adjacent-scope freshness.
- No counterexample found in this pass.

### 2026-08-28 12:36 CEST - Discarded shortcuts and explicit counterexamples

- **False shortcut: pair constraints alone suffice.** Suppose `t` leaves the initial state and enters `q1`, while `u` leaves a different state `q2` and enters a final state, and both labels are `a`. Then `rho_(m_t) a rho_(m_u) a` passes the natural start, end, and allowed-pair checks, but `t,u` are not composable. The forbidden length-3 factors are therefore essential.
- **False shortcut: one undifferentiated marker identifies transitions.** If two transitions have the same payload label but different endpoints, a common marker followed by that label does not retain enough information to check run composition. The construction must use transition-specific marker registers (or a more complicated uniquely decodable marker code).
- **False overgeneralization: arbitrary reassignment insertions are inert.** Inserting `rho_1` between the two letters of `x_1 x_1` changes the equality pattern from two equal outputs to two unequal outputs. Only reassignments of fresh, never-output registers may be inserted.
- **Infinity is essential to the neutrality proof.** Over a hypothetical one-element atom set, `Inst_emptyset(x0)` is nonempty but adding one untouched dummy register makes `x0` impossible. The actual problem assumes countably infinite `A`, so the finite-avoidance construction is valid.

### 2026-08-28 12:36 CEST - Separate adversarial audit, pass 2 (expression/support audit)

- Fix enlarged alphabet `B=Gamma_J` and let `U_J` be the union of every literal in `B`. Then `L(U_J*)=B*`, `supp(U_J*)=J`, and its height is exactly 1.
- Every local-condition operand is forced to have support exactly `J` by an occurrence of `U_J*`: start is `P U_J*`, end is `U_J* E`, and factor avoidance is `not(U_J* N_k U_J*)`. Thus every complement in these operands is genuinely relative to `B*`, not a smaller accidental alphabet.
- For full-support expressions `E_1,...,E_r`, their intersection is represented by `not(not E_1 union ... union not E_r)`. Both inner and outer complements use `B*`; complement and union do not raise height. No star occurs inside another star anywhere, so height stays at most 1.
- The unwanted enlarged-alphabet literals `x_(m_t)` occur in `B` and hence in the bad-pair set. Any word of length at least 2 containing one has a forbidden adjacent pair; words of length 0 or 1 are controlled separately. Therefore they cannot leak into the code language.
- Line-by-line exactness check of the local characterization: the starting condition selects a transition out of `q0`; good pairs force a unique alternating factorization into blocks `rho_(m_t) lambda(t)`; forbidden triples enforce adjacent endpoints; and the ending condition enforces a final target. Conversely every accepting run satisfies all four conditions.
- The epsilon case is separated before applying prefix/suffix constraints and is added iff `q0` is final.
- **Conclusion of pass 2:** every expression-semantics inference and every support/height calculation checks out; no unsupported step or counterexample remains.

### 2026-08-28 12:40 CEST - Final literal audit of `SOLUTION.md`

- Re-read all three rendered PDF pages and compared the proof against Definitions 1-12. In particular, the audit used the stronger reassignment rule requiring a new value to differ from the register's own previous value as well as all other current values.
- Checked finiteness assumptions: `Gamma_I` is finite, so a complete DFA has finitely many transitions; only finitely many fresh indices are needed; every fixed trace has finitely many old values, `x0` outputs, and dummy scopes.
- Checked that no transition marker outputs data: every marker is a fresh `rho_(m_t)`, never `x_(m_t)`.
- Checked both set equalities used in the conclusion: Lemma 1 is pointwise for every encoded word, and the local-language proof establishes exactly `C={c(w):w in K}`, not merely one inclusion.
- Checked the generalized-expression syntax: finite languages use only literals, finite union, and concatenation; the only stars are separate occurrences of `U_J*`; intersection is expanded using only union and complement; all complement operands have exact support `J`.
- Checked the minimization step: the explicitly constructed `C subset Gamma_J*` is regular, satisfies `Inst_J(C)=D`, and has `h_gsym(C)<=1`; hence it is an admissible witness in the minimum defining `h_gdata(D)`.
- Rejected no further claims and found no hidden assumption. The proof is accepted after the separate adversarial audit.
- **Audit completion Unix time:** `1787913640`; elapsed wall-clock time from recorded start: `628` seconds. Early termination is justified by completion and verification of a full proof.
