# Oracle separation of comparator circuits and catalytic logspace

We use exactly the oracle conventions in the question. In particular, on
inputs of length \(n\), every oracle gate of a \(\mathrm{CC}^O\) circuit is a
\(\widehat O_n\)-gate and therefore asks \(O\) only about strings of length
\(n-1\).

## Two witness languages

For every Boolean oracle \(O\), define (irrelevant values at lengths \(0\) and
\(1\) may be chosen arbitrarily)
\[
 A^O(x_1\cdots x_n)
   =O(\neg x_1\cdots\neg x_{n-1}) \qquad(n\ge 2)
\]
and
\[
 B^O(x)=O(x).
\]

For every \(O\),
\[
 A^O\in \mathrm{CC}^O,
 \qquad
 B^O\in \mathrm{CL}^O.                                      \tag{1}
\]
Indeed, for \(A^O\) use \(n\) wires, initialize the answer wire to \(0\),
initialize the other \(n-1\) wires to
\(\neg x_1,\ldots,\neg x_{n-1}\), apply one \(\widehat O_n\)-gate, and
designate its first output. This is an AC\(^0\)-uniform, linear-description-size
family. For \(B^O\), a catalytic machine designates the whole read-only input
as its query interval, calls \(O\), and returns the oracle-output bit. It never
changes the catalyst.

The rest of the proof constructs \(O\) so that no CLO machine decides \(A^O\)
and no CCO family decides \(B^O\).

## A restoration-counting lemma

We use the bit-tape convention stated in the problem: the auxiliary data
\(a\), and hence the current content \(y\) of an interval submitted to the
Boolean oracle, are bit strings. Thus each of the \(m\) catalytic cells has two
possible contents throughout the computation. This point is essential to the
information count below. (In a variant whose catalyst alphabet is \(\Gamma\)
and which quantifies over every \(a\in\Gamma^m\), the identical argument uses
\(|\Gamma|^m\) and \(|\Gamma|^{m-\ell}\).) Fix a catalytic machine \(M\), an
input \(x\) of length \(n\), a Boolean oracle, and resource bounds of \(w\)
ordinary work cells and \(m\) catalytic cells. All \(m\) catalytic cells are
initially filled by an arbitrary string \(a\in\{0,1\}^m\); unused cells can
simply be padded.

**Lemma.** Suppose that, for every \(a\in\{0,1\}^m\), the computation
\(M(x,a)\) halts and restores its catalyst to \(a\). Let \(q\in\{0,1\}^\ell\)
be a string which is not a substring of \(x\). There are constants \(K,d,e\),
depending only on \(M\), such that the number of catalysts \(a\) whose
computation ever calls the oracle on \(q\) is at most
\[
 K(n+m)^d 2^{m-\ell+ew}.                                    \tag{2}
\]
When \(\ell>m\), that number is zero.

**Proof.** For each catalyst whose run calls the oracle on \(q\), select the
first complete instantaneous configuration immediately before such a call.
The selected configurations for two distinct initial catalysts cannot be the
same. If they were the same (even if reached at different times), determinism
with the fixed oracle would give the two runs the same suffix and hence the
same final catalytic contents. Exact restoration would then say that their two
distinct initial catalysts are equal, a contradiction.

Because \(q\) is not an input substring, this call must designate an interval
of the catalytic tape. For a fixed position of that interval, fixing its
\(\ell\) bits to \(q\) leaves at most \(2^{m-\ell}\) choices for the remainder
of the catalyst. The interval position, finite control, tape-head positions,
oracle-output bit, and endpoint data contribute only a polynomial factor in
\(n+m\); the contents of the \(w\)-cell ordinary work tape contribute
\(2^{O(w)}\). Summing over possible interval positions gives (2). The
injectivity just proved now finishes the count. \(\square\)

In particular, if \(m=n^{O(1)}\), \(w=O(\log n)\),
\(\ell=n-1\), and \(n\) is sufficiently large (with the machine and its
resource constants fixed), the right side of (2) is strictly smaller than
\(2^m\). Thus some initial catalyst never causes a query to \(q\).

## The two finite-extension steps

A *finite partial oracle* is a map from a finite subset of
\(\{0,1\}^*\) to \(\{0,1\}\). Every step below preserves all values already
assigned. The separating oracle need not be computable, so the semantic case
distinction used below is legitimate.

### Defeating one CCO family

Fix a CCO circuit family \(C=\{C_n\}\) and a finite partial oracle \(\sigma\).
Choose \(n\) so large that no string of length \(n-1\) or \(n\) has yet been
assigned. Assign \(0\) to every string of length \(n-1\), and evaluate
\(C_n\) on \(x=0^n\); call its output \(c\). This output is now permanent,
because every oracle gate in \(C_n\) queries only a string of length \(n-1\).
Set
\[
 O(0^n)=1-c.                                                  \tag{3}
\]
Then \(C_n(0^n)=c\ne B^O(0^n)\). Thus this finite extension permanently
defeats \(C\) as a decider for \(B^O\).

