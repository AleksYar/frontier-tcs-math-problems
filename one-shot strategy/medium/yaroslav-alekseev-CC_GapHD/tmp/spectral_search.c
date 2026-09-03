#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int pc(unsigned x) { return __builtin_popcount(x); }

int main(void) {
    enum { n = 6, N = 64, M = 20 };
    int mid[M], a[N], m = 0;
    uint64_t best_l1 = UINT64_MAX;
    unsigned best_mask = 0;
    for (int x = 0; x < N; ++x)
        if (pc((unsigned)x) == 3) mid[m++] = x;
    for (unsigned mask = 0; mask < (1u << M); ++mask) {
        for (int x = 0; x < N; ++x) {
            int bit = pc((unsigned)x) >= 4;
            if (pc((unsigned)x) == 3) {
                int j = 0;
                while (mid[j] != x) ++j;
                bit = (mask >> j) & 1u;
            }
            a[x] = bit ? -1 : 1;
        }
        for (int step = 1; step < N; step <<= 1) {
            for (int i = 0; i < N; i += 2 * step) {
                for (int j = 0; j < step; ++j) {
                    int u = a[i+j], v = a[i+j+step];
                    a[i+j] = u+v;
                    a[i+j+step] = u-v;
                }
            }
        }
        uint64_t l1 = 0;
        for (int x = 0; x < N; ++x) l1 += (uint64_t)abs(a[x]);
        if (l1 < best_l1) {
            best_l1 = l1;
            best_mask = mask;
        }
    }
    printf("minimum normalized Fourier l1: %.8f\n", (double)best_l1 / N);
    printf("middle vectors labeled 1:");
    for (int j = 0; j < M; ++j)
        if ((best_mask >> j) & 1u) printf(" %d", mid[j]);
    puts("");
    return 0;
}
