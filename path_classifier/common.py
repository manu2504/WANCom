#!/usr/bin/python

import config

gen_log = config.get_logger("general", config.log_general)

def merge_dics_of_lists(src_dic, extra_dic):

    for k, v in extra_dic.iteritems():
        if k in src_dic:
            # append two lists together
            src_dic[k] += v
        else:
            src_dic[k] = v

    return src_dic


def dump_path_dic(pd, msg=""):

    for k, v in pd.iteritems():
        for i, p in enumerate(v):
            if i == 0:
                print "%s->[%15s]   %s" % (msg, k, p)
            else:
                print "%s->[%15s]   %s" %(msg, " ", p)


def delete_indexes_from_list(l, indxs):
    for i in sorted(indxs, reverse=True):
        try:
            del l[i]
        except IndexError:
            gen_log.info("Error deleting items from the list, index out of range")
            gen_log.info(l);
            gen_log.info(len(l))
            gen_log.info(i)


def count_paths_in_dic(npcs):
    count = 0
    for k, v in npcs.iteritems():
        count += len(v)
    return count
