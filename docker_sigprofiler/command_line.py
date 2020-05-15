#!/usr/bin/env python3

import os
import sys
import argparse
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
        dest='maximum_signatures',
        type=int,
        # required=True,
        default=5,
        help='the total number of signatures to end with',
    )

    parser.add_argument(
        '-n', '--iteration',
        dest='nmf_replicates',
        type=int,
        default=250,
        help='number of iterations for extracting signatures, default is 250'
    )

    parser.add_argument(
        '-ct', '--context_type',
        dest='context_type',
        type=str,
        default='SBS96',
        help='to indicate the type of signatures, eg. SBS96,DBS78'
    )

    parser.add_argument(
        '--init',
        dest='nmf_init',
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

    parser.add_argument(
        '--batch_size',
        dest='batch_size',
        type=int,
        default=1,
        help='to define bath size for running on GPU'
    )

    parser.add_argument(
        '--precision',
        dest='precision',
        type=str,
        default='single',
        help='to define precision'
    )

    parser.add_argument(
        '-mn','--matrix_normalization',
        dest='matrix_normalization',
        type=str,
        default='100X',
        help='to define times of matrix normalization'
    )

    parser.add_argument(
        '--seeds',
        dest='seeds',
        type=str,
        default='random',
        help='to define the seed for each NMF process, can be "random" or a "seed file"'
    )

    parser.add_argument(
        '--min_nmf_iterations',
        dest='min_nmf_iterations',
        type=int,
        default=10000,
        help='to define minimum number of NMF iterations'
    )

    parser.add_argument(
        '--max_nmf_iterations',
        dest='max_nmf_iterations',
        type=int,
        default=1000000,
        help='to define maximum number of NMF iterations'
    )

    parser.add_argument(
        '--nmf_test_conv',
        dest='nmf_test_conv',
        type=int,
        default=10000,
        help='to define NMF test converge'
    )

    parser.add_argument(
        '--nmf_tolerance',
        dest='nmf_tolerance',
        type=float,
        default=1e-15,
        help='NMF tolerance threshold'
    )

    parser.add_argument(
        '--get_all_signature_matrices',
        dest='get_all_signature_matrices',
        action='store_true',
        help='to flag get_all_signature_matrices as true'
    )

    parser.add_argument(
        '--nnls_penalty',
        dest='nnls_penalty',
        type=float,
        default=0.05,
        help='to define NNLS penalty threshold'
    )


    args = parser.parse_args()
    sigpro.sigProfilerExtractor(
        args.input_file_type, 
        args.output_dir, 
        args.input_file, 
        reference_genome=args.ref, 
        opportunity_genome=args.ref, 
        minimum_signatures=args.min_sig,
        maximum_signatures=args.maximum_signatures, 
        nmf_replicates=args.nmf_replicates, 
        nmf_init=args.nmf_init, 
        cpu=args.core, 
        context_type=args.context_type, 
        exome=args.exome, 
        nnls_penalty=args.nnls_penalty,
        resample=True, 
        gpu=args.gpu,
        batch_size=args.batch_size,
        precision=args.precision,
        matrix_normalization=args.matrix_normalization,
        seeds=args.seeds,
        min_nmf_iterations=args.min_nmf_iterations,
        max_nmf_iterations=args.max_nmf_iterations,
        nmf_test_conv=args.nmf_test_conv,
        nmf_tolerance=args.nmf_tolerance,
        get_all_signature_matrices=args.get_all_signature_matrices
        )
    print('''
    ========================
    = Extraction finished! =
    ========================''')


if __name__ == "__main__":
    main()
