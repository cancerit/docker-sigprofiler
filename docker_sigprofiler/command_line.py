#!/usr/bin/env python3

import os
import sys
import argparse
sys.path.insert(0, '/opt/cgp/new_lib/')
from SigProfilerExtractor import sigpro
from . import version


def main():
    '''
    please pass parameters as required.
    '''
    parser = argparse.ArgumentParser(
        description='This script is implemented for accept parameters for the SigProfiler.'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s {}'.format(version),
        help='show the version number and exit'
    )

    parser.add_argument(
        '-i', '--input',
        dest='input_file',
        type=str,
        required=True,
        help='path to input files'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        type=str,
        required=True,
        help='directory for storing results'
    )

    parser.add_argument(
        '-it', '--input_type',
        dest='input_file_type',
        type=str.lower,
        choices=['table', 'text', 'csv', 'matrix', 'vcf', 'matobj'],
        default='vcf',
        help='input files format'
    )

    parser.add_argument(
        '-r', '--reference',
        dest='ref',
        type=str,
        required=True,
        choices=['GRCh37', 'GRCh38', 'c_elegans', 'dog', 'mm9', 'mm10', 'rn6'],
        help='name of reference genome'
    )

    parser.add_argument(
        '-c', '--cpu',
        dest='core',
        type=int,
        default=-1,
        help='Number of CPU cores to use, -1 for all available CPUs'
    )

    parser.add_argument(
        '-ms', '--minimum_sig',
        dest='min_sig',
        type=int,
        default=1,
        help='the minimum number of signatures to start with'
    )

    parser.add_argument(
        '-ts', '--total_sig',
        dest='process',
        type=int,
        # required=True,
        default=5,
        help='the total number of signatures to end with',
    )

    parser.add_argument(
        '-n', '--iteration',
        dest='iteration',
        type=int,
        default=1000,
        help='number of iterations for extracting signatures, default is 1000'
    )

    parser.add_argument(
        '-m', '--mutation_type',
        dest='m_type',
        type=str,
        default='SBS96',
        help='to indicate the type of signatures, eg. SBS96,DBS78'
    )

    parser.add_argument(
        '--init',
        dest='init',
        type=str,
        default='alexandrov-lab-custom',
        choices=['alexandrov-lab-custom', 'nndsvda'],
        help='init method'
    )

    parser.add_argument(
        '-e', '--exome',
        dest='exome',
        action='store_true',
        help='to flag exome data'
    )

    parser.add_argument(
        '--gpu',
        dest='gpu',
        action='store_true',
        help='to use GPU'
    )

    args = parser.parse_args()
    sigpro.sigProfilerExtractor(args.input_file_type, args.output_dir, args.input_file, refgen=args.ref, genome_build=args.ref, startProcess=args.min_sig,
                             endProcess=args.process, totalIterations=args.iteration, init=args.init, cpu=args.core, mtype=args.m_type, 
                             exome=args.exome, penalty=0.05, resample=True, wall=False, gpu=args.gpu)
    print('''
    ========================
    = Extraction finished! =
    ========================''')


if __name__ == "__main__":
    main()
