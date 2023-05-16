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
    def minimumCost(self, start: List[int], target: List[int], specialRoads: List[List[int]]) -> int:
        # filter useful spec roads
        spec_road = [((x1, y1), (x2, y2), cost) for x1, y1, x2, y2, cost in specialRoads if cost < abs(x1-x2)+abs(y1-y2)]

        # optimized dist to end of spec roads
        dist = defaultdict(lambda : INF)
        dist[(0, 0)] = 0

        min_queue = [(0, start)]
        # dijskra, update all nodes' dist
        while min_queue:
            # cur_cost: dist from 0 to cur(x, y)
            cur_cost, (x, y) = heapq.heappop(min_queue)
            for (x1, y1), (x2, y2), cost in spec_road:
                # if cur optimized dist to end of spec roads is less ideal than go to start and use the special road to end
                # lhs: cur optimized dist from 0 to end
                # rhs: dist from 0 to cur(x, y), then go to start, use special road
                if dist[(x2, y2)] > abs(x-x1) + abs(y-y1) + cur_cost + cost:
                    dist[(x2, y2)] = abs(x-x1) + abs(y-y1) + cur_cost + cost
                    # 'cause source node is updated, we need to update its casual paths
                    heapq.heappush(min_queue, (dist[(x2, y2)], (x2, y2)))
        
        shrt_dist = abs(start[0]-target[0]) + abs(start[1]-target[1])
        for (x1, y1), (x2, y2), _ in spec_road:
            # update if go to end and go from end to target is more ideal
            shrt_dist = min(shrt_dist, dist[(x2, y2)] + abs(target[0]-x2) + abs(target[1]-y2))
        return shrt_dist
