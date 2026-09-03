#include <algorithm>
#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>

// Exhaustive decision-protocol search for tiny U_m diamond KW_g instances.
// A state is a combinatorial rectangle A x B. Invalid pairs (equal g-vectors)
// impose no output constraint, matching the promised relation in the PDF.

struct Key {
  uint32_t a, b;
  uint8_t d;
  bool operator==(const Key& o) const { return a == o.a && b == o.b && d == o.d; }
};
struct Hash {
  size_t operator()(const Key& k) const {
    return (uint64_t(k.a) * 0x9e3779b185ebca87ULL) ^
           (uint64_t(k.b) * 0xc2b2ae3d27d4eb4fULL) ^ k.d;
  }
};

int nbits, rows, input_bits, ninputs, noutputs;
uint32_t gtable;
std::vector<uint32_t> outmask;
std::vector<std::vector<uint32_t>> bad_union;
std::vector<uint32_t> heuristic_masks;
std::unordered_map<Key, bool, Hash> memo;
uint64_t calls;
bool heuristic_only = false;

int grow(int x, int r) {
  int rowmask = (1 << nbits) - 1;
  return (gtable >> ((x >> (r * nbits)) & rowmask)) & 1;
}

uint32_t gv(int x) {
  uint32_t ans = 0;
  for (int r = 0; r < rows; ++r) ans |= uint32_t(grow(x, r)) << r;
  return ans;
}

bool mono(uint32_t A, uint32_t B) {
  if (!bad_union.empty()) {
    for (int o = 0; o < noutputs; ++o)
      if ((bad_union[o][A] & B) == 0) return true;
    return false;
  }
  uint32_t common = (noutputs == 32 ? ~uint32_t(0) : ((uint32_t(1) << noutputs) - 1));
  bool any = false;
  for (int x = 0; x < ninputs; ++x) if ((A >> x) & 1) {
    for (int y = 0; y < ninputs; ++y) if ((B >> y) & 1) {
      uint32_t om = outmask[x * ninputs + y];
      if (om) { any = true; common &= om; if (!common) return false; }
    }
  }
  return !any || common;
}

bool can_one(uint32_t A, uint32_t B) {
  if (mono(A, B)) return true;
  if (bad_union.empty()) return false;
  // Alice partitions A: each child must be monochromatic.  Such a partition
  // exists iff two output labels' singleton-good row sets cover A.
  std::vector<uint32_t> good_rows(noutputs), good_cols(noutputs);
  uint32_t input_universe = ninputs == 32 ? ~uint32_t(0) : ((uint32_t(1) << ninputs) - 1);
  for (int o = 0; o < noutputs; ++o) {
    uint32_t gr = 0;
    for (int x = 0; x < ninputs; ++x)
      if ((bad_union[o][uint32_t(1) << x] & B) == 0) gr |= uint32_t(1) << x;
    good_rows[o] = gr;
    good_cols[o] = input_universe ^ bad_union[o][A];
  }
  for (int o = 0; o < noutputs; ++o) for (int p = o; p < noutputs; ++p) {
    if ((A & ~(good_rows[o] | good_rows[p])) == 0) return true;
    if ((B & ~(good_cols[o] | good_cols[p])) == 0) return true;
  }
  return false;
}

bool can(uint32_t A, uint32_t B, int d) {
  ++calls;
  if (mono(A, B)) return true;
  if (!d) return false;
  if (d == 1 && !bad_union.empty()) return can_one(A, B);
  if (A > B) std::swap(A, B); // symmetry of this relation
  Key key{A, B, uint8_t(d)};
  auto it = memo.find(key);
  if (it != memo.end()) return it->second;

  // Enumerate unordered proper bipartitions by forcing the least element into S.
  auto try_side = [&](uint32_t P, uint32_t Q) {
    for (uint32_t H : heuristic_masks) {
      uint32_t S = P & H;
      if (S && S != P && can(S, Q, d - 1) && can(P ^ S, Q, d - 1)) return true;
    }
    if (heuristic_only) return false;
    uint32_t low = P & -P;
    uint32_t rest = P ^ low;
    for (uint32_t sub = rest;; sub = (sub - 1) & rest) {
      uint32_t S = sub | low;
      if (S != P && can(S, Q, d - 1) && can(P ^ S, Q, d - 1)) return true;
      if (sub == 0) break;
    }
    return false;
  };

  bool ans = try_side(A, B) || try_side(B, A);
  memo.emplace(key, ans);
  return ans;
}

