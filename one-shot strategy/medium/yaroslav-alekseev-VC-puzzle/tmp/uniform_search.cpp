#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

int n=8,k=4;
vector<int> blocks, tris;
vector<vector<int>> covers;
vector<array<int,56>> trpat;
uint64_t nodes=0; int best=0; vector<int> bestsel;

bool dfs(uint64_t covered, array<unsigned char,56> masks, vector<int>& sel){
  nodes++;
  int cv=__builtin_popcountll(covered); if(cv>best){best=cv;bestsel=sel;cerr<<"best "<<best<<" rows "<<sel.size()<<" nodes "<<nodes<<"\n";}
  if(cv==56){cout<<"FOUND\n";for(int b:sel)cout<<blocks[b]<<' ';cout<<'\n';return true;}
  int pick=-1,opts=99;
  for(int t=0;t<56;t++)if(!(covered>>t&1)){
    int c=0;
    for(int b:covers[t]) {
      bool ok=true;
      for(int u=0;u<56;u++)if((masks[u]|(1<<trpat[b][u]))==255){ok=false;break;}
      if(ok)c++;
    }
    if(c<opts){opts=c;pick=t;if(!c)break;}
  }
  if(opts==0)return false;
  for(int b:covers[pick]){
    auto nm=masks; bool ok=true;
    for(int u=0;u<56;u++){nm[u]|=1<<trpat[b][u];if(nm[u]==255){ok=false;break;}}
    if(!ok)continue;
    uint64_t nc=covered;
    for(int t=0;t<56;t++)if((blocks[b]&tris[t])==tris[t])nc|=1ULL<<t;
    sel.push_back(b);
    if(dfs(nc,nm,sel))return true;
    sel.pop_back();
  }
  return false;
}
int main(){
 for(int x=0;x<(1<<n);x++){int c=__builtin_popcount((unsigned)x);if(c==k)blocks.push_back(x);if(c==3)tris.push_back(x);}
 covers.resize(56);trpat.resize(70);
 for(int b=0;b<70;b++)for(int t=0;t<56;t++){
  int p=0,q=0;for(int i=0;i<n;i++)if(tris[t]>>i&1){if(blocks[b]>>i&1)p|=1<<q;q++;}trpat[b][t]=p;
  if((blocks[b]&tris[t])==tris[t])covers[t].push_back(b);
 }
 // By symmetry include the first block 0123.
 int b0=0;array<unsigned char,56> masks{};uint64_t cov=0;
 for(int t=0;t<56;t++){masks[t]=1<<trpat[b0][t];if((blocks[b0]&tris[t])==tris[t])cov|=1ULL<<t;}
 vector<int> sel{b0}; bool f=dfs(cov,masks,sel);cerr<<"done "<<f<<" nodes "<<nodes<<" best "<<best<<"\n";
 cerr<<"best family:";for(int b:bestsel)cerr<<' '<<blocks[b];cerr<<"\n";
}
