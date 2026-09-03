# Independent adversarial audit of `PROOF.md`

This audit concerns the proved sufficient theorem and necessary condition in
`PROOF.md`.  It does **not** promote the remaining logarithmic gap to a solved
claim.

## Claims audited

1. If `s >= C (log n)^3/(log log n)^2`, then
   `lambda_s(n) ~ binom(n,2)s`.
2. If `lambda_s(n) ~ binom(n,2)s`, then necessarily
   `s/log n -> infinity`.

## Deterministic part

- Re-derived the equivalence between order `s` and `c_ab <= s`, and the exact
  transition inequality `|U|-1 <= sum c_ab <= binom(n,2)s`.
- Checked inflation locally in all three kinds of projection: the inflated
  pair gains exactly the chosen even number of changes, while a projection
  involving one endpoint and a third symbol gains none.  Distinct supported
  pairs use distinct transition positions, so simultaneous inflation has no
  collision assumption.
- Re-derived the skeleton defect identity.  A boundary of two maximal
  unordered-edge runs gives a distinct non-edge projection change.  Contracting
  a run preserves its endpoints and one occurrence of each symbol, so it
  reduces `c_ab` and `e_ab` equally for the run pair and changes neither for a
  third-symbol projection after repetitions are suppressed.
- Exhaustively tested the skeleton contraction for every repetition-free word
  on up to four symbols and length up to nine.  In every case support and defect
  were preserved and no pair count increased.
- Re-derived the recency-rank identity `sum c_ab = sum r_i`.  For every cache
  size `k`, cheap accesses preserve the top-`k` set and an expensive access
  introduces at most `k-1` new co-resident pairs.  This gives
  `P <= k^2+(k+1)M_k`; dyadic summation then gives
  `sum c_ab = Omega(n^2 log n)`.
- Exhaustively tested that cache inequality for every repetition-free word on
  up to five symbols and length up to eight.

No counterexample was found in the deterministic part.

## Random recursive construction

- Recounted the four fibers of the map
  `g -> (g(0),g(1))`, including the deletion of the zero difference.  The
  resulting probabilities are exactly those in (5).
- After clearing denominators, the actual offspring PGF minus the critical
  binary PGF has numerator `1+2z-3z^2`, which is nonpositive for `z>=1`.
- Conditional on a common child, its fresh uniform bijection sends the pair to
  a uniform distinct child pair.  Different child invocations have independent
  construction randomness.  These are precisely the independence statements
  used by the branching calculation; no independence between different root
  pairs is used.
- Re-derived the first and second moments of the base population.  In the
  thinned case the safe recurrence is
  `E Z_(j+1)^2 <= p^2 E Z_j^2+4 E Z_j`, which yields
  `E Z^2=O(p^t/epsilon)` and hence survival
  `Omega(epsilon p^t)` by Paley--Zygmund.
- Rechecked the run accounting at a recursion node.  With `r` common blocks,
  there are exactly `2-r` singleton blocks for each endpoint; hence the added
  number of projected runs is at most `2(2-r)<=4`.  Thus projected alternating
  length is at most five times total progeny, including empty thinned blocks.
- Independently iterated the critical MGF recurrence for depths up to 3000.
  At parameter `1/(100t^2)` its excess over one was about `0.01/t`, well below
  the analytic bound `1/t`.  The analytic induction and the subcritical
  invariant interval `[0,2epsilon]` were also checked term by term.

## Assembly and asymptotics

- A uniform injection sends each fixed pair to a uniform distinct root pair;
  restriction cannot increase its two-letter projection and cannot destroy a
  retained adjacent transition between its endpoints.
- Coverage needs only an expectation/Markov argument for the unsupported
  *fraction*.  The maximum pair count uses the MGF independently for each fixed
  pair and a union bound; it does not assume root-pair independence.
- With `epsilon=(log t-log log t)/t`, verified
  `p^t~(log t)/t`, one-copy survival
  `Omega((log t)^2/t^2)`, and
  `r epsilon=O(t log log log t/log t)=o(t)`.
  Therefore the Chernoff exponent at
  `H=Ct^3/(log t)^2` beats the fewer-than-`4^t` root pairs.
- The expected average count is
  `O(t^3 log log log t/(log t)^3)=o(H)`, so a Markov threshold can be chosen
  strictly between these scales.  Coverage, maximum, and average events each
  have probability tending to one and therefore intersect.
- Pair-specific inflation loses the **sum** of baseline pair counts, not the
  maximum times the number of pairs.  This is why a fixed sufficiently large
  constant multiple of `H` is enough.

## Audit conclusion

No unsupported inference, hidden independence assumption, parity error, or
counterexample was found in the two audited claims.  The exact smallest growth
rate remains unproved: the audit certifies only the window

`s/log n -> infinity` (necessary) versus
`s >= C(log n)^3/(log log n)^2` (sufficient).
