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
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        nums.sort()

        range_sum = [0] + list(accumulate(nums))
        total = sum(nums)
        
        min_operations = [0] * len(queries)
        for i, query in enumerate(queries):
            # j elements smaller than query
            j = bisect.bisect_left(nums, query)
            # needs increment steps for them to match query
            increments = query * j - range_sum[j]
            # k elements larger than or equal to query
            k = len(nums) - j
            # needs decrement steps for them to match query
            decrements = (total - range_sum[j]) - query * k

            min_operations[i] = increments + decrements

        return min_operations
