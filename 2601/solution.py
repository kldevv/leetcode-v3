import bisect
import collections
from collections.abc import Iterable


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
    def primeSubOperation(self, nums: Iterable[int]) -> bool:
        primes = generate_primes(max(nums))

        for i in range(len(nums)-2, -1, -1):
            if nums[i] >= nums[i+1]:
                prime_offset_idx = bisect.bisect_right(primes, nums[i]-nums[i+1])
                if prime_offset_idx == len(primes) or primes[prime_offset_idx] >= nums[i]:
                    return False
                nums[i] -= primes[prime_offset_idx]
        
        return True