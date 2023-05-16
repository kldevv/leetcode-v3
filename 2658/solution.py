import bisect
import heapq
import math
from sortedcontainers import SortedList
from collections import Counter, deque, defaultdict
from itertools import accumulate
from functools import cache, wraps
from typing import List, Dict, Union, Any, Optional, Callable, Iterable, Set, Tuple


INF = float('inf')
PI = 3.14159

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children != None else []

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

@cache
def gcd(a: int, b: int) -> int:
    """
    Returns the Greatest Common Divisor (GCD) of two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The GCD of `a` and `b`.
    """
    while b:
        a, b = b, a % b
    return a

class Solution:
    def findMaxFish(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0]) if m else 0

        def dfs(r, c, visited):
            cur_max_fish = grid[r][c]
            visited.add((r, c))
            for rr in [r+1, r-1]:
                if rr >= 0 and rr < m and grid[rr][c] > 0 and (rr, c) not in visited:
                    cur_max_fish += dfs(rr, c, visited)
            
            for cc in [c+1, c-1]:
                if cc >= 0 and cc < n and grid[r][cc] > 0 and (r, cc) not in visited:
                    cur_max_fish += dfs(r, cc, visited)

            return cur_max_fish
        
        max_fish = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] > 0:
                    max_fish = max(max_fish, dfs(r, c, set()))

        return max_fish