int main(int argc, char** argv) {
  if (argc < 4 || argc > 6) {
    std::cerr << "usage: protocol_search n m truth_table_mask [start_depth] [heuristic_only]\n";
    return 2;
  }
  nbits = std::stoi(argv[1]);
  rows = std::stoi(argv[2]);
  gtable = uint32_t(std::stoul(argv[3], nullptr, 0));
  input_bits = nbits * rows;
  ninputs = 1 << input_bits;
  noutputs = input_bits;
  if (ninputs > 32 || noutputs > 31) {
    std::cerr << "tiny search supports at most 32 inputs and 31 outputs\n";
    return 2;
  }
  outmask.assign(ninputs * ninputs, 0);
  for (int x = 0; x < ninputs; ++x) for (int y = 0; y < ninputs; ++y) {
    if (gv(x) == gv(y)) continue;
    uint32_t diff = uint32_t(x ^ y);
    outmask[x * ninputs + y] = diff;
  }
  if (ninputs <= 16) {
    bad_union.assign(noutputs, std::vector<uint32_t>(uint32_t(1) << ninputs));
    for (int o = 0; o < noutputs; ++o) {
      std::vector<uint32_t> bad_row(ninputs);
      for (int x = 0; x < ninputs; ++x) {
        uint32_t ys = 0;
        for (int y = 0; y < ninputs; ++y) {
          uint32_t om = outmask[x * ninputs + y];
          if (om && ((om >> o) & 1) == 0) ys |= uint32_t(1) << y;
        }
        bad_row[x] = ys;
      }
      for (uint32_t A = 1; A < (uint32_t(1) << ninputs); ++A) {
        uint32_t low = A & -A;
        int x = __builtin_ctz(low);
        bad_union[o][A] = bad_union[o][A ^ low] | bad_row[x];
      }
    }
  }
  for (int bit = 0; bit < input_bits; ++bit) {
    uint32_t H = 0;
    for (int x = 0; x < ninputs; ++x) if ((x >> bit) & 1) H |= uint32_t(1) << x;
    heuristic_masks.push_back(H);
  }
  for (int r = 0; r < rows; ++r) {
    uint32_t H = 0;
    for (int x = 0; x < ninputs; ++x) if (grow(x, r)) H |= uint32_t(1) << x;
    heuristic_masks.push_back(H);
  }
  for (uint32_t v = 0; v < (uint32_t(1) << rows); ++v) {
    uint32_t H = 0;
    for (int x = 0; x < ninputs; ++x) if (gv(x) == v) H |= uint32_t(1) << x;
    heuristic_masks.push_back(H);
  }
  uint32_t all = ninputs == 32 ? ~uint32_t(0) : ((uint32_t(1) << ninputs) - 1);
  int start_depth = argc == 5 ? std::stoi(argv[4]) : 0;
  if (argc >= 5) start_depth = std::stoi(argv[4]);
  if (argc == 6) heuristic_only = std::stoi(argv[5]) != 0;
  for (int d = start_depth; d <= input_bits + 4; ++d) {
    memo.clear(); calls = 0;
    bool ok = can(all, all, d);
    std::cout << "depth " << d << ": " << (ok ? "YES" : "NO")
              << " states=" << memo.size() << " calls=" << calls << std::endl;
    if (ok) break;
  }
}
