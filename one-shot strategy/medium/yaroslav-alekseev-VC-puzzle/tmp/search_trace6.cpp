#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

// Search over one selected forbidden trace on every 3-subset of [6].  Once
// forbidden traces are fixed, all 6-bit rows avoiding them may be included.
// We maximize the number of allowed rows of Hamming weight exactly three,
// subject to retaining a 111 witness for every triple.

std::vector<int> triples;
std::array<std::array<uint64_t,8>,20> patmask{};
std::array<std::vector<int>,20> witnesses;
int best = -1;
std::array<int,20> best_forbid{};
uint64_t nodes = 0;

int trace(int row, int tri) {
  int p=0, k=0;
  for(int i=0;i<6;i++) if((tri>>i)&1) {
    if((row>>i)&1) p |= 1<<k;
    ++k;
  }
  return p;
}

void dfs(int depth, uint64_t allowed, std::array<int,20>& forbid) {
  ++nodes;
  // Every triple must still possess an allowed row containing it.
  for(int t=0;t<20;t++) {
    bool ok=false;
    for(int r:witnesses[t]) if((allowed>>r)&1ULL) {ok=true;break;}
    if(!ok) return;
  }
  if(depth==20) {
    int val=0;
    for(int r=0;r<64;r++) if(((allowed>>r)&1ULL) && __builtin_popcount((unsigned)r)==3) ++val;
    if(val>best) { best=val; best_forbid=forbid; std::cerr<<"best "<<best<<" nodes "<<nodes<<"\n"; }
    return;
  }
  // Pick the unassigned triple/pattern branch producing the strongest pruning.
  int t=depth;
  // 111 cannot be forbidden because every triple must be covered.
  std::vector<std::pair<int,uint64_t>> opts;
  for(int p=0;p<7;p++) {
    uint64_t next=allowed & ~uint64_t(patmask[t][p]);
    opts.push_back({p,next});
  }
  std::sort(opts.begin(),opts.end(),[](auto a,auto b){return __builtin_popcountll(a.second)<__builtin_popcountll(b.second);});
  for(auto [p,next]:opts) { forbid[t]=p; dfs(depth+1,next,forbid); }
}

int main(){
  for(int x=0;x<64;x++) if(__builtin_popcount((unsigned)x)==3) triples.push_back(x);
  for(int t=0;t<20;t++) {
    for(int r=0;r<64;r++) {
      int p=trace(r,triples[t]);
      patmask[t][p] |= (1ULL<<r);
      if((r&triples[t])==triples[t]) witnesses[t].push_back(r);
    }
  }
  std::array<int,20> f{};
  dfs(0,~0ULL,f);
  std::cout<<"best="<<best<<" nodes="<<nodes<<"\nforbidden:";
  for(int x:best_forbid) std::cout<<' '<<x;
  std::cout<<'\n';
}
