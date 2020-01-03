#!/usr/bin/env python3

import os
import sys
import argparse
from sigproextractor import sigpro


def main():
    '''
    please pass parameters as required.
    '''
    parser = argparse.ArgumentParser(
        description='This script is implemented for accept parameters for the SigProfiler.'
    )

    parser.add_argument(
        '-i', '--input',
        dest='input_file',
        type=str,
        required=True,
        help='Path to input files'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        type=str,
        required=True,
        help='Directory for storing results'
    )

    parser.add_argument(
        '-it', '--input_type',
        dest='input_file_type',
        type=str,
        required=True,
        help='Input files format'
    )

    parser.add_argument(
        '-r', '--reference',
        dest='ref',
        type=str,
        required=True,
        help='Name of reference genome'
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
        help='The minimum number of signatures to start with',
        default=1
    )

    parser.add_argument(
        '-ts', '--total_sig',
        dest='process',
        type=int,
        required=True,
        help='The total number of signatures to end with',
    )

    parser.add_argument(
        '-n', '--iteration',
        dest='iteration',
        type=int,
        default=1000,
        help='Number of iterations for extracting signatures, default is 1000.'
    )

    parser.add_argument(
        '-m', '--mutation_type',
        dest='m_type',
        action='append',
        type=str,
        default=['96', 'DINUC'],
        help='To indicate the type of signatures',
    )

    parser.add_argument(
        '--hierarchy',
        dest='hie',
        action='store_true',
        help='To flag if hierarchy is expected in the data'
    )

    parser.add_argument(
        '-e', '--exome',
        dest='exome',
        action='store_true',
        help='To flag exome data'
    )

    args = parser.parse_args()
    sigpro.sigProfilerExtractor(args.input_file_type, args.output_dir, args.input_file, refgen=args.ref, startProcess=args.min_sig,
                             endProcess=args.process, totalIterations=args.iteration, cpu=args.core, hierarchy=args.hie,
                             mtype=args.m_type, exome=args.exome)
    print('''
    ========================
    = Extraction finished! =
    ========================''')

if __name__ == "__main__":
    main()
