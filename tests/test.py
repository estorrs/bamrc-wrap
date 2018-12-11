import pytest
import subprocess


import sys
sys.path.insert(0, "/app/bamrc-wrap/")

import vaf_generator


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

def test_vaf_processor_simple():

    commands = ['python', 'readcount-processor.py', '--vafs', '--threads', '2', '--input-dir',
            TEST_OUTPUT_DIR, '--output-dir', TEST_OUTPUT_DIR]

    subprocess.check_output(commands)
    assert True

def test_vaf_calculations():
    test_line_stats = [
        ('chr1', 1875755, 'G', 9, {'A': 0, 'C': 0, 'G': 4, 'T': 5, 'N': 0}),
        ('chr1', 1875756, 'A', 2, {'A': 0, 'C': 0, 'G': 0, 'T': 2, 'N': 0}),
        ('chr1', 1875799, 'T', 49, {'A': 0, 'C': 3, 'G': 0, 'T': 45, 'N': 1})
    ]

    ds = []
    for chrom, pos, ref, depth, base_dict in test_line_stats:
        vaf_dict = vaf_generator.get_base_vafs(ref, depth, base_dict)
        ds.append(vaf_dict)

    assert ds == [{'A': 0.0,
          'C': 0.0,
          'G': 0.4444444444444444,
          'T': 0.5555555555555556,
          'N': 0.0,
          'minor': 0.5555555555555556},
         {'A': 0.0, 'C': 0.0, 'G': 0.0, 'T': 1.0, 'N': 0.0, 'minor': 1.0},
         {'A': 0.0,
          'C': 0.061224489795918366,
          'G': 0.0,
          'T': 0.9183673469387755,
          'N': 0.02040816326530612,
          'minor': 0.08163265306122448}]
