import os
import re
import subprocess
import sys
from collections import OrderedDict
from multiprocessing import Pool


def index_bam(bam_fp):
    """Index the given bam file.

    The indexed .bai file will be put in same directory as input file
    """
    samtools_command = ['samtools', 'index', bam_fp]
    subprocess.check_output(samtools_command)

def worker_wrapper(args):
        return execute_bam(*args)
        
def execute_bam(bam_fp, output_fp, fasta_fp, filter_positions_fp=''):
    """Execute a bam file"""
    # index bam
    index_bam(bam_fp)

    # execute remaining commands
    command_args = generate_bamrc_command(bam_fp, output_fp, fasta_fp, filter_positions_fp)
    result = subprocess.check_output(command_args)
    
    f = open(output_fp, 'wb')
    f.write(result)
    f.close()

    return output_fp

def generate_bamrc_command(bam_fp, output_fp, fasta_fp, filter_positions_fp=''):
    """
    return the bam readcount command

    """
    command = ['bam-readcount', '-w', '1', '-f', fasta_fp]

    if filter_positions_fp != '':
        command += ['-l', filter_positions_fp]

#     command += [bam_fp, '>', output_fp]
    command += [bam_fp]

    return command

    
class BamrcWrapper(object):
    def __init__(self, input_files, output_dir, fasta_fp, filter_positions_fp='',
                 output_extension='.readcount', threads=1):
        """Wrapper for Samtools
        
        args:
        
        input_files: list
            list of input bams
        output_dir: str
            directory to store outputs in
        fasta_fp: str
            path to reference fasta
        fasta_fp: str
            path to reference fasta
            
        kwargs:
        
        threads: int
            number of precesses to use
        verbose: bool
            verbose output
            
        """
        self.input_files = input_files
        self.output_dir = output_dir
        
        self.fasta_fp = fasta_fp
        self.filter_positions_fp = filter_positions_fp
        
        self.output_extension = output_extension
        self.num_threads = threads
        
    def run_bams(self):
        # create argument pool
        arg_pool = []
        for fp in self.input_files:
            sample = fp.split('/')[-1]
            sample = re.sub(r'.bam', self.output_extension, sample)
            output_fp = os.path.join(self.output_dir, sample)
            arg_pool.append((fp, output_fp, self.fasta_fp, self.filter_positions_fp))


        with Pool(self.num_threads) as p:
            results = p.map(worker_wrapper, arg_pool)

        print(results)
