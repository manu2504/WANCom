#!/usr/bin/python
import argparse
import logging
import operator
from collections import Counter

logging.basicConfig(format="(%(process)d)\t%(asctime)s\t%(levelname)s\t%(message)s", datefmt='%H:%M:%S', level=logging.INFO)

from spycheck.common import *
from spycheck.checkcommas import *
from spycheck.checkgrammar import *






def parse_args():

    parser = argparse.ArgumentParser(description ="Check Text Syntax")

    parser.add_argument('--path', help='Location of *tex files to check',
        type=str, default="./content/")

    return parser.parse_args()




def check_test(file_name, line, line_number):

    reg_exsps = [
    # ("correlate+[ |\w]+to","correlate with", []),

    ("[S|s]uch set","correlate with", []),
    ("potentially would", "would potentially", []),
    ("[a] per-", "no article", []),
    ("[f|F]ull picture", "complete picture", []),
    ("[T|t]he informantion", "no article", []),
    ("[T|t]he correl", "a correlation?", []),
    ("[C|c]ompa[\w]+[ ]+to", "Compare with", [])
    ]


    for exp in reg_exsps:
        p = re.compile(exp[0])
        m = p.search(line)
        if m and m.group() not in exp[2]:
            left_index,_ = m.span()
            print_warning(
                file_name, line_number, line, m.group(),
                left_index, message=" (use: %s ?)"%(exp[1])
                )

    ##########################################
    # Complex Checks
    ##########################################

    # [only + verb:present.endswith(ed)] we say verb then only
    match, left_indx, _ = match_reg(line, "only [\w]+[ ]")
    if match:
        tokens = fix_spaces(match).split(" ")
        word = tokens[-1]
        try:
            if word == en.verb.present(word) and word.endswith("ed"):
                print_warning(file_name, line_number, line, match,
                    left_indx, message=" (use: Remove article?)")
        except:
            logging.debug("Ignoring case: %s " % match)
            pass







def check_files_by_line(src_files, per_line_check_function):


    for sf in src_files:
        # fpath = os.path.join(FLAGS.path, sf)

        with open(sf) as sfile:
            content = sfile.readlines()

        for line_number, line in enumerate(content):
            line = line.lstrip().rstrip()
            if (line.startswith("%") or
                line.startswith("\\")
                ):
                continue
            line = re.sub("""{}""", '', line)
            per_line_check_function(sf, line, line_number+1)


def check_word_frequency(src_files):

    group = ["demonstrate", "show", "indicate"]
    to_use = [
    "In contrast,"

    ]

    counter = Counter()
    for sf in src_files:
        # fpath = os.path.join(FLAGS.path, sf)

        with open(sf) as sfile:
            for line in sfile.readlines():
                line = line.lstrip().rstrip()
                if (line.startswith("%") or
                    line.startswith("\\") or
                    len(line) < 3
                ):
                    continue
                line = re.sub("[.,}{:;\"\'?!()0-9~]", '', line).lower()

                # words = re.split(" |, |\. |: |; |{|}|(|)", line)
                words = re.split(" ", line)
                # print words
                for w in words:
                    if w:
                        w = w.lower()
                        if (len(w) > 3 and
                            not w[0] == "\\" and
                            not w.startswith("%")
                            ):
                            counter[w] += 1

    sorted_words = sorted(
        counter.items(),
        key=operator.itemgetter(1),
        reverse=True)

    for i in range(0, 15):
        print sorted_words[i]
    return sorted_words

if __name__ == '__main__':

    FLAGS = parse_args()

    # print FLAGS.path


    src_files = get_tex_files(FLAGS.path)
    print src_files

    print_color("-------Missing Commas-------", bcolors.UNDERLINE )
    check_files_by_line(src_files, check_line_for_commas)

    print_color("-------Grammar-------", bcolors.UNDERLINE )
    check_files_by_line(src_files, check_line_for_unwanted_patterns)

    print_color("-------New Tests-------", bcolors.UNDERLINE )
    check_files_by_line(src_files, check_test)

    # check_files_for_unwanted_patterns(src_files)

    print_color("-------Word Statistics-------", bcolors.UNDERLINE )
    sw = check_word_frequency(src_files)