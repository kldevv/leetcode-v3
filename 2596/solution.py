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
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        # if doesn't start with top-left most cell
        if grid[0][0] != 0:
            return False
        
        n = len(grid)
        dest =  [(None, None)] * (n * n)
        for i in range(n):
            for j in range(n):
                # at grid[i][j] step, it should be at (i, j) cell
                dest[grid[i][j]] = (i, j)
        
        for i in range(1, n * n):
            prev_cell = dest[i-1]
            cur_cell = dest[i]
            # if there is no cell assign to i step
            if not cur_cell:
                return False
            dx = abs(cur_cell[0] - prev_cell[0])
            dy = abs(cur_cell[1] - prev_cell[1])
            # also goes diagonally with 1, 2 delta
            if dx * dy != 2:
                return False
        return True
