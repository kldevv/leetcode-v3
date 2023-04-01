import bisect
from collections import Counter, deque
from itertools import accumulate, combinations
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


def generate_subsets(iterable, subset_size=None):
    if subset_size is None:
        # Generate all subset sizes
        for size in range(len(iterable) + 1):
            for subset in combinations(iterable, size):
                yield subset
    else:
        # Generate subsets of a specific size
        for subset in combinations(iterable, subset_size):
            yield subset

class Solution:
    def beautifulSubsets(self, nums: List[int], k: int) -> int:
        groups = [Counter() for _ in range(k)]
        for num in nums:
            groups[num % k][num] += 1
        
        susbet_cnt = 1
        for group in groups:
            # dp0 is the # of subsets without prev in it
            dp0 = 1
            # dp1 is the # of subsets with prev in it
            dp1 = 0
            prev = 0
            for a in sorted(group.keys()):
                v = pow(2, group[a])
                # if prev + k != a, we can combine dp0 and dp1 and add the current element to dp1
                # otherwise only add the current element to dp1
                # for the next element, the set without the current element is dp0 + dp1 regardless
                # similar to 198.
                if prev + k == a:
                    dp0, dp1 = dp0 + dp1, dp0 * (v - 1)
                else:
                    dp0, dp1 = dp0 + dp1, (dp0 + dp1) * (v - 1)
                prev = a
            # dp0 + dp1 is the all the valid sets in this group
            # valid sets in different group can be add combinatorially and still be valid
            susbet_cnt *= dp0 + dp1
        return susbet_cnt - 1
