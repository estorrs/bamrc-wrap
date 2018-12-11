import argparse
import os
from multiprocessing import Pool

import vaf_generator

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument('--input-dir', type=str,
        help="Directory containing input bams.")
group.add_argument('--input-files', type=str,
        help="File containing input bams. One per line.")

parser.add_argument('--output-dir', type=str,
        help='Directory output files are to be put in.')

parser.add_argument('--vafs',
        action='store_true', help='Do vaf calculations')

parser.add_argument('--threads', type=int,
        default=1, help='number of processes to run')

args = parser.parse_args()

def get_fps_from_file(fp):
    f = open(fp)
    return [line.replace('\n', '') for line in f]

def get_fps_from_dir(dir_path):
    return [os.path.join(dir_path, p) for p in os.listdir(dir_path)
          if p[-10:] == '.readcount']

def get_input_files():
    if args.input_dir is not None:
        return get_fps_from_dir(args.input_dir)
    else:
        return get_fps_from_file(args.input_files)

def check_arguments():
    if args.output_dir is None:
        raise ValueError('Must specify --output-dir')

    if args.input_dir is None and args.input_files is None:
        raise ValueError('Must specify an --input-files file list or --input_dir directory.')

def worker(args):
    return vaf_generator.process_readcounts(*args)

def main():
    check_arguments()

    input_fps = get_input_files()

    arg_pool = []
    for fp in input_fps:
        sample = fp.split('/')[-1]
        sample += '.vafs'
        output_fp = os.path.join(args.output_dir, sample)
        arg_pool.append((fp, output_fp))

    with Pool(args.threads) as p:
        results = p.map(worker, arg_pool)

if __name__ == '__main__':
    main()
