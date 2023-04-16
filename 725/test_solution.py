from typing import List, Any, Iterable, Union, Set, Callable, Optional
from functools import wraps
from collections import deque

import pytest

import solution

'''
CLASSES
'''
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

'''
SERIALIZATION
'''
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

def serialize_leetcode_linked_list(head: ListNode) -> List[Union[int, None]]:
    """
    Serialize a linked list into a list of integers and None values in LeetCode-style.

    Args:
        head (ListNode): The head of the linked list.

    Returns:
        List[Union[int, None]]: The serialized linked list.
    """
    serialized = []
    current = head
    while current:
        serialized.append(current.val)
        current = current.next
    return serialized

def deserialize_leetcode_linked_list(serialized: List[Union[int, None]]) -> ListNode:
    """
    Deserialize a list of integers and None values into a linked list in LeetCode-style.

    Args:
        serialized (List[Union[int, None]]): The serialized linked list.

    Returns:
        ListNode: The deserialized linked list.
    """
    if not serialized:
        return None
    nodes = deque(ListNode(val=val) if val is not None else None for val in serialized)
    head = nodes.popleft()
    current = head
    while nodes:
        node = nodes.popleft()
        current.next = node
        current = node
    return head

def tree_serialization(deserialize_input_params: Optional[Set[str]] = {'root'}, enabled: bool = True) -> Callable[..., List[Union[int, None]]]:
    """
    Decorator to convert a LeetCode-style serialized tree_adaptor input into a deserialized tree before calling the target function,
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
        if enabled:
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Union[int, None]]:
                for k in deserialize_input_params:
                    if k in kwargs:
                        kwargs[k] = deserialize_leetcode_tree(kwargs[k])
                
                result = func(*args, **kwargs)

                def serialize_tree(result):
                    if isinstance(result, Optional[TreeNode]):
                        return serialize_leetcode_tree(result)
                    elif isinstance(result, tuple):
                        return tuple(serialize_tree(v) for v in result)
                    elif isinstance(result, list):
                        return [serialize_tree(v) for v in result]
                    elif isinstance(result, set):
                        return set(serialize_tree(v) for v in result)
                    else:
                        return result
                return serialize_tree(result)
            
            return wrapper
        else:
            return func

    return decorator

def sll_serialization(deserialize_input_params: Union[Set[str], List[str], None] = {'head'}, enabled: bool = False) -> Callable[..., List[Union[int, None]]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., List[Union[int, None]]]:
        if enabled:
            @wraps(func)
            def wrapper(*args, **kwargs) -> List[Union[int, None]]:
                for k in deserialize_input_params:
                    if k in kwargs:
                        kwargs[k] = deserialize_leetcode_linked_list(kwargs[k])

                result = func(*args, **kwargs)

                def serialize_linked_lists(result):
                    if isinstance(result, Optional[ListNode]):
                        return serialize_leetcode_linked_list(result)
                    elif isinstance(result, tuple):
                        return tuple(serialize_linked_lists(v) for v in result)
                    elif isinstance(result, list):
                        return [serialize_linked_lists(v) for v in result]
                    elif isinstance(result, set):
                        return set(serialize_linked_lists(v) for v in result)
                    else:
                        return result
                return serialize_linked_lists(result)
            return wrapper
        else:
            return func
        
    return decorator

def serialization(func):
    @tree_serialization(enabled=True)
    @sll_serialization(enabled=True)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

'''
UTILS
'''
def recursive_sorted(arr: List[Any]) -> List[Any]:
    """
    Sorts a list of lists recursively.
    
    Args:
        arr: A list of any types and/or sub-lists.
    
    Returns:
        A sorted list of any types and/or sub-lists.
    """
    if isinstance(arr[i], Iterable):
        for i in range(len(arr)):
                arr[i] = recursive_sorted(arr[i])
        return sorted(arr)
    return arr

def execu(input_case):
    obj = solution.Solution()
    func = [x for x in dir(obj) if '__' not in x][0]

    output = eval(f'serialization(obj.{func})({input_case})')
    return output


'''
LOAD CASES
'''
INPUT_CASES_PATH = r'./input.txt'
EXPECTED_CASES_PATH = r'./expected.txt'

def read_cases(path: str) -> List[str]:
    cases = []
    with open(path, 'r') as f:
        for line in f:
            cases.append(line.strip().replace('\n', '').replace('null', 'None'))
    return cases

input_cases = read_cases(INPUT_CASES_PATH)
expected_cases = read_cases(EXPECTED_CASES_PATH)


'''
TEST
'''
def test_target_function_exist_and_unique():
    obj = solution.Solution()
    public_functions = [x for x in dir(obj) if '__' not in x]
    assert len(public_functions) == 1

def test_cases_length_match():
    assert len(expected_cases) == len(input_cases)

@pytest.mark.parametrize("input_case, expected_case", zip(input_cases, expected_cases))
def test_ordered_output(input_case, expected_case):
    output = execu(input_case)
    expected = eval(expected_case)
    
    assert output == expected

@pytest.mark.parametrize("input_case, expected_case", zip(input_cases, expected_cases))
def test_unordered_output(input_case, expected_case):
    output = recursive_sorted(execu(input_case))
    expected = recursive_sorted(eval(expected_case))
    
    assert output == expected