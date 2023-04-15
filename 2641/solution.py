import bisect
import heapq
import math
from sortedcontainers import SortedList
from collections import Counter, deque, defaultdict
from itertools import accumulate
from functools import cache, wraps
from typing import List, Dict, Union, Any, Optional, Callable, Iterable, Set, Tuple


INF = float('inf')

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

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

def deserialize_leetcode_tree(data: List[Union[int, None]]) -> Optional[TreeNode]:
    """
    Deserializes a LeetCode-style tree input into a TreeNode structure.
    
    Args:
        data (List[Union[int, None]]): A list of integers and None values representing a level-order traversal of a binary tree.
    
    Returns:
        TreeNode: The root of the deserialized binary tree, or None if the input list is empty or contains only None values.
    """
    if not data or data[0] is None:
        return None

    root = TreeNode(data[0])
    queue = deque([root])
    index = 1

    while queue and index < len(data):
        current = queue.popleft()

        if data[index] is not None:
            current.left = TreeNode(data[index])
            queue.append(current.left)
        index += 1

        if index < len(data) and data[index] is not None:
            current.right = TreeNode(data[index])
            queue.append(current.right)
        index += 1

    return root

def serialize_leetcode_tree(root: TreeNode) -> List[Union[int, None]]:
    """
    Serializes a TreeNode structure into a LeetCode-style tree input.
    
    Args:
        root (TreeNode): The root of the binary tree to be serialized.
    
    Returns:
        List[Union[int, None]]: A list of integers and None values representing a level-order traversal of the input binary tree.
    """
    if root is None:
        return []

    result = []
    queue = deque([root])

    while queue:
        current = queue.popleft()

        if current:
            result.append(current.val)
            queue.append(current.left)
            queue.append(current.right)
        else:
            result.append(None)

    # Remove trailing None values
    while result and result[-1] is None:
        result.pop()

    return result

def tree_convertor(deserialize_input_params: Optional[Set[str]] = {'root'}, serialize_output_params: Optional[Set[int]] = None) -> Callable[..., List[Union[int, None]]]:
    """
    Decorator to convert a LeetCode-style serialized tree input into a deserialized tree before calling the target function,
    and to convert the target function's output into a serialized tree.
    
    Args:
        deserialize_input_params (Optional[Set[str]]): A set of parameter names to deserialize from the input kwargs.
            If None, no parameters will be deserialized.
            Default is {'root'}.
        serialize_output_params (Optional[Set[int]]): A set of indices of the output tuple to serialize to LeetCode-style.
            If None, no output will be serialized.
            Default is None.

    Returns:
        A wrapped function that takes serialized tree inputs and returns serialized tree outputs.
    """
    
    def decorator(func: Callable[..., TreeNode]) -> Callable[..., List[Union[int, None]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> List[Union[int, None]]:
            if deserialize_input_params:
                deserialize_kwargs = {k: deserialize_leetcode_tree(kwargs[k]) for k in deserialize_input_params}
            kwargs.update(deserialize_kwargs)
            
            result = func(*args, **kwargs)

            if serialize_output_params and isinstance(result, Tuple):
                result = tuple(serialize_leetcode_tree(result[i]) if i in serialize_output_params else result[i] for i in range(len(result)))
            elif serialize_output_params == {0}:
                result = serialize_leetcode_tree(result)
            return result
        
        return wrapper
    
    return decorator

class Solution:
    @tree_convertor(deserialize_input_params={'root'}, serialize_output_params={0})
    def replaceValueInTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        p = {root: None}
        q = deque([root])
        vals = defaultdict(int)
        last_floor_sum = 0
        while q:
            floor_sum = 0
            for _ in range(len(q)):
                node = q.popleft()
                
                if node.right:
                    q.append(node.right)
                    p[node.right] = node
                    vals[node] += node.right.val
                    floor_sum += node.right.val
                if node.left:
                    q.append(node.left)
                    p[node.left] = node
                    vals[node] += node.left.val
                    floor_sum += node.left.val
                
                node.val = last_floor_sum - vals[p[node]]
            last_floor_sum = floor_sum
        return root