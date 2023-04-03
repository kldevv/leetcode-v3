import bisect
from collections import Counter, deque
from itertools import accumulate
from typing import List, Dict


def generate_primes(n):
    # Create a boolean array "is_prime[0..n]" and initialize all entries as true.
    is_prime = [True for i in range(n+1)]
    p = 2
    while (p**2 <= n):
        # If is_prime[p] is not changed, then it is a prime
        if (is_prime[p] == True):
            # Update all multiples of p
            for i in range(p**2, n+1, p):
                is_prime[i] = False
        p += 1
    
    # Create a list of prime numbers up to n
    primes = []
    for p in range(2, n+1):
        if is_prime[p]:
            primes.append(p)
    
    return primes


class Solution:
    def minNumber(self, nums1: List[int], nums2: List[int]) -> int:
        s1 = set(nums1)
        s2 = set(nums2)

        if len(s1 & s2) > 0:
            return min(list(s1 & s2))

        m1 = min(nums1)
        m2 = min(nums2)
        if m1 > m2:
            return int(str(m2) + str(m1))
        return int(str(m1) + str(m2))
