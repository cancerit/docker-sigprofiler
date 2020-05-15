#!/usr/bin/env python3

import os
import sys
import argparse
import SigProfilerMatrixGenerator
from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen


def main():
    '''
    please pass parameters as required.
    '''

    parser = argparse.ArgumentParser(
        description='This script is implemented for accept parameters for the SigProfilerMatrixGenerator.'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=SigProfilerMatrixGenerator.__version__,
        help='Show matrixGenerator core version number and exit.'
    )

    parser.add_argument(
        '-p', '--project',
        dest='project',
        type=str,
        required=True,
        help='unique name given to the current samples.'
    )

    parser.add_argument(
        '-r', '--ref',
        dest='ref',
        type=str,
        required=True,
        help='reference genome.'
    )

    parser.add_argument(
        '-i', '--input',
        dest='input',
        type=str,
        required=True,
        help='path to input files.'
    )

    parser.add_argument(
        '--bed_file',
        dest='bed_file',
        type=str,
        default=None,
        help='BED file that contains a list of ranges to be used in generating the matrices saved into the output/TSB directory.'
    )

    parser.add_argument(
        '--cushion',
        dest='cushion',
        type=int,
        default=100,
        help='path to input files.'
    )


    parser.add_argument(
        '--plot',
        dest='plot',
        action='store_true',
        help='flag to generate the plots for each context.'
    )

    parser.add_argument(
        '--exome',
        dest='exome',
        action='store_true',
        help='flag to use only the exome.'
    )

    parser.add_argument(
        '--chrom_based',
        dest='chrom_based',
        action='store_true',
        help='flag to create the matrices on a per chromosome basis.'
    )

    parser.add_argument(
        '--tsb_stat',
        dest='tsb_stat',
        action='store_true',
        help='performs a transcriptional strand bias test for the 24, 384, and 6144 contexts. The output is saved into the output/TSB directory.'
    )

    parser.add_argument(
        '--seq_info',
        dest='seq_info',
        action='store_true',
        help='outputs original mutations into a text file that contains the SigProfilerMatrixGenerator classification for each mutation.'
    )

    parser.add_argument(
        '--gs',
        dest='gs',
        action='store_true',
        help='flag that performs a gene strand bias test.'
    )

    args = parser.parse_args()
    assert os.path.exists(args.input)

    matGen.SigProfilerMatrixGeneratorFunc(args.project, args.ref, 
        args.input, 
        plot=args.plot, 
        exome=args.exome, 
        bed_file=args.bed_file, 
        chrom_based=args.chrom_based, 
        tsb_stat=args.tsb_stat, 
        seqInfo=args.seq_info, 
        cushion=args.cushion,  
        gs=args.gs)

    print('job finished!')
    print(f'The matrices are available at {(args.input).strip("/")}/output!')


if __name__ == "__main__":
    main()

# project  -> unique name given to the current samples
# genome  -> reference genome 
# vcfFiles  -> path where the input vcf files are located.
# plot  -> flag to generate the plots for each context
# exome  -> flag to use only the exome or not
# chrom_based  -> flag to create the matrices on a per chromosome basis
# tsb_stat  -> performs a transcriptional strand bias test for the 24, 384, and 6144 contexts. The output is

# bed_file  -> BED file that contains a list of ranges to be used in generating the matrices
# saved into the output/TSB directory
# gs  -> flag that performs a gene strand bias test