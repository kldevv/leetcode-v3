from typing import List, Any, Iterable, Optional
import pytest

import solution

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
    obj = solution.Solution()
    target_function = [x for x in dir(obj) if '__' not in x][0]

    output = eval(f'obj.{target_function}({input_case})')
    expected = eval(expected_case)
    
    assert output == expected

@pytest.mark.parametrize("input_case, expected_case", zip(input_cases, expected_cases))
def test_unordered_output(input_case, expected_case):
    def recursive_sorted(arr: List[Any]) -> List[Any]:
        """
        Sorts a list of lists recursively.
        
        Args:
            arr: A list of any types and/or sub-lists.
        
        Returns:
            A sorted list of any types and/or sub-lists.
        """
        for i in range(len(arr)):
            if isinstance(arr[i], Iterable):
                arr[i] = recursive_sorted(arr[i])
        return sorted(arr)
    
    obj = solution.Solution()
    target_function = [x for x in dir(obj) if '__' not in x][0]

    output = recursive_sorted(eval(f'obj.{target_function}({input_case})'))
    expected = recursive_sorted(eval(expected_case))
    
    assert output == expected