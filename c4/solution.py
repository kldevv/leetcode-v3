import bisect
import heapq
import math
from sortedcontainers import SortedList
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
    def minReverseOperations(self, n: int, p: int, banned: List[int], k: int) -> List[int]:
        def get_palidrome_index(start, length, i):
            # i + next_i = start + (start + length - 1)
            # next_i = start * 2 + length - 1 - i
            return start * 2 + length - 1 - i

        banned = set(banned)
        next_i_it = [SortedList(), SortedList()]
        for i in range(n):
            if i != p and i not in banned:
                next_i_it[i & 1].add(i)

        q = deque([p])
        min_ops = [-1] * n
        min_ops[p] = 0
        while q:
            for _ in range(len(q)):
                i = q.popleft()
                subarray_start_lo = max(i - k + 1, 0)
                next_i_lo = get_palidrome_index(subarray_start_lo, k, i)

                subarray_start_hi = min(i + k - 1, n - 1) - (k - 1)
                next_i_hi = get_palidrome_index(subarray_start_hi, k, i)

                for next_i in list(next_i_it[next_i_lo & 1].irange(next_i_lo, next_i_hi)):
                    min_ops[next_i] = min_ops[i] + 1
                    next_i_it[next_i_lo & 1].remove(next_i)
                    q.append(next_i)
        return min_ops
