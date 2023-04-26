# Virus detection pipeline
# Requirements: metaFlye, viralFlye, PFAM HMM db and a long read NGS dataset in fasta format
    # METAFLYE & VIRALFLYE ENV: conda env create -f virus_pipeline_conda.yml (create myclone environment)
    # VIRALFLYE: git clone https://github.com/Dmitry-Antipov/viralFlye (download viralFlye binaries)
    # PFAM: https://www.ebi.ac.uk/interpro/download/pfam/ (download PFAM HMM models)
# USAGE: virus_pipeline.py -h
# OUTPUT: Circular and linear virus construct(s). Intermediary files include microbial MAGs.

import importlib

# Check whether argparse, logging, subprocess, and os are installed
packages = ['argparse', 'logging', 'subprocess', 'os']
not_installed = []

for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        not_installed.append(package)

if not_installed:
    print("ERROR: Please first install the following python packages: {}".format(', '.join(not_installed)))
    quit()

import argparse
import logging
import subprocess
import os

# Initialize argument parser
parser = argparse.ArgumentParser(prog = 'Werner\'s virus finder',
                                 description='Assemble viral genomes from long reads. NOTE: metaflye must be in your path, and the paths to viralflye and a PFAM HMM db (hmmpressed) must be supplied explicitly.')

parser.add_argument('-f', dest='FASTA', type=str, help='FASTA file with long reads', 
                    required=True)
parser.add_argument('-r', dest='READTYPE', type=str, 
                    help='pacbio-raw | pacbio-corr | pacbio-hifi | nano-raw | nano-cor | nano-hq', 
                    required=True)
parser.add_argument('-x', dest='VIRALFLYE', type=str, help='Path to viralFlye.py', required=True)
parser.add_argument('-p', dest='HMM', type=str, help='Path to Pfam HMM', required=True)
parser.add_argument('-t', dest='THREADS', type=str, default=str(4),
                    help='Number of CPU threads to use [Default = 4]')
parser.add_argument('-l', dest='LOGFILE', type=str, default='werner.log', help='Name of log file [Default: werner.log]')
parser.add_argument('-d', dest='DRYRUN', action='store_true', help='Toggle debug mode')
parser.add_argument('-v', action='version', version='%(prog)s (version 1.0)')
try:
    args = parser.parse_args()
except:
    print("Run virus_pipeline.py -h for help")
    quit()

def main():
    oscwd = os.getcwd()
    # Initialize logger
    logging.basicConfig(filename=args.LOGFILE,
                        format='%(asctime)s %(levelname)-8s %(message)s', 
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filemode="w+")

    print()
    print("Log file saved to current directory: {}".format(args.LOGFILE))
    logging.info("FASTA file name taken as: {}".format(args.FASTA))
    logging.info("Type of reads taken as: {}".format(args.READTYPE))
    logging.info("HMM path taken as: {}".format(args.FASTA))
    logging.info("viralFlye.py path taken as: {}".format(args.FASTA))
    logging.info("Number of CPU threads taken as: {}".format(args.THREADS))

    # Check whether metaFlye is installed and run it
    try:
        metaflye_version = subprocess.check_output(["flye", "--version"])
        logging.info("Found metaFlye version " + metaflye_version.decode('utf-8').replace("\n", ""))
    except:
        print("The metaFlye executable \"flye\" must be in your path. It does not appear to be.")
        logging.error("metaflye could not be found in your path")
        quit()

    metaflye_command = ["flye", "--"+args.READTYPE, args.FASTA, 
                        "--threads", args.THREADS, "-o", "metaflye_output"]
    metaflye_command_print = " ".join(str(n) for n in metaflye_command)
    logging.info("metaFlye command: {}".format(metaflye_command_print))
    if args.DRYRUN is False:
        metaflye_output = subprocess.check_output(metaflye_command)
        logging.info("metaFlye output saved in: {}".format("metaflye_output"))

    # Run viralFlye
    os.chdir(oscwd)
    viralflye_command = [args.VIRALFLYE, "--dir", "metaflye_output", "--reads", args.FASTA, 
                        "--hmm", args.HMM, "--threads", args.THREADS, "--outdir", "viralflye_output"]
    viralflye_command_print = " ".join(str(n) for n in viralflye_command)
    logging.info("viralFlye command: {}".format(viralflye_command_print))
    if args.DRYRUN is False:
        viralflye_output = subprocess.check_output(viralflye_command)
        logging.info("viralFlye output saved in: {}".format("viralflye_output"))
    logging.info("Viral detection pipeline has finished")

    # Finish
    print("Viral detection pipeline has finished!")
    if args.DRYRUN:
        logging.info("END OF DRYRUN")

if __name__ == "__main__":
    main()