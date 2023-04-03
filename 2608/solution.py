import bisect
from collections import Counter, deque, defaultdict
from itertools import accumulate
from typing import List, Dict


INF = float('inf')

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
    def findShortestCycle(self, n: int, edges: List[List[int]]) -> int:
        graph = [[] for _ in range(n)]
        for u, v in set(map(tuple, edges)):
            graph[u].append(v)
            graph[v].append(u)
        
        min_cycle_dist = INF

        for i in range(n):
            par = [None] * n
            dist = [INF] * n
            dist[i] = 0

            q = [i]
            for u in q:
                for v in graph[u]:
                    if dist[v] == INF:
                        par[v] = u
                        dist[v] = dist[u] + 1
                        q.append(v)
                    elif par[v] != u and par[u] != v:
                        # encounter somewhere and is not immediate parent-children
                        # the nodes involved = dist[u] + dist[v] + 1
                        min_cycle_dist = min(min_cycle_dist, dist[u] + dist[v] + 1)
                        
        return min_cycle_dist if min_cycle_dist < INF else -1
