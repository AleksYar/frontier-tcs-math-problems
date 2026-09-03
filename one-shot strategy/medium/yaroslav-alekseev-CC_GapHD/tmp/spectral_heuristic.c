#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum { N = 256, MAX_MID = 256 };

static uint64_t state = 0x9e3779b97f4a7c15ULL;
static uint64_t rng64(void) {
    state ^= state << 7;
    state ^= state >> 9;
    return state;
}

static int pc(unsigned x) { return __builtin_popcount(x); }
static int iabs(int x) { return x < 0 ? -x : x; }

static long long transform(const int *value, int *walsh) {
    for (int x = 0; x < N; ++x) walsh[x] = value[x];
    for (int step = 1; step < N; step <<= 1)
        for (int i = 0; i < N; i += 2 * step)
            for (int j = 0; j < step; ++j) {
                int u = walsh[i+j], v = walsh[i+j+step];
                walsh[i+j] = u+v;
                walsh[i+j+step] = u-v;
            }
    long long l1 = 0;
    for (int a = 0; a < N; ++a) l1 += iabs(walsh[a]);
    return l1;
}

static void initialize(int *value, const int *middle, int middle_count, int mode) {
    for (int x = 0; x < N; ++x) {
        int weight = pc((unsigned)x);
        int bit;
        if (weight <= 2) bit = 0;
        else if (weight >= 6) bit = 1;
        else if (mode == 0) bit = pc((unsigned)x & 0x1fU) >= 3;
        else if (mode == 1) bit = weight >= 4;
        else bit = (int)(rng64() & 1U);
        value[x] = bit ? -1 : 1;
    }
    (void)middle;
    (void)middle_count;
}

int main(int argc, char **argv) {
    int seconds = argc > 1 ? atoi(argv[1]) : 60;
    int middle[MAX_MID], middle_count = 0;
    int value[N], walsh[N], best_value[N];
    for (int x = 0; x < N; ++x) {
        int w = pc((unsigned)x);
        if (3 <= w && w <= 5) middle[middle_count++] = x;
    }

    initialize(value, middle, middle_count, 0);
    long long current = transform(value, walsh), best = current;
    for (int x = 0; x < N; ++x) best_value[x] = value[x];
    printf("initial normalized l1 %.9f, middle variables %d\n",
           (double)current / N, middle_count);
    fflush(stdout);

    time_t start = time(NULL), last_report = start;
    unsigned long long iterations = 0;
    while (time(NULL) - start < seconds) {
        int x = middle[rng64() % (unsigned)middle_count];
        int old_value = value[x];
        long long delta = 0;
        for (int a = 0; a < N; ++a) {
            int chi = (pc((unsigned)(a & x)) & 1) ? -1 : 1;
            int next = walsh[a] - 2 * old_value * chi;
            delta += iabs(next) - iabs(walsh[a]);
        }
        int accept = delta <= 0;
        if (!accept && (rng64() & ((1U << 18) - 1U)) == 0) accept = 1;
        if (accept) {
            value[x] = -old_value;
            for (int a = 0; a < N; ++a) {
                int chi = (pc((unsigned)(a & x)) & 1) ? -1 : 1;
                walsh[a] -= 2 * old_value * chi;
            }
            current += delta;
            if (current < best) {
                best = current;
                for (int z = 0; z < N; ++z) best_value[z] = value[z];
                printf("best normalized l1 %.9f after %llu iterations\n",
                       (double)best / N, iterations);
                fflush(stdout);
            }
        }
        ++iterations;
        if (iterations % 2000000ULL == 0 && time(NULL) != last_report) {
            last_report = time(NULL);
            if ((rng64() & 15U) == 0) {
                initialize(value, middle, middle_count, 2);
                current = transform(value, walsh);
            }
        }
    }
    printf("final best normalized l1 %.9f after %llu iterations\n",
           (double)best / N, iterations);
    printf("best middle-one vectors:");
    for (int j = 0; j < middle_count; ++j)
        if (best_value[middle[j]] == -1) printf(" %d", middle[j]);
    puts("");
    return 0;
}
