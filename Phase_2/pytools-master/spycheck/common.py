#!/usr/bin/python
import fnmatch
import os
import re
import ntpath
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
#import en


NOUNS = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
VERBS = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}

wnl = WordNetLemmatizer()


def is_plural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    # return plural, lemma
    return plural

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_tex_files(where, mask="*.tex"):
    matching_files = []

    if os.path.isfile(where):
        matching_files.append(where)
    else:

        for folder_entry in os.listdir(where):
            if fnmatch.fnmatch(folder_entry, mask):
                if os.path.isfile(os.path.join(where, folder_entry)):
                    matching_files.append(
                         os.path.join(where, folder_entry)
                         )
    return matching_files


def print_warning(file_name, line_number, line, pattern, index, message=""):
    file_name =  ntpath.basename(file_name)
    msg_length = 40
    file_name_buf = get_fname_print_buf(file_name, line_number)
    buff = "{0:45}{1}{2}{3}{4}".format(
        file_name_buf,
        line[max(0, index-msg_length):index],
        bcolors.WARNING + pattern + bcolors.ENDC,
        line[index+len(pattern):index+len(pattern)+msg_length],
        bcolors.WARNING + message + bcolors.ENDC)
    print buff

def print_color(msg, color):
    print "{}{}{}".format(
        bcolors.WARNING,
        msg,
        bcolors.ENDC
        )

def get_fname_print_buf(file_name, line_number=0):

    line_buff = ""
    if line_number > 0:
        line_buff = ":%3.3s" % line_number
    return "{}[{}{}]{}".format(
        bcolors.OKGREEN,
        file_name,
        line_buff,
        bcolors.ENDC
        )

def match_reg(line, reg):
    p = re.compile(reg)
    m = p.search(line)
    if m:
        matched_exp = m.group()
        left_index, right_index = m.span()
        return matched_exp, left_index, right_index
    return None, None, None

def fix_spaces(line):
    return " ".join(line.split())
