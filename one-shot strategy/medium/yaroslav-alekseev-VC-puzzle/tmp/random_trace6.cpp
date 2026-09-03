#include <array>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

int main(){
  std::vector<int> tri;
  for(int x=0;x<64;x++) if(__builtin_popcount((unsigned)x)==3) tri.push_back(x);
  std::array<std::array<uint64_t,8>,20> pm{};
  auto tr=[](int r,int t){int p=0,k=0; for(int i=0;i<6;i++)if(t>>i&1){if(r>>i&1)p|=1<<k;k++;}return p;};
  for(int t=0;t<20;t++)for(int r=0;r<64;r++)pm[t][tr(r,tri[t])]|=1ULL<<r;
  std::mt19937_64 gen(1234567);
  std::array<uint64_t,4> hist{};
  int good=0;
  for(int it=0;it<10000000;it++){
    uint64_t a=~0ULL;
    for(int t=0;t<20;t++)a &= ~pm[t][gen()%7];
    std::array<int,4> h{}; bool ok=true;
    for(int t=0;t<20;t++){
      int best=4;
      for(int r=0;r<64;r++)if((a>>r&1)&&(r&tri[t])==tri[t]) best=std::min(best,__builtin_popcount((unsigned)(r&~tri[t])));
      if(best==4){ok=false;break;} h[best]++;
    }
    if(ok){good++; uint64_t code=h[0]+21ULL*h[1]+441ULL*h[2]+9261ULL*h[3]; hist[0]=std::max(hist[0],code);
      if(good<=20)std::cout<<h[0]<<' '<<h[1]<<' '<<h[2]<<' '<<h[3]<<" rows "<<__builtin_popcountll(a)<<'\n';
    }
  }
  std::cerr<<"good "<<good<<"\n";
}
