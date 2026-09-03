#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <vector>

static constexpr int MOD = 1000003;

int modpow(long long a, int e) {
    long long out = 1;
    while (e) {
        if (e & 1) out = out * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return static_cast<int>(out);
}

int norm(long long x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return static_cast<int>(x);
}

std::array<int, 255> gradient(const std::array<int, 8>& space,
                              const std::array<int, 256>& c) {
    std::array<int, 255> out{};
    std::array<int, 7> pts{};
    for (int i = 0; i < 7; ++i) pts[i] = space[i + 1];
    int total = 0;
    for (int p : pts) total = norm(total + c[p]);
    const int inv3 = modpow(3, MOD - 2);
    const int inv7 = modpow(7, MOD - 2);
    for (int p : pts) {
        const int cp = c[p];
        long long dtop = 3LL * total * total - 3LL * cp * cp;
        long long dlift = 0;
        // The three Fano lines through p are indexed twice by the other six
        // points, so retain one representative from each xor-pair.
        for (int q : pts) {
            if (q == p) continue;
            int r = p ^ q;
            if (q > r) continue;
            int s = norm(static_cast<long long>(cp) + c[q] + c[r]);
            long long dB = 3LL * s * s - 3LL * cp * cp;
            long long dD = 2LL * s - 2LL * cp;
            dtop -= dB;
            dlift += dB - 3LL * dD;
        }
        long long dpoint = 3LL * cp * cp - 6LL * cp + 2;
        out[p - 1] = norm(dtop + inv3 * dlift + inv7 * dpoint);
    }
    return out;
}

int main() {
    std::array<int, 256> c{};
    int quarter = modpow(4, MOD - 2);
    for (int x = 1; x < 256; ++x) if ((x & 3) == 3) c[x] = quarter;

    std::map<int, std::array<int, 255>> basis;
    long long checked = 0;
    bool done = false;
    for (int p0 = 0; p0 < 8 && !done; ++p0)
    for (int p1 = p0 + 1; p1 < 8 && !done; ++p1)
    for (int p2 = p1 + 1; p2 < 8 && !done; ++p2) {
        std::array<int, 3> piv{p0, p1, p2};
        std::vector<std::pair<int, int>> slots;
        for (int col = 0; col < 8; ++col) {
            if (col == p0 || col == p1 || col == p2) continue;
            for (int row = 0; row < 3; ++row)
                if (piv[row] < col) slots.emplace_back(row, col);
        }
        std::uint64_t limit = 1ULL << slots.size();
        for (std::uint64_t mask = 0; mask < limit; ++mask) {
            std::array<int, 3> rows{1 << p0, 1 << p1, 1 << p2};
            for (std::size_t i = 0; i < slots.size(); ++i)
                if ((mask >> i) & 1ULL) rows[slots[i].first] |= 1 << slots[i].second;
            std::array<int, 8> space{};
            int at = 0;
            for (int bits = 0; bits < 8; ++bits) {
                int x = 0;
                for (int i = 0; i < 3; ++i) if ((bits >> i) & 1) x ^= rows[i];
                space[at++] = x;
            }
            // XOR generation is not sorted, but gradient only requires zero first.
            for (int i = 1; i < 8; ++i) {
                if (space[i] == 0) std::swap(space[0], space[i]);
            }
            auto row = gradient(space, c);
            ++checked;
            while (true) {
                int pivot = -1;
                for (int j = 0; j < 255; ++j) if (row[j]) { pivot = j; break; }
                if (pivot < 0) break;
                auto it = basis.find(pivot);
                if (it == basis.end()) {
                    int scale = modpow(row[pivot], MOD - 2);
                    for (int& x : row) x = static_cast<int>(1LL * x * scale % MOD);
                    basis.emplace(pivot, row);
                    break;
                }
                int scale = row[pivot];
                for (int j = pivot; j < 255; ++j)
                    row[j] = norm(row[j] - 1LL * scale * it->second[j]);
            }
            if (basis.size() == 255) { done = true; break; }
        }
    }
    std::cout << "prime " << MOD << " rows " << checked
              << " rank " << basis.size() << "\n";
}
