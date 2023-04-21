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

class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        adj_list = [[] for _ in range(n)]
        for cur_node, neigh_node in edges:
            adj_list[cur_node].append(neigh_node)
            adj_list[neigh_node].append(cur_node)
        
        
        def find_pass_by_nodes(start_node, end_node, passed_by_nodes_occur):
            def back_track(cur_node, par_node):
                passed_by_nodes_occur[cur_node] += 1

                if cur_node == end_node:
                    return True

                for neigh_node in adj_list[cur_node]:
                    if neigh_node != par_node:
                        if back_track(neigh_node, cur_node):
                            return True
                        passed_by_nodes_occur[neigh_node] -= 1

            back_track(start_node, None)


        passed_by_nodes_occur = [0] * n
        for start_node, end_node in trips:
            find_pass_by_nodes(start_node, end_node, passed_by_nodes_occur)
        
        @cache
        def alt_reduce(cur_node, par_node, selectable):
            cost = price[cur_node] * passed_by_nodes_occur[cur_node]
            reduce_cost = cost // 2 if selectable else INF

            for neigh_node in adj_list[cur_node]:
                if neigh_node != par_node:
                    if selectable:
                        reduce_cost += alt_reduce(neigh_node, cur_node, False)
                    cost += alt_reduce(neigh_node, cur_node, True)
            
            return min(reduce_cost, cost)
        
        return min(alt_reduce(0, None, True), alt_reduce(0, None, False))
