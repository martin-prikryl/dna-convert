"""
Tests for DNA sequence converter
"""

import os
import pytest
import subprocess


# run and compare output with a file
def run_check_output(sequence_file: str, l_number: int, output_file: str) -> subprocess.CompletedProcess:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    completed_process = subprocess.run(
        ('bash', '-c',
         f'diff {tests_dir}/test_data/{output_file}'
         f' <({tests_dir}/../dna_convert.py {tests_dir}/test_data/{sequence_file} {l_number})'))
    return completed_process


# run with parameters
def run(parameters: tuple) -> subprocess.CompletedProcess:
    tests_dir = os.path.dirname(os.path.realpath(__file__))
    return subprocess.run((f'{tests_dir}/../dna_convert.py',) + parameters)


##############################################################################################


# check output of different sequences and L numbers
@pytest.mark.parametrize('sequence_file, l_number, output_file', [
    ('sequence0', 1, 'output0_1'),
    ('sequence1', 1, 'output1_1'),
    ('sequence1', 999, 'output1_999'),
    ('sequence1024', 1023, 'output1024_1023'),
    ('sequence1024', 1024, 'output1024_1024'),
    ('sequence10111', 10, 'output10111_10'),
    ('sequence10111', 10112, 'output10111_10112')
])
def test_output(sequence_file, l_number, output_file):
    assert run_check_output(sequence_file, l_number, output_file).returncode == 0


# check result code of run with different parameters
@pytest.mark.parametrize('parameters, result_code', [
    (tuple(), 2),
    (('1',), 2),
    (('yes', 'no'), 2),
    (('abc', '9', '9'), 2),
    (('2', '3'), 10),
    (('file_does_not_exist', '100'), 10),
    (('sequence', '0'), 12),
    (('sequence', '-5'), 12)
])
def test_parameters(parameters, result_code):
    assert run(parameters).returncode == result_code
