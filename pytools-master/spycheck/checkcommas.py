#!/usr/bin/python
import re
import logging
from common import *

def check_line_for_commas(file_name, line, line_number):

    reg_exsps = [
    # ("[a-zA-Z]+, [a-zA-Z]+ (and).", "x, y, and z"),
    ("[\w] such as", ", such as"),
    ("[\w] however", ", however,"),
    ("[\w] hence", ", hence"),
    ("[^,;] thus", ", thus"),
    ("however [\w]", ", however,"),
    ("Moreover [\w]", "Moreover,"),
    ("However [\w]", "However,"),
    ("For example [\w]", "For example,"),
    ("Next [\w]", "Next,"),
    ("[^,] but", ", but"),
    ("[\w] while", ", while"),

    # comma before ie eg
    ("[\w] i\.e\.", ", i.e."),
    ("[\w] i\.e\.", ", e.g."),

    # comma after ie eg
    ("i\.e\. [\w]", "i.e.,"),
    ("e\.g\. [\w]", "e.g.,"),


    ("First [\w]", "First, "),
    ("Second [\w]", "Second, "),
    ("Third [\w]", "Third, "),
    ("Finally [\w]", "Finally, "),
    # ("Then [\w]", "Then, "),
    ("Next [\w]", "Next, "),

    ("First} [\w]", "First, "),
    ("Second} [\w]", "Second, "),
    ("Third} [\w]", "Third, "),
    ("Finally} [\w]", "Finally, "),
    ("Unfortunately [\w]", "Unfortunately, "),

    ("instead [\w]", "Unfortunately, "),
    ("[\w] instead", "Unfortunately, "),



    ]
    # ("", ""),

    for exp in reg_exsps:
        p = re.compile(exp[0])
        m = p.search(line)
        if m:
            left_index,_ = m.span()
            print_warning(file_name, line_number, line, m.group(), left_index, message=" (use: %s ?)"%(exp[1]))