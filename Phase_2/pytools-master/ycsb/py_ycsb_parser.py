#!/usr/bin/python
import argparse
import json
import logging
import os
import sys
import numpy as np


def verify_token_line4logs(tokens, column_order, dtypes_dic):

    res = []
    try:
        for i, column in enumerate(column_order):
            v = -1

            if dtypes_dic[column] == np.uint16:
                v = np.uint64(tokens[i])
                if v > np.iinfo(np.uint16).max:
                    raise RuntimeError("Detected overflow in np.uint16")
            elif dtypes_dic[column] == np.uint32:
                v = np.uint64(tokens[i])
                if v > np.iinfo(np.uint32).max:
                    raise RuntimeError("Detected overflow in np.uint32")
            elif dtypes_dic[column] == np.uint64:
                v = np.uint64(tokens[i])
            elif dtypes_dic[column] == str:
                v = str(tokens[i])
                if not v or tokens[i] == np.NaN:
                    raise RuntimeError("An empty string should not be converted to str")
                if v not in ["RawREAD"]:
                    raise RuntimeError("Unknown String")
            else:
                assert False, "Cannot verify column data type [%s]" % column

        res.append(v)
    except:
        exec_info = sys.exc_info()
        print "%s: %s" % ("", sys.exc_info())
        return False

    return True



if __name__ == '__main__':

    line_count = 0
    ifile = "/home/kirillb/data_sets_nc/drc/17.06.08.AZEvaluations/5x.cluster.zing/initial_samples/plane_DC_RR_LOCAL_ONE_VTRACE_51_450_LONG/2017-06-16_20:33:02_1/FRANi1_wl1_ycsb.ycsb"
    with open(ifile, "r") as f, open("pyout.txt", "w") as of:
        for line in f:
            line_count += 1
            if line_count % 100000 == 0:
                print line_count

            tokens = line.split(",")

            if len(tokens) != 3:
                continue

            ok = verify_token_line4logs(
                tokens,
                column_order=["opcode", "time_ns", "latency_us"],
                dtypes_dic={"opcode":str, "time_ns":np.uint64, "latency_us":np.uint32} )

            if ok:
                of.write(line)
            else:
                print line
