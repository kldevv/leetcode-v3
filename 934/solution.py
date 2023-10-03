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
    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)
        queue = deque([])

        def dfs(i, j):
            grid[i][j] = -1
            queue.append((i, j))
            for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                if 0 <= x < n and 0 <= y < n and grid[x][y] == 1:
                    dfs(x, y)

        def find_first_land():
            for i in range(n):
                for j in range(n):
                    if grid[i][j] == 1:
                        return i, j

        # mark the 1st island `-1` to tell the difference between the 2nd island
        # while also pushing the 1st island lands to the queue
        dfs(*find_first_land())

        step = 0

        while queue:
            m = len(queue)
            for _ in range(m):
                i, j = queue.popleft()
                for x, y in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
                    if 0 <= x < n and 0 <= y < n:
                        if grid[x][y] == 1:
                            return step
                        if grid[x][y] == 0:
                            # mark the visited sea `-1` to avoid it being visiting twice
                            grid[x][y] = -1
                            queue.append((x, y))
            # increase the bridge length by 1
            step += 1

        return -1
