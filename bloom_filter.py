"""Bloom Filter — space-efficient probabilistic membership."""
import hashlib, math

class BloomFilter:
    def __init__(self, n, fp_rate=0.01):
        self.m = int(-n * math.log(fp_rate) / (math.log(2)**2))
        self.k = int(self.m / n * math.log(2))
        self.bits = bytearray(self.m // 8 + 1)
        self.count = 0
    def _hashes(self, item):
        for i in range(self.k):
            h = int(hashlib.md5(f"{item}:{i}".encode()).hexdigest(), 16)
            yield h % self.m
    def add(self, item):
        for h in self._hashes(item):
            self.bits[h // 8] |= 1 << (h % 8)
        self.count += 1
    def __contains__(self, item):
        return all(self.bits[h // 8] & (1 << (h % 8)) for h in self._hashes(item))

if __name__ == "__main__":
    bf = BloomFilter(10000, 0.01)
    for i in range(10000): bf.add(f"item-{i}")
    assert all(f"item-{i}" in bf for i in range(10000))
    fp = sum(1 for i in range(10000, 20000) if f"item-{i}" in bf)
    rate = fp / 10000
    print(f"Bloom: m={bf.m}, k={bf.k}, FP rate={rate:.4f}")
    assert rate < 0.02
    print("All tests passed!")
