#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

enum { N = 512, MAX_MID = 512 };
static uint64_t state = 0xa0761d6478bd642fULL;
static uint64_t rng64(void) { state ^= state << 7; state ^= state >> 9; return state; }
static int pc(unsigned x) { return __builtin_popcount(x); }
static int absi(int x) { return x < 0 ? -x : x; }
static long long transform(const int *v, int *w) {
    for (int x=0;x<N;++x) w[x]=v[x];
    for (int s=1;s<N;s<<=1) for (int i=0;i<N;i+=2*s) for (int j=0;j<s;++j) {
        int a=w[i+j],b=w[i+j+s]; w[i+j]=a+b; w[i+j+s]=a-b;
    }
    long long r=0; for(int i=0;i<N;++i) r+=absi(w[i]); return r;
}
int main(int argc,char **argv) {
    int seconds=argc>1?atoi(argv[1]):180, mid[MAX_MID], mc=0, v[N],w[N];
    for(int x=0;x<N;++x) if(4<=pc((unsigned)x)&&pc((unsigned)x)<=5) mid[mc++]=x;
    for(int x=0;x<N;++x) { int wt=pc((unsigned)x),bit=wt>=6||(4<=wt&&wt<=5&&pc((unsigned)x&0x7fU)>=4); v[x]=bit?-1:1; }
    long long cur=transform(v,w),best=cur; printf("initial normalized l1 %.9f, middle variables %d\n",(double)cur/N,mc); fflush(stdout);
    time_t start=time(NULL); unsigned long long it=0;
    while(time(NULL)-start<seconds) {
        int x=mid[rng64()%(unsigned)mc],old=v[x]; long long delta=0;
        for(int a=0;a<N;++a){int chi=(pc((unsigned)(a&x))&1)?-1:1; delta+=absi(w[a]-2*old*chi)-absi(w[a]);}
        if(delta<=0 || ((rng64()&((1U<<19)-1U))==0)) {
            v[x]=-old; for(int a=0;a<N;++a){int chi=(pc((unsigned)(a&x))&1)?-1:1;w[a]-=2*old*chi;} cur+=delta;
            if(cur<best){best=cur;printf("best normalized l1 %.9f after %llu iterations\n",(double)best/N,it);fflush(stdout);}
        }
        ++it;
    }
    printf("final best normalized l1 %.9f after %llu iterations\n",(double)best/N,it);
    return 0;
}
