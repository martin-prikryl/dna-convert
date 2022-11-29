"""
Tests for DNA sequence converter
"""

import os
import pytest
import subprocess


# run and compare output with a file
def run_check_output(sequence_file: str, l_number: int, output_file: str, java: bool) -> subprocess.CompletedProcess:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    if java:
        command = \
            f'diff {tests_dir}/test_data/{output_file}' \
            f' <(java {tests_dir}/../dna_convert.java {tests_dir}/test_data/{sequence_file} {l_number})'
    else:
        command = \
            f'diff {tests_dir}/test_data/{output_file}' \
            f' <({tests_dir}/../dna_convert.py {tests_dir}/test_data/{sequence_file} {l_number})'
    completed_process = subprocess.run(('bash', '-c', command))
    return completed_process


# run with parameters
def run(parameters: tuple, java: bool) -> subprocess.CompletedProcess:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    if java:
        return subprocess.run(('java', f'{tests_dir}/../dna_convert.java') + parameters)
    return subprocess.run((f'{tests_dir}/../dna_convert.py',) + parameters)


##############################################################################################


# check output of different sequences and L numbers
@pytest.mark.parametrize('sequence_file, l_number, output_file, java', [
    ('sequence0', 1, 'output0_1', False),
    ('sequence1', 1, 'output1_1', False),
    ('sequence1', 999, 'output1_999', False),
    ('sequence1024', 1023, 'output1024_1023', False),
    ('sequence1024', 1024, 'output1024_1024', False),
    ('sequence10111', 10, 'output10111_10', False),
    ('sequence10111', 10112, 'output10111_10112', False),
    ('sequence0', 1, 'output0_1', True),
    ('sequence1', 1, 'output1_1', True),
    ('sequence1', 999, 'output1_999', True),
    ('sequence1024', 1023, 'output1024_1023', True),
    ('sequence1024', 1024, 'output1024_1024', True),
    ('sequence10111', 10, 'output10111_10', True),
    ('sequence10111', 10112, 'output10111_10112', True)
])
def test_output(sequence_file, l_number, output_file, java):
    assert run_check_output(sequence_file, l_number, output_file, java).returncode == 0


# check result code of run with different parameters
@pytest.mark.parametrize('parameters, result_code, java', [
    (tuple(), 2, False),
    (('1',), 2, False),
    (('yes', 'no'), 2, False),
    (('abc', '9', '9'), 2, False),
    (('2', '3'), 10, False),
    (('file_does_not_exist', '100'), 10, False),
    (('sequence', '0'), 12, False),
    (('sequence', '-5'), 12, False),
    (tuple(), 2, True),
    (('1',), 2, True),
    (('yes', 'no'), 2, True),
    (('abc', '9', '9'), 2, True),
    (('2', '3'), 10, True),
    (('file_does_not_exist', '100'), 10, True),
    (('sequence', '0'), 12, True),
    (('sequence', '-5'), 12, True)
])
def test_parameters(parameters, result_code, java):
    assert run(parameters, java).returncode == result_code
