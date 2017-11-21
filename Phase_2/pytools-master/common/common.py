#!/usr/bin/python
import collections
import fnmatch
import os
import re
import subprocess
import sys
import time
import traceback
from pytools.common.common import *

def remove_repeated_spaces(line):
    return " ".join(line.split())


def chunk_list(array_to_chunk, chunk_size):
    """Yield successive n-sized chunks from l.
    Divides an array into a number of equally sized chunks"""
    for i in xrange(0, len(array_to_chunk), chunk_size):
        yield array_to_chunk[i:i+chunk_size]

def chunk_list_by_nsets(array_to_chunk, number_of_sublists):

    chunk_size  = len(array_to_chunk) / number_of_sublists
    if len(array_to_chunk) % number_of_sublists > 0:
        chunk_size += 1

    chunk_size = max(1, chunk_size)


    for i in xrange(0, len(array_to_chunk), chunk_size):
        yield array_to_chunk[i:i+chunk_size]


def get_folders_matching_mask(where, mask):
    matching_folders = []
    # print where, mask
    for folder_entry in os.listdir(where):
        if fnmatch.fnmatch(folder_entry, mask):
            if os.path.isdir(os.path.join(where, folder_entry)):
                matching_folders.append(folder_entry)
    return matching_folders


def get_files_matching_mask(where, mask):
    matching_files = []
    # print where, mask
    for folder_entry in os.listdir(where):
        if fnmatch.fnmatch(folder_entry, mask):
            if os.path.isfile(os.path.join(where, folder_entry)):
                matching_files.append(folder_entry)
    return matching_files

def find_files_matching_mask(where, mask):
    p = subprocess.Popen(["find", where, "-name", mask], stdout=subprocess.PIPE)
    out, _ = p.communicate()
    for line in out.readlines():
        print line

def yeld_iterative_folders(folder_entry, index_start=1, index_end=0, replace_pattern=""):
    ''' Iterator over folders that contain an index number. For example:
    fldr_1_test, fldr_2_test, fldr_3_test. etc.
    the folder entry can be in a form "fldr_{}_test" or "fldr_REPLACE_PATTERN_test"
    If no replace pattern is specified or not curly brackets in the folder_entry then
    the input foder_entry is returned as the only folder if exists.
    '''
    index = index_start

    while True:

        if len(replace_pattern):
            fldr_name = folder_entry.replace(replace_pattern, index)
        elif "{" in folder_entry:
            fldr_name = folder_entry.format(index)
        else:
            # Nothing to iterate over, try to return the input.
            fldr_name = folder_entry
            index_end = 1

        if os.path.isdir(fldr_name):
            yield fldr_name
        else:
            break

        index += 1

        if index_end > 0 and index > index_end:
            break




def wait_with_message(message, seconds):
    _now = time.time()
    _end = _now + seconds
    while _end > _now:
        sys.stdout.write("{0} ({1} seconds)   \r".format(message, int(_end - _now)))
        sys.stdout.flush()
        time.sleep(1)
        _now = time.time()
    print ""

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def get_duplicate_values_in_list(l):
    return [item for item, count in collections.Counter(l).items() if count > 1]

def merge_dicts(dst_dic, src_dic, overwrite=True):
    """ Takes src_dic and adds everything into dst_dict. Can either add new elements only
    or overwrite old ones"""
    if not src_dic:
        return dst_dic

    for k, v in src_dic.iteritems():
        # print k, isinstance(dst_dic[k], dict), isinstance(v, dict)
        if k in dst_dic and isinstance(dst_dic[k], dict) and isinstance(v, dict):
            merge_dicts(dst_dic[k], v)

        elif k in dst_dic and overwrite:
            dst_dic[k] = v
            continue

        if k not in dst_dic:
            dst_dic[k] = v

    return dst_dic

def is_strin_anIP(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def print_generic_exception(msg="Generic Exception"):
    exec_info = sys.exc_info()
    print "%s: %s" % (msg, sys.exc_info())
    traceback.print_exception(*exec_info)

def remove_files(flist):
    for f in flist:
        if os.path.isfile(f):
            os.remove(f)

def remove_non_alphanumerics(instr):
    regex = re.compile('[^a-zA-Z0-9]')
    return regex.sub('', instr)
