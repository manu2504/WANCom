#!/usr/bin/python

import re
import logging
from common import *


def check_line_for_unwanted_patterns(file_name, line, line_number):

    reg_exsps = [
    ("pick up","pick", []),
    ("which leads","leads", []),
    ("are then","are", []),

    ("[N|n]etwork state","network's state", []),
    ("[N|n]etwork condit","network's", []),
    ("[N|n]etwork utili","network's", []),



    # ("network+[ ]+[\w]+[ ]+state","network's state", []),

    ("strong and weak","advantages and disadvantages", []),
    ("one hand side","one side", []),
    ("consider a ","considering", []),
    ("Consider a ","considering", []),

    ("[L|l]atency delay class ","latency class", []),


    # ("Consider a ","considering", []),


    ("not clear","unclear", []),
    ("not sufficient","insufficient", []),
    ("not necessary","unnecessary", []),
    ("than it is","than is", []),
    ("dependent on","depends on", []),

    ("from a target","of a target", []),
    ("from the target","of the target", []),
    ("look into","investigate", []),
    ("on Figure","in Figure", []),
    ("at the times when","when", []),

    ("significant","perhaps large?", []),

    ("higher is the","higher the", []),
    ("lower is the","lower the", []),
    ("greater is the","greater the", []),
    ("a lot of","many", []),
    ("when exactly","exactly when", []),
    ("can expect","expect", []),
    ("has been defined","defined", []),
    ("tells us", "states", []),
    ("erformance over", "performance on", []),
    ("[s] has", "have", []),
    ("real time", "real-time", []),
    ("[B|b]ack end","back-end", []),
    (" [R|r]e[ |~|-]*eval"," \mbox{re-evaluate} non separatable dash", []),

    # (" a [a-zA-Z]+[s]+[ \.\,;:]+", "Remove article?", [" a weakness "]),
    # (" a [a-zA-Z]+[ ]+[a-zA-Z]+[s]+[ \.\,;:]+", "Remove article?", []),
    ("this [\w]+[s]+[^\w]", "Use these?", ["this is ", "this suggests ", "this differs ", "this was "]),
    # ("significantly", "a lot ?"),

    # ("[0-9]+[ ~]+hours", "x-hour", []),
    ("[0-9]+[ ]+(ms|sec|min|hour|Hz)", "use ~ between number and a measurement", []),

    ("[T|t]o be able to", "simply: to", []),

    ("minimal", "minimum", []),


    # DASHED WORDS

    ("non intuitive", "non-intuitive", []),
    ("[O|o]ne way", "one-way", []),

    # WORD ORDERING

    (" only used", "used only", []),
    (" only with", "with only", []),
    ("the only", "only the", []),

    # This as example demonstrates ==> As this example demonstrates
    ("this as", "as this", []),

    # Alternative Suggestions
    ("enough", "perhaps: sufficient/insufficient?", []),
    (" pace", "perhaps: rate?", []),
    ("[D|d]epend on", "perhaps: depend upon", []),
    ("[D|d]epends on", "perhaps: depends upon", []),




    ("axes", "axis?, ex: The X axis, Many axes", []),


    ("[T|t]hen", "consider synonym: Subsequently", []),

    ("[O|o]rder at which", "order IN which", []),
    ("only from", "of only", []),

    ("desire to provide", "perhaps: want to achieve ?", []),

    ("[A|a]s a result", "perhaps: thus ?", []),

    ("[W|w]ith accordance", "perhaps: in accordance ?", []),
    ("accordance to", "perhaps: accordance with?", []),

    ("[N|n]ot possible", "perhaps: impossible?", []),


    ("[K|k]ernel level", "perhaps: kernel space?", []),
    ("[U|u]ser level", "perhaps: user space?", []),


    ("guarantee", "perhaps: ensure?", []),

    ("[V|v]iew into", "perhaps: view of?", []),

    ("Cassandra's requests", "Cassandra requests", []),

    ("[A|a]pplication's requests", "application requests", []),

    ("the interference", "interference", []),

    ("performed frequently", "frequently performed", []),

    ("improving the performance", "no _the_", []),

    ("with regard to", "avoid, potentially: while taking advantage of...."),

    ("not able", "unable", []),
    ("in the multiple", "multiples", []),

    ("not active", "inactive", []),

    ("according to", "as described in", []),
    ("not practical", "impractical", []),

    ("clients threads", "client threads", []),

    ("need only", "only need", []),





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


    p = re.compile(" a [a-zA-Z]+[s]+[ \.\,;:]+")
    m = p.search(line)
    if m:
        left_index,_ = m.span()
        word = fix_spaces(m.group()).split(" ")[-1]
        if word in NOUNS and is_plural(word):
            print_warning(file_name, line_number, line, m.group(),
                left_index, message=" (use: Remove article?)")
        else:
            logging.debug("Ignoring case: %s " % (m.group()))

    # Example: a large numbers
    match, left_indx, _ = match_reg(line, " a [a-zA-Z]+[ ]+[a-zA-Z]+[s]+[ \.\,;:]+")
    if match:
        tokens = fix_spaces(match).split(" ")
        word = tokens[-1]
        if word in NOUNS and is_plural(word):
            print_warning(file_name, line_number, line, match,
                left_indx, message=" (use: Remove article(2)?)")
        else:
            logging.debug("Ignoring case: %s " % match)


    # [x, y, and z] comma case, check x, y are nouns
    p = re.compile("[a-zA-Z]+, [a-zA-Z]+ (and).")
    m = p.search(line)
    if m:
        substr = m.group()
        substr.translate(None, ",")

        word_x = m.group().split(" ")[0]
        word_y = m.group().split(" ")[1]

        if word_x in NOUNS and word_y in NOUNS:
            left_index,_ = m.span()
            print_warning(file_name, line_number, line, m.group(),
                left_index, message=" (use: x, y, and z?)")
        else:
            logging.debug("Ignoring case: %s " % (m.group()))