#!/usr/bin/python

import itertools
import os
import logging
import argparse

from pytools.common.common import get_files_matching_mask, get_folders_matching_mask

YCSB_MASK="*.ycsb"
PARSED_FILE_EXTENSION="4cdf"
PARSING_VALID_PREFIXES=["READ", "UPDATE", "RawREAD", "RawUPDATE"]
DEFAULT_YCSB_COLUMNS=["opcode", "timestamp_ms", "latency_us"]


class Flags():
    def __init__(self, src_files="", src_dirs=""):
        self.src_files=src_files
        self.src_dirs=src_dirs

def get_source_files(FLAGS, flatten=False):
    assert len(FLAGS.src_files) or len(FLAGS.src_dirs)

    fgroups = []

    if len(FLAGS.src_files):
        fgroups.append(FLAGS.src_files)


    for sdir in FLAGS.src_dirs:

        fldr_index = 1
        file_group = []

        while True:

            # <1.> See if we have a folder counter, and insert it if we do
            if "{}" in sdir or "{0}" in sdir:
                sdir_formatted = sdir.format(fldr_index)
            else:
                sdir_formatted = sdir
                # If there is only one folder, then do not iterate
                if fldr_index > 1:
                    break

            sub_folders = []

            # <2.> If we have wild card, find all matching folders, and return a list
            if "*" in sdir_formatted:
                sub_folders = get_folders_matching_mask(
                    where=os.path.dirname(sdir_formatted),
                    mask=os.path.basename(sdir_formatted)
                    )
                sub_folders = [os.path.join(os.path.dirname(sdir_formatted), x) for x in sub_folders]
            else:
                sub_folders = [sdir_formatted]

            if (len(sub_folders) == 0) or not os.path.isdir(sub_folders[0]):
                ## We say: if we did not returned any folders at all then break.
                ## OR the first folder in the list does not exist (the else path)
                break

            # <3.> For each matching folder find, ycsb files
            for subf in sub_folders:
                for matched_files in get_files_matching_mask(where=subf, mask="*.ycsb"):

                    ifname = os.path.join(subf, matched_files)
                    file_group.append(ifname)
                    print "match ", ifname

            fldr_index += 1

        if len(file_group):
            fgroups.append(file_group)




    for i, group in enumerate(fgroups):
        for f in group:
            logging.info("Input group [%i], file [%s]",i, f)

    if flatten:
        # convert list of list into a list
        fgroups = [i for i in itertools.chain.from_iterable(fgroups)]

    return fgroups


def get_default_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("--src_files", nargs='*', default=[],
        help="A list of individual ycsb files for processing")

    parser.add_argument("--src_dirs", nargs="*", default=[],
        help="""A list of directories for all input files in a set. All ycsb files will
        be picked up from the root level of the folder.

        -------------------------------------
        Each folder can have a counter that goes 1,2,3... it
        should be indicated as {0} within the string. From each valid folder all *.ycsb
        files will be picked up. Each folder forms a group. Example /mnt/.../folder_{0}.
        The counter stops when the a next folder does not exists.
        -------------------------------------------------
        Next, folder pattern can end with a *, in which case wild card matching will
        be used, example: /mnt/.../folder_test_*
        -------------------------------------------------
        Finally, it is possible to match iterators and wild cards, example:
        /mnt/.../folder{0}_test_*. In this case we try to match all folders with counter 1
        then all folders with counter 2, etc. Until the first folder does not exists.
        """)

    parser.add_argument('--src_recurent', dest='sampling', action='store_true',
        help="Recursively search through each folder for ycsb files")

    parser.add_argument("--out_dir", default="./", type=str)

    parser.add_argument("--out_data_file", default="", type=str,
        help="This is a file where all plotting samples will be stored for future replots")

    return parser