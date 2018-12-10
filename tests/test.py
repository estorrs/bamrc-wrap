import pytest
import subprocess


TEST_INPUT_DIR = '/app/bamrc-wrap/tests/data/'
TEST_INPUT_FILES = '/app/bamrc-wrap/tests/data/input_files.txt'
TEST_OUTPUT_DIR = '/app/bamrc-wrap/tests/data/output/'
TEST_FASTA = '/app/bamrc-wrap/tests/data/chr1.fa'
TEST_POSITIONS = '/app/bamrc-wrap/tests/data/positions.bed'

def test_simple():
    
    commands = ['python', 'bamrc-wrap.py', '--fasta',  TEST_FASTA, '--input-dir', TEST_INPUT_DIR,
            '--output-dir', TEST_OUTPUT_DIR]

    subprocess.check_output(commands)
    assert True

def test_filter_positions():
    
    commands = ['python', 'bamrc-wrap.py', '--fasta',  TEST_FASTA, '--filter-positions',
            TEST_POSITIONS, '--input-dir', TEST_INPUT_DIR, '--output-dir', TEST_OUTPUT_DIR]

    subprocess.check_output(commands)
    assert True


