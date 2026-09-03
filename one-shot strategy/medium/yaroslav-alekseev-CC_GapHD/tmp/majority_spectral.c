#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    for (int n = 1; n <= 23; n += 2) {
        int N = 1 << n;
        int *a = malloc((size_t)N * sizeof(*a));
        for (int x = 0; x < N; ++x)
            a[x] = __builtin_popcount((unsigned)x) > n / 2 ? -1 : 1;
        for (int step = 1; step < N; step <<= 1)
            for (int i = 0; i < N; i += 2 * step)
                for (int j = 0; j < step; ++j) {
                    int u = a[i+j], v = a[i+j+step];
                    a[i+j] = u+v; a[i+j+step] = u-v;
                }
        double l1 = 0;
        for (int x = 0; x < N; ++x) l1 += fabs((double)a[x]) / N;
        printf("n=%d l1=%.9g\n", n, l1);
        free(a);
    }
    return 0;
}
