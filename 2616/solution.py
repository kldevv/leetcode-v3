import bisect
import heapq
import math
from collections import Counter, deque, defaultdict
from itertools import accumulate
from functools import cache
from typing import List, Dict, Union, Any


INF = float('inf')

@cache
def generate_primes(n: Union[int, float]) -> List[int]:
    """
    Generates a list of prime numbers up to the given limit (inclusive).

    Args:
        n (Union[int, float]): The limit up to which prime numbers are to be generated.

    Returns:
        List[int]: A list of prime numbers up to the given limit (inclusive).
    """
    is_prime = [True for _ in range(n+1)]
    p = 2
    while (p**2 <= n):
        if (is_prime[p] == True):
            for i in range(p**2, n+1, p):
                is_prime[i] = False
        p += 1
    
    primes = []
    for p in range(2, n+1):
        if is_prime[p]:
            primes.append(p)
    
    return primes

@cache
def is_prime(n: Union[int, float]) -> bool:
    """
    Determines if the given number is a prime number.

    Args:
        n (Union[int, float]): The number to be checked for primality.

    Returns:
        bool: True if the input number is prime, False otherwise.
    """
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0 or isinstance(n, float):
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_square_matrix(matrix: List[List[Any]]) -> bool:
    """
    Determines if a given list of lists represents a square matrix.

    Args:
        matrix (List[List[Any]): The list of lists to be checked.

    Returns:
        bool: True if the input represents a square matrix, False otherwise.
    """
    row_length = len(matrix)
    for row in matrix:
        if len(row) != row_length:
            return False

    return True


class Solution:
    def minimizeMax(self, nums: List[int], p: int) -> int:
        def is_valid(m, p):
            i = 1
            while i < len(nums):
                if nums[i] - nums[i-1] <= m:
                    # greedily take nums[i] - nums[i-1] if it's lower than m
                    # if take nums[i] - nums[i-1], consider nums[i+2] - nums[i+1]
                    # otherwise, consider nums[i+1] - nums[i]
                    p -= 1
                    i += 2
                else:
                    i += 1
            return p <= 0
                

        if p == 0 or p > len(nums) // 2:
            return 0
        
        nums = sorted(nums)

        l = 0
        u = nums[-1] - nums[0]
        while l < u:
            m = (u + l) // 2
            if is_valid(m, p):
                u = m
            else:
                l = m + 1
        return l
