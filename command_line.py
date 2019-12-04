#!/usr/bin/env python3

import os
import argparse
from sigproextractor import sigpro as sig


def string_to_bool(input_string):
    return False if input_string.lower() == "false" else True


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
        action='store',
        type=str,
        required=True,
        help='Path to input files'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_dir',
        action='append',
        type=str,
        required=True,
        help='Directory for storing results'
    )

    parser.add_argument(
        '-it', '--input_type',
        action='store',
        dest='input_file_type',
        type=str,
        required=True,
        help='Input files format'
    )

    parser.add_argument(
        '-r', '--reference',
        dest='ref',
        action='store',
        type=str,
        required=True,
        help='Name of reference genome'
    )

    parser.add_argument(
        '-c', '--cpu',
        dest='core',
        action='store',
        type=int,
        required=False,
        help='Number of CPU cores to use, -1 for all available CPUs',
        default=-1
    )

    parser.add_argument(
        '-ms', '--minimum_sig',
        dest='min_sig',
        action='store',
        type=int,
        required=False,
        help='The minimum number of signatures to start with',
        default=1
    )

    parser.add_argument(
        '-ts', '--total_sig',
        dest='process',
        action='store',
        type=int,
        required=True,
        help='The total number of signatures to end with',
    )

    parser.add_argument(
        '-n', '--iteration',
        dest='iteration',
        action='store',
        type=int,
        required=False,
        help='Number of iterations for extracting signatures, default is 1000.',
        default=1000
    )

    parser.add_argument(
        '-m', '--mutation_type',
        dest='m_type',
        action='store',
        type=int,
        required=False,
        help='To indicate the type of signatures',
        # default=False
    )

    parser.add_argument(
        '--hierarchy',
        dest='hie',
        action='store',
        type=bool,
        required=False,
        help='To flag if hierarchy is expected in the data',
        default=False
    )

    parser.add_argument(
        '-e', '--exome',
        dest='exome',
        action='store',
        type=bool,
        required=False,
        help='To flag exome data',
        default=False
    )

    args = parser.parse_args()
    print(args.m_type)
    print(args.exome)
    print(type(args.exome))


    # input_file = os.environ.get('INPUT_FILE')
    # output_dir = os.environ.get('OUTPUT_DIR')
    # input_file_type = os.environ.get('INPUT_FILE_TYPE')
    # ref = os.environ.get('REF_GENOME')
    # core = int(os.environ.get('CPU'))
    # min_sig = int(os.environ.get('MINUM_SIG'))
    # process = int(os.environ.get('NUMBER_OF_SIGNATURE'))
    # iteration = int(os.environ.get('ITERATION'))
    # hie = os.environ.get('HIERARCHY')
    # m_type = os.environ.get('MTYPE').split(',')
    # exome = os.environ.get('EXOME')

    # if m_type is None:
    #     m_type = ["default"]
    # hie = string_to_bool(hie)
    # exome = string_to_bool(exome)
    # print(
    #     input_file, output_dir, ref, input_file_type, core, min_sig, process, iteration, hie, m_type, exome
    # )
    sig.sigProfilerExtractor(args.input_file_type, args.output_dir, args.input_file, refgen=args.ref, startProcess=args.min_sig,
                             endProcess=args.process, totalIterations=args.iteration, cpu=args.core, hierarchy=args.hie,
                             mtype=args.m_type, exome=args.exome)
    print('''
    ========================
    = Extraction finished! =
    ========================''')

if __name__ == "__main__":
    main()
    
