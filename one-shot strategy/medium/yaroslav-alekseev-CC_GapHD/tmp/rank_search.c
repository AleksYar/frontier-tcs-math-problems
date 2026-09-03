#include <stdio.h>
#include <stdint.h>

static int pc(unsigned x) { return __builtin_popcount(x); }

int main(void) {
    enum { n = 6, N = 64, M = 20 };
    int mid[M], m = 0, a[N], best_a[N];
    unsigned best_mask = 0;
    int best = N + 1, count_best = 0;
    for (int x = 0; x < N; ++x) if (pc((unsigned)x) == 3) mid[m++] = x;
    for (unsigned mask = 0; mask < (1u << M); ++mask) {
        for (int x = 0; x < N; ++x) {
            int bit = pc((unsigned)x) >= 4;
            if (pc((unsigned)x) == 3) {
                int j = 0; while (mid[j] != x) ++j;
                bit = (mask >> j) & 1u;
            }
            a[x] = bit ? -1 : 1;
        }
        for (int step = 1; step < N; step <<= 1) {
            for (int i = 0; i < N; i += 2 * step) {
                for (int j = 0; j < step; ++j) {
                    int u = a[i+j], v = a[i+j+step];
                    a[i+j] = u+v; a[i+j+step] = u-v;
                }
            }
        }
        int support = 0;
        for (int x = 0; x < N; ++x) support += a[x] != 0;
        if (support < best) {
            best = support; best_mask = mask; count_best = 1;
            for (int x = 0; x < N; ++x) best_a[x] = a[x];
        } else if (support == best) ++count_best;
    }
    printf("minimum Walsh support / exact XOR-matrix rank: %d\n", best);
    printf("number attaining minimum: %d\n", count_best);
    printf("middle vectors labeled 1:");
    for (int j = 0; j < M; ++j) if ((best_mask >> j) & 1u) printf(" %d", mid[j]);
    printf("\nnonzero coefficients by Fourier degree:");
    for (int d = 0; d <= n; ++d) {
        int c = 0; for (int x = 0; x < N; ++x) c += best_a[x] != 0 && pc((unsigned)x) == d;
        printf(" %d:%d", d, c);
    }
    puts("");
    return 0;
}
