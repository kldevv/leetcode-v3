import bisect
from collections import Counter, deque
from itertools import accumulate
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


class Solution:
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)
        
        graph = [set() for _ in range(n)]
        for u, v in edges:
            # undirected
            graph[u].add(v)
            graph[v].add(u)
        
        q = []
        for i, neighs in enumerate(graph):
            # collect leaves that has no coins
            if len(neighs) == 1 and coins[i] == 0:
                q.append(i)
        
        # recursively remove leaves, these are of no value
        removed_edges = 0
        for i in q:
            for neigh in graph[i]:
                graph[neigh].remove(i)
                # record how many edges we've removed
                removed_edges += 1
                if len(graph[neigh]) == 1 and coins[neigh] == 0:
                    q.append(neigh)
            graph[i].clear()
        
        # now all the leaves remain has coins
        # trim back additional grace levels, 2 in this case
        grace = 2
        for _ in range(grace):
            for i, neighs in enumerate(graph):
                if len(neighs) == 1:
                    q.append(i)
            for i in q:
                for neigh in graph[i]:
                    # record how many edges we've removed
                    graph[neigh].remove(i)
                    removed_edges += 1
                graph[i].clear()
        
        # total = n - 1 edges
        # remaind edges are to be travelled twice
        return (n - 1 - removed_edges) * 2
    