### Defeating one CLO machine

Fix a *syntactically bounded* catalytic machine \(M\), with hard barriers at
the explicit integer capacity bounds
\[
 w(n)=O(\log n),\qquad m(n)=n^{O(1)},                         \tag{4}
\]
and a finite partial oracle \(\sigma\). Choose \(n\) so large that \(n-1\)
exceeds every previously assigned oracle length and so that the consequence of
the lemma applies. Put
\[
 x=0^n,\qquad q=1^{n-1}.                                     \tag{5}
\]
Notice that \(q\) is not a substring of \(x\). Let
\(R=\max\{n,m(n)\}\). Temporarily leave \(q\) open and assign \(0\) to every
other still-unassigned oracle string of length at most \(R\). No computation
of \(M\) on an input of length \(n\) can query a longer string: an allowed
query is an interval of either the \(n\)-bit input or the \(m(n)\)-bit
catalyst.

First consider the completion in which \(O(q)=0\). If some initial catalyst
has a computation which does not halt and restore, retain this completion.
That bad computation is permanent because every oracle answer it could ask has
now been fixed, and \(M\) is not a valid CLO decider.

Otherwise all \(2^{m(n)}\) computations halt and restore. By the lemma, some
catalyst \(a\) has a computation which never queries \(q\). Let its decision
bit be \(d\). If \(d=1\), set \(O(q)=0\); then
\(d\ne A^O(0^n)=0\). If \(d=0\), instead set \(O(q)=1\). The selected
computation is unchanged because it never queries \(q\), so now
\(d\ne A^O(0^n)=1\). In either case, after this finite extension \(M\)
permanently fails to decide \(A^O\).

This argument also covers a machine whose answer depends on the initial
catalyst: one wrong catalyst already violates the definition.

Here is the precise enumeration which justifies the syntactic bound used
above. Enumerate all triples \((P,c,k)\), and replace \(P\) by a bounded version
\(P_{c,k}\) having hard barriers on ordinary-work addresses, catalytic
addresses, and oracle-interval endpoints at
\[
 c\lceil\log(n+2)\rceil
 \quad\text{and}\quad
 (n+2)^k,                                                      \tag{6}
\]
respectively. An attempted overrun enters a fixed failure behavior. Pad the
catalyst to the declared capacity and have the simulation ignore the padding.
Consequently \(P_{c,k}\) respects these bounds for *every* oracle, including
the temporary completion used at its diagonal stage.

Now suppose, toward contradiction, that some machine \(P\) is a CLO decider
for \(A^O\) in the final oracle constructed below. For suitable \(c,k\), its
computation relative to that final \(O\) never meets the barriers in (6), so
the corresponding entry \(P_{c,k}\) agrees with \(P\) there. But the stage for
that entry permanently makes \(P_{c,k}\) fail on \(A^O\), a contradiction.
Thus diagonalizing this countable list of syntactically bounded machines is
sufficient even though a program's space use under other oracle completions
could have been larger.

## One-sided oracles

Enumerate all AC\(^0\)-uniform polynomial-size CCO families and repeatedly
apply the first finite-extension step, always choosing a fresh larger input
length. Take the union of the partial oracles and set every still-undefined
value to \(0\). The resulting oracle \(O_2\) satisfies
\[
 B^{O_2}\in\mathrm{CL}^{O_2}
 \quad\hbox{but}\quad
 B^{O_2}\notin\mathrm{CC}^{O_2},
\]
so \(\mathrm{CL}^{O_2}\not\subseteq\mathrm{CC}^{O_2}\).

Similarly, enumerate all logarithmic-work, polynomial-catalyst machines and
apply the second finite-extension step. The resulting oracle \(O_1\) satisfies
\[
 A^{O_1}\in\mathrm{CC}^{O_1}
 \quad\hbox{but}\quad
 A^{O_1}\notin\mathrm{CL}^{O_1},
\]
so \(\mathrm{CC}^{O_1}\not\subseteq\mathrm{CL}^{O_1}\).

## A single oracle

Finally, interleave the two enumerations. At even stages apply the extension
which defeats the next CCO family on \(B^O\); at odd stages apply the extension
which defeats the next CLO machine on \(A^O\). At every stage choose the new
input length \(n\) so that \(n-1\) exceeds the length of every string assigned
at all earlier stages.
Each stage assigns only finitely many values and never changes an old one, so
all earlier diagonal witnesses remain permanent.

Let \(O\) be the union of these finite partial oracles, completed by \(0\) on
all strings never assigned. By (1), \(A^O\in\mathrm{CC}^O\) and
\(B^O\in\mathrm{CL}^O\). Every CLO machine fails on \(A^O\), and every CCO
family fails on \(B^O\). Consequently
\[
 \boxed{
 \mathrm{CC}^O\not\subseteq\mathrm{CL}^O
 \quad\text{and}\quad
 \mathrm{CL}^O\not\subseteq\mathrm{CC}^O.}
\]
