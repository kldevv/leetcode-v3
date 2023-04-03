import bisect
from collections import Counter, deque
from itertools import accumulate
from typing import List, Dict, Iterable, Union


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

def get_median(nums: Iterable[Union[int, float]]) -> Union[int, float]:
    nums = sorted(nums)
    middle_index = len(nums) // 2

    # Check if the length of the list is odd or even
    if len(nums) % 2 == 0:
        # If the length of the list is even, calculate the average of the middle two values
        median = (nums[middle_index - 1] + nums[middle_index]) / 2
    else:
        # If the length of the list is odd, the median is the middle value
        median = nums[middle_index]
    return median



class Solution:
    def makeSubKSumEqual(self, arr: List[int], k: int) -> int:
        n = len(arr)
        visited = [False] * n
        groups = []
        for i in range(n):
            # a[i] == a[i+k], to make all subarray of length k sum to equal
            # group all the a[i], a[i+k], a[i+k*2],...a[i+k*n]
            if not visited[i]:
                visited[i] = True
                group = [arr[i]]
                j = (i + k) % n
                while j != i:
                    visited[j] = True
                    group.append(arr[j])
                    j = (j + k) % n
                groups.append(group)
         
        steps = 0
        for group in groups:
            # median is the target to make minimum adjustment for all elements
            m = int(get_median(group))
            steps += sum(abs(num - m) for num in group)
        return steps
