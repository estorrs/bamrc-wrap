#!/bin/python

import argparse
import os
from collections import OrderedDict

from bam_readcount_wrapper import BamrcWrapper

"""
usage: bamrc-wrap [options] [input directory|input files] [output directory]

args:

input files or input directory: txt or directory input files: list of bams to use as inputs.
    One file per line. File paths must be absolute. OR input directory: directory containing
    bams to use as input. path must be absolute

output directory: directory path directory to put output files. path must be absolute.

options:

--fasta: fasta reference to pass to bam readcount

--filter-positions: .bed file positions to keep in bams three columns.
    Format is <chrom>\t<start-pos>\t<end-pos>.
    Positions are inclusive.

--output-extension: extension of output files. Default is .readcount

--threads: int number of processes to use. default is 1.
"""

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('--input-dir', type=str,
        help="Directory containing input bams.")
group.add_argument('--input-files', type=str,
        help="File containing input bams. One per line.")

parser.add_argument('--output-dir', type=str,
        help='Directory output files are to be put in.')

# parser.add_argument('--bulk-index',
#         action="store_true", help='Index the input bams')
# parser.add_argument('--bulk-sort',
#         action='store_true', help='Sort output bams')
# parser.add_argument('--sort-threads', type=int,
#         default=1, help='Number of threads for samtools to use during sorting.')
parser.add_argument('--fasta', type=str,
        help='Fasta reference to pass to bam-readcount')
parser.add_argument('--filter-positions', type=str,
        default='', help='''.bed file containing positions to filter bams with.\n
            Format is the following: <chrom>\t<start-pos>\t<end-pos>''')
parser.add_argument('--output-extension', type=str,
        default='.readcount', help='extension for output files. Default is .readcount')
parser.add_argument('--threads', type=int,
        default=1, help='Number of processes to use. Default is 1.')

args = parser.parse_args()

def get_fps_from_file(fp):
    f = open(fp)
    return [line.replace('\n', '') for line in f]

def get_fps_from_dir(dir_path):
    return [os.path.join(dir_path, p) for p in os.listdir(dir_path)
          if p[-4:] == '.bam']

def get_input_files():
    if args.input_dir is not None:
        return get_fps_from_dir(args.input_dir)
    else:
        return get_fps_from_file(args.input_files)

# def get_operations_dict():
#     d = OrderedDict()
# 
#     if args.bulk_index:
#         d['index'] = None
# 
#     if args.filter_positions is not None:
#         d['position_filter'] = {
#                 'positions_fp': args.filter_positions
#                 }
# 
#     if args.bulk_sort:
#         d['sort'] = {
#                 'sort_threads': args.sort_threads
#                 }
# 
#     return d

def check_arguments():
    if args.output_dir is None:
        raise ValueError('Must specify --output-dir')

    if args.input_dir is None and args.input_files is None:
        raise ValueError('Must specify an --input-files file list or --input_dir directory.')

    if args.fasta is None:
        raise ValueError('Must specify an --fasta file')

def main():
    check_arguments()

    input_fps = get_input_files()

#     operations_dict = get_operations_dict()

    bw = BamrcWrapper(input_fps, args.output_dir, args.fasta, args.filter_positions,
        output_extension=args.output_extension, threads=args.threads)
    bw.run_bams()

if __name__ == '__main__':
    main()
