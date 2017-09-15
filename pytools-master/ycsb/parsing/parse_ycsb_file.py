#!/usr/bin/python
import argparse
import logging
import multiprocessing
import subprocess
import os
import numpy as np
from pytools.common.proc import check_pid_output
from pytools.common.common import print_generic_exception, get_files_matching_mask, remove_files
from pytools.ycsb.ycsb_common import PARSED_FILE_EXTENSION, PARSING_VALID_PREFIXES

logging.basicConfig(
    format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s",
    datefmt='%H:%M:%S', level=logging.INFO)

SPLIT_SUFFIX_LENGTH=2 # should match -a parameter in split used in split_file.sh

def split_file(ifile, n_parts):

    try:
        cmd = "split_file.sh {file} {n_parts} {base_file_name}".format(
            file=ifile,
            n_parts=n_parts,
            base_file_name=os.path.basename(ifile))
        logging.info("Splitting file [%s] into [%s] parts", ifile, n_parts)

        proc = subprocess.Popen(cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        check_pid_output(proc)

    except:
        print_generic_exception("file splitting failed")

def get_split_parts(ifile, n_parts):
    base_file_name=os.path.basename(ifile)
    flist = []
    for i in range(0, n_parts):

        ifile = get_files_matching_mask(where="./", mask="%s.%s"% (
            base_file_name,
            str(i).zfill(2))
            )
        print ifile, "%s.%s"% (
            base_file_name,
            str(i).zfill(2))

        assert len(ifile) == 1 or len(ifile) == 0
        if len(ifile) == 1:
            flist.append(ifile[0])

    return flist

def join_files(parsed_files, out_file):
    logging.debug("Joining files: [%s] into [%s]", parsed_files, out_file)

    for i, pf in enumerate(parsed_files):

        if i == 0:
            cmd = "cat %s > %s" % (pf, out_file)
        else:
            cmd = "cat %s >> %s" % (pf, out_file)

        logging.debug("Joining [%s] into [%s]", pf, out_file)
        proc = subprocess.Popen(cmd, shell=True)
        check_pid_output(proc)


def parallel_fast_parse(flist, valid_prefixes, pattern):

    parsed_files = []
    procs2wait_on = []

    for f in flist:
        parsed_file_name = "%s.%s" % (f, PARSED_FILE_EXTENSION)
        cmd = "fast_cpp_ycsb_parser {input_file} {output_file} {pattern} {valid_prefixes} ".format(
            input_file=f,
            output_file=parsed_file_name,
            pattern=pattern,
            valid_prefixes=" ".join(valid_prefixes)
            )
        parsed_files.append(parsed_file_name)

        logging.debug("Executing cmd[%s]", cmd)
        proc = subprocess.Popen(cmd,
                shell=True)
        procs2wait_on.append(proc)

    for p in procs2wait_on:
        p.wait()

    return parsed_files


####################################################################################################
# This is a wrapper for fast parsing of YCSB outputs
# Scripts takes a large YCSB output and splits it into smaller files,
# then it uses fast_cpp_ycsb_parser.cpp to parse individual chunks, then it merges data back into
# a single file
# for the list of patterns see the CPP code.
####################################################################################################

def cpp_parse_ycsb_file(ifile,  out_file_name=None,
    valid_prefixes=PARSING_VALID_PREFIXES, pattern=1, n_parts=multiprocessing.cpu_count()):

    if not out_file_name:
        out_file_name = "%s.%s" % (ifile, PARSED_FILE_EXTENSION)

    split_file(ifile, n_parts)

    flist = get_split_parts(ifile, n_parts)

    parsed_files = parallel_fast_parse(flist, valid_prefixes, pattern)

    join_files(parsed_files, out_file_name)

    logging.debug("REMOVING files [%s] ", flist)
    remove_files(flist)
    logging.debug("REMOVING files [%s]", parsed_files)
    remove_files(parsed_files)


if __name__ == '__main__':

    parser = argparse.ArgumentParser("""Parsing of the YCSB output files""",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--src_file", type=str)
    parser.add_argument("--out_file", type=str)

    parser.add_argument("--pattern", default=1, help="Specifies fields to be parsed out")

    parser.add_argument("--valid_prefixes", nargs='*',
        default=["READ"],
        help="""For a given pattern, specifies allowed sub-patterns, e.g., READ or R etc. """)

    FLAGS = parser.parse_args()

    cpp_parse_ycsb_file(FLAGS.src_file, FLAGS.out_file, FLAGS.valid_prefixes, FLAGS.pattern)
