#!/usr/bin/env python3
"""Bloom filter — space-efficient probabilistic set membership."""
import hashlib,math
class BloomFilter:
    def __init__(self,n,fp_rate=0.01):
        self.m=int(-n*math.log(fp_rate)/(math.log(2)**2));self.k=int(self.m/n*math.log(2))
        self.bits=[False]*self.m
    def _hashes(self,item):
        h1=int(hashlib.md5(str(item).encode()).hexdigest(),16)
        h2=int(hashlib.sha1(str(item).encode()).hexdigest(),16)
        return [(h1+i*h2)%self.m for i in range(self.k)]
    def add(self,item):
        for h in self._hashes(item): self.bits[h]=True
    def __contains__(self,item):
        return all(self.bits[h] for h in self._hashes(item))
def main():
    bf=BloomFilter(1000);[bf.add(i) for i in range(100)]
    print(f"50 in bf: {50 in bf}, 500 in bf: {500 in bf}")
if __name__=="__main__":main()
