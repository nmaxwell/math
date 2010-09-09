#include <stdio.h>
#include <vector>

using namespace std;

typedef unsigned long long int uint64; 
typedef unsigned int uint32;

inline uint64 bit(const uint64 & x, const uint64 & j) {
  return (x & ((uint64)1<<j))>>j;
}

vector<uint64> all_seed_sets(uint64 n) {
  
  vector<uint64> acc;
  
  uint64 K = (uint64)1 << n;
  uint64 M = (uint64)1 << ((uint64)1<<n);
  
  for (uint64 m=0; m<M; m++) {
    
    uint64 U=0;
    for (uint64 k=0; k<K; k++)
      if (bit(m,k)) U |= k;
    
    if (U == ((uint64)1<<n)-(uint64)1)
      acc.push_back(m);
  }
  
  return acc;
}


inline char count_bits_set(const uint64 &x)
{
  char c=0;
  for (char j=0; j<64; j++)
    c += (x >> j)&1;
  return c;
}








uint64 gen_topology(uint64 E)
{
  char L = count_bits_set(E);
  
  for (char k=0; k<((uint64)1 << L); k++) {
    
  }
}




int main() {
  
  int disp = 1;
  int n = 3;
  
  if (disp) {
    for (int j=0; j<n; j++) {
      for (int k=(1<<n)-1; k>=0; k--)
	if (bit(k,j)) printf("1");
	else printf("0");
      printf("\n"); }
    
    for (int k=0; k<(1<<n); k++)
      printf("-");
    printf("\n");
  }
  
  vector<uint64> unions = all_seed_sets(n);
  
  if (disp) {
    int disp2 = unions.size();
    
    for (int j=0; j<disp2; j++) {
      uint64 x = unions[j];
      
      for (int k=(1<<n)-1; k>=0; k--)
	if (bit(x,k)) printf("1");
	else printf("0");
      printf("\n");
    }
  }
  
  return 0;
}









