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
    def minimumVisitedCells(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        next_j = [SortedList(range(n)) for _ in range(m)]
        next_i = [SortedList(range(m)) for _ in range(n)]

        q = deque([(0, 0, 1)])
        while q:
            i, j, move = q.popleft()
            if i == m-1 and j == n-1:
                return move
            
            dx = grid[i][j]
            for kj in list(next_j[i].irange(j+1, min(j+1+dx, n)-1)):
                q.append((i, kj, move+1))
                next_j[i].remove(kj)
                next_i[kj].remove(i)
            for ki in list(next_i[j].irange(i+1, min(i+1+dx, m)-1)):
                q.append((ki, j, move+1))
                next_j[ki].remove(j)
                next_i[j].remove(ki)

        return -1
