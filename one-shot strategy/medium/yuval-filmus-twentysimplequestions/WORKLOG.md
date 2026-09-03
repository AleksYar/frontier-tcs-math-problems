# Proof Search Worklog

- **Start Unix time:** `1787937611`
- **Start UTC:** `2026-08-28T17:20:11Z`
- **Proof-and-audit completion Unix time:** `1787938895`
- **Elapsed wall time to verified proof:** `1284` seconds
- **Problem source:** `yuval-filmus-twentysimplequestions.pdf`

## Chronological log

- **2026-08-28T17:20:22Z** — Confirmed the source PDF is present and has one letter-sized page. Began read-only extraction and visual inspection.
- **2026-08-28T17:20:49Z** — Extracted and rendered the complete PDF. Verified the sole problem asks, for fixed `c > 2`, for a small natural inventory of partitions of `[n]` into at most `c` answer classes which supports, for every distribution `mu`, a decision tree of expected depth `< H_c(mu)+1`. The source suggests generalizing the binary inventory consisting of threshold questions `x<m` and equality questions `x=m`.
- **2026-08-28T17:22:31Z** — Located and downloaded the referenced Dagan--Filmus--Gabizon--Moran paper. Read its complete binary redundancy-1 proof: a weight-balancing algorithm switches to equality tests when the largest conditional atom exceeds a threshold (e.g. `0.3`); its published analysis uses a one-dimensional adversarial game.
- **2026-08-28T17:28:40Z** — Detected a consistency error in the problem sheet. The stated interval-only bound `H_c(mu)+log_c 2` is false as written: for `c=3`, `mu=(epsilon,1-2epsilon,epsilon)` has `H_3(mu)->0`, while any strategy on its three-point support asks at least one question, contradicting an additive constant `log_3 2<1`. The standard Gilbert--Moore ceiling calculation instead gives `< H_c(mu)+1+log_c 2`, so the sheet likely omitted `+1`. This does not affect the explicit target `<H_c(mu)+1`.
- **2026-08-28T17:30:05Z** — Candidate route A: optimal alphabetic `c`-ary trees (questions partitioning the current ordered support into at most `c` intervals). If their redundancy is already `<1` for `c>=3`, the natural inventory of all interval partitions solves the target. Began exact dynamic-programming falsification on small instances.
- **2026-08-28T17:32:18Z** — Exact dynamic programming for optimal ternary alphabetic trees on hundreds of thousands of random distributions up to support size 30 found no redundancy `>=1` (worst cases approach 1 only for a distribution tending to a point mass). This supports, but does not prove, the interval-tree route.
- **2026-08-28T17:33:02Z** — Discarded a specific midpoint/Patricia-trie construction: randomized tests gave explicit redundancy `>1` (e.g. approximately `1.52` for `c=3` on an 11-point highly nonuniform distribution). Thus optimal alphabetic behavior cannot be justified by that naive trie.
- **2026-08-28T17:35:45Z** — Verified a clean shifted-grid lemma leading to a complete candidate proof with a slightly richer inventory: all partitions of the cyclic order on `[n]` into at most `c` cyclic intervals. For fixed `c` this inventory has at most `sum_{k=2}^c binom(n,k)=O_c(n^c)` nontrivial questions.
  - Place probability arcs `J_i` of lengths `p_i` consecutively on the unit circle.
  - Shift the nested `c`-adic grid by `U`; encode `i` by the first grid cell wholly contained in `J_i`. The chosen cells are disjoint, hence yield a prefix code. Its trie is implementable by cyclic-interval questions.
  - With `m=ceil(log_c(1/p))`, `s=c^{-m}`, and `r=p/s in [1,c)`, the first containing-cell level is `m` surely if `r>=2`; if `1<=r<2`, it is `m` with probability `r-1` and `m+1` otherwise. Level `m+1` always works because `c>=3`.
  - For `r>1`, expected pointwise redundancy is `<1`: it is `log_c r<1` for `r>=2`, and `2-r+log_c r<1` for `1<r<2`, using `log_c r<r-1` since `ln c>1`. For `r=1` it is exactly 1.
  - Therefore averaging over shifts gives total expected length `<H_c+1` unless all positive probabilities are integral powers of `c`. In the all-`c`-adic case, align the grid with one probability arc: that symbol uses its information length exactly, while every other symbol uses at most information length plus 1, giving the strict saving of that symbol's positive mass.
- **2026-08-28T17:37:04Z** — Wrote the complete candidate proof to `SOLUTION.md`.
- **2026-08-28T17:41:11Z** — Completed a separate adversarial audit of the candidate proof.
  - **Grid boundary audit:** checked `r=1`, `r=2`, `p` near 1, and circle-wrap cases. Coarser levels cannot fit because `c^{-(m-1)}>p`; level `m+1` always fits because its cell size is `s/c` and `p>=s>=3s/c>2s/c`. Half-open endpoints affect only null events and not the bounds.
  - **Strictness audit:** for `1<r<2`, the exact slack is `r-1-log_c r>0`; for `2<=r<c`, it is `1-log_c r>0`. When every `r=1`, aligning one arc saves its positive mass `p_i0`, so the final inequality is strict. The support-one case separately has cost `0<1`.
  - **Prefix-free audit:** selected grid cells lie in disjoint probability arcs. Nested-grid cells can only be disjoint or nested, so no selected cell is a prefix ancestor of another.
  - **Inventory audit:** inside each grid cell, child candidates are consecutive in cyclic order. A proper current candidate block has a cyclic-interval complement; merging that complement into an end child extends the local split to a global partition into no more than `c` cyclic intervals. Zero-probability gaps can likewise be absorbed into adjacent blocks.
  - **Size audit:** a `k`-arc cyclic partition is determined by `k` cut gaps, yielding at most `1+sum_{k=2}^c binom(n,k)=O_c(n^c)` questions (up to constant answer-label permutations).
  - **Computational falsification:** checked 120 random distributions for each of several `c` values using 5,000 equidistributed shifts per instance; all produced a shift below `H_c+1`. Also checked the adversarial `3`-adic sequence `(1/9,1/3,1/9,1/3,1/9)` under each arc-aligned shift; all costs were strictly below the target.
  - **Hidden-assumption audit:** the same random shift is shared by all symbols, but only linearity of expectation is used, so no independence assumption is present. Suppressing unary trie vertices only lowers cost. The construction and inventory are independent of `mu` except for the selected strategy, as required.
  - **Audit conclusion:** no unsupported inference or counterexample found. The candidate proof is complete.
