from typing import List
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
            cases.append(line.strip().replace('\n', ''))
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
def test_nonnested_output(input_case, expected_case):
    obj = solution.Solution()
    target_function = [x for x in dir(obj) if '__' not in x][0]
    
    assert eval(f'obj.{target_function}({input_case})') == eval(expected_case)
