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
    def evenOddBit(self, n: int) -> List[int]:
        even = 0
        odd = 0
        count = 0
        while n:
            if count & 1:
                odd += (n & 1 == 1)
            else:
                even += (n & 1 == 1)
            count += 1
            n >>= 1
        return [even, odd]
