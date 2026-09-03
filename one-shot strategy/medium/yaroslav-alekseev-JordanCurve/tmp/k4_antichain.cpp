#include <algorithm>
#include <cstdint>
#include <iostream>
#include <unordered_set>
#include <vector>

// Diagnostic solver for the full-block existential k-pebble game.
// A packed position uses 12 bits per (variable,value) assignment (7 for a
// variable index and 5 for a D<=5 grid value), plus size.
struct Solver {
  int D, M, V, Q, k;
  std::vector<std::vector<int>> vals;
  std::vector<std::unordered_set<uint64_t>> win;

  uint64_t pack(const std::vector<std::pair<int,int>>& t) const {
    uint64_t z=t.size(); int sh=3;
    for (auto [x,a]:t) { z |= uint64_t((x<<5)|a)<<sh; sh+=12; }
    return z;
  }
  bool okpair(int i,int a,int j,int b) const {
    if(i>j){std::swap(i,j);std::swap(a,b);}
    if(((i<M)==(j<M)) && j==i+1){
      int x=a/D,y=a%D,u=b/D,v=b%D;
      return std::abs(x-u)+std::abs(y-v)<=1;
    }
    if(i<M && j>=M) return a!=b;
    return true;
  }
  bool consistent(const std::vector<std::pair<int,int>>& t,int x,int a) const {
    for(auto [i,b]:t) if(!okpair(i,b,x,a)) return false;
    return true;
  }
  bool winning_subset(const std::vector<std::pair<int,int>>& t) const {
    int n=t.size();
    for(int mask=0;mask<(1<<n);++mask){
      std::vector<std::pair<int,int>> s;
      for(int i=0;i<n;++i) if(mask>>i&1) s.push_back(t[i]);
      // A query from a (k-1)-block position momentarily creates k blocks,
      // but the game must forget back below k before the next query.  We only
      // store winning bases of size < k, so skip the unforgotten full subset.
      if(s.size()<win.size() && win[s.size()].count(pack(s))) return true;
    }
    return false;
  }
  bool response_winning(const std::vector<std::pair<int,int>>& t,int x,int a) const {
    std::vector<std::pair<int,int>> u=t; u.push_back({x,a});
    std::sort(u.begin(),u.end());
    return winning_subset(u);
  }
  bool becomes_winning(const std::vector<std::pair<int,int>>& t) const {
    if(winning_subset(t)) return false;
    std::vector<char> used(V,false); for(auto [x,a]:t) used[x]=true;
    for(int x=0;x<V;++x) if(!used[x]){
      bool all=true, any=false;
      for(int a:vals[x]) if(consistent(t,x,a)){
        any=true;
        if(!response_winning(t,x,a)){all=false;break;}
      }
      if(all) return true; // includes no legal response
    }
    return false;
  }
  std::vector<std::pair<int,int>> unpack(uint64_t z) const {
    int n=z&7; z>>=3;
    std::vector<std::pair<int,int>> t;
    for(int i=0;i<n;++i){
      int p=z&4095; z>>=12;
      t.push_back({p>>5,p&31});
    }
    return t;
  }
  void prune_nonminimal(){
    for(int s=1;s<k;++s){
      for(auto it=win[s].begin();it!=win[s].end();){
        auto t=unpack(*it); bool redundant=false;
        int n=t.size();
        for(int mask=0;mask<(1<<n)-1 && !redundant;++mask){
          std::vector<std::pair<int,int>> u;
          for(int i=0;i<n;++i) if(mask>>i&1) u.push_back(t[i]);
          redundant=win[u.size()].count(pack(u));
        }
        if(redundant) it=win[s].erase(it); else ++it;
      }
    }
  }
  void enumerate(int target,int start,std::vector<std::pair<int,int>>& t,
                 std::vector<uint64_t>& add) const {
    if((int)t.size()==target){ if(becomes_winning(t)) add.push_back(pack(t)); return; }
    for(int x=start;x<V;++x) for(int a:vals[x]) if(consistent(t,x,a)){
      t.push_back({x,a}); enumerate(target,x+1,t,add); t.pop_back();
    }
  }
  void run(){
    V=2*M;Q=D*D;vals.assign(V,{});
    for(int x=0;x<V;++x){
      if(x==0) vals[x]={0};
      else if(x==M-1) vals[x]={Q-1};
      else if(x==M) vals[x]={D-1};
      else if(x==2*M-1) vals[x]={D*(D-1)};
      else for(int a=0;a<Q;++a) vals[x].push_back(a);
    }
    win.resize(k);
    for(int round=1;round<=200;++round){
      std::vector<std::pair<int,int>> t;
      size_t fresh=0;
      // Insert smaller bases before enumerating larger positions in the same
      // round, so supersets are never recorded as minimal bases.
      for(int s=0;s<k;++s){
        std::vector<uint64_t> add;
        enumerate(s,0,t,add);
        for(auto z:add) fresh+=win[s].insert(z).second;
      }
      prune_nonminimal();
      size_t total=0;for(auto& h:win)total+=h.size();
      std::cout<<"round "<<round<<" fresh "<<fresh<<" bases "<<total;
      for(int s=0;s<k;++s)std::cout<<" b"<<s<<"="<<win[s].size();
      std::cout<<std::endl;
      if(win[0].count(0)){std::cout<<"SPOILER WINS\n";return;}
      if(!fresh){std::cout<<"DUPLICATOR SURVIVES\n";return;}
    }
  }
};
int main(int argc,char**argv){
  Solver s; s.D=argc>1?std::stoi(argv[1]):4; s.M=argc>2?std::stoi(argv[2]):12;
  s.k=argc>3?std::stoi(argv[3]):4; s.run();
}
