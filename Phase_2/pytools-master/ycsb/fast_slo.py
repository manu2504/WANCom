#!/usr/bin/python
import argparse
import logging
import os.path
import pandas as pd
import joblib
import subprocess
import csv

from pytools.plots.py_plot import pyplot_colors, create_ecdf_for_plot, suggest_plots_lims
from pytools.ycsb.ycsb import *
from pytools.common.io import *
from pytools.common.common import merge_dicts
from pytools.experiments.exp_common import make_dir

import ycsb_common as ycsb
import matplotlib.pyplot as plt
from matplotlib import dates
from pytools.common.common import *

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s", datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("plot_ycsb_timeline")


PERCENTILES = [0,50,90,95,99,99.9,99.99, 100]

def get_metric_tuples(ifile):
    matching_patterns = [
    "[OVERALL], RunTime(ms)",
    "[OVERALL], Throughput(ops/sec)",
    "[READ], Average",
    "[READ], Min",
    "[READ], Max",
    "[READ], p1,",
    "[READ], p5,",
    "[READ], p50,",
    "[READ], p90,",
    "[READ], p95,",
    "[READ], p99,",
    "[READ], p99.9,",
    "[READ], p99.99",
    "[READ], SLO Violations(%)",
    "[READ], Operations",
    "[HdrREAD], Average",
    "[HdrREAD], Min",
    "[HdrREAD], Max",
    "[HdrREAD], p1,",
    "[HdrREAD], p5,",
    "[HdrREAD], p50,",
    "[HdrREAD], p90,",
    "[HdrREAD], p95,",
    "[HdrREAD], p99,",
    "[HdrREAD], p99.9,",
    "[HdrREAD], p99.99",
    "[HdrREAD], SLO Violations(%)",
    "[HdrREAD], Operations",


    # "[UPDATE], Min,",
    # "[UPDATE], Max,",
    # "[UPDATE], p1,",
    # "[UPDATE], p5,",
    # "[UPDATE], p50,",
    # "[UPDATE], p90,",
    # "[UPDATE], p95,",
    # "[UPDATE], p99,",
    # "[UPDATE], p99.9,",
    # "[UPDATE], p99.99,"
    ]

    ret_dic = {}

    proc = subprocess.Popen(["tail","-n", "1000", ifile], stdout=subprocess.PIPE)
    stat_dic = {}
    while True:
        line = proc.stdout.readline()

        for pid, pattrn in enumerate(matching_patterns):

            if line.startswith(pattrn):
                unspaced_pattrn = pattrn.translate(None, ", ")

                # each pattern should be matched only once
                assert unspaced_pattrn not in ret_dic

                value = line.rstrip().split(" ")[-1]
                # First 2 patterns (see above) are for overal time, throughput
                # Thus, no need to translate to ms
                if pid > 1:
                    value_ms = float(value)
                else:
                    value_ms = value
                ret_dic[unspaced_pattrn] = value_ms


        if line == '':
            break

    return ret_dic

def get_stats_percentiles_from_ts(ts, percentiles=[99,50]):
    ret_dic = {}
    values = np.asarray(ts.values)
    for p in percentiles:
        ret_dic["%.2fp" % p] = np.percentile(values, p)

    return ret_dic


def get_index_by_value(ifile):
    """
    This function parses out initial configuration from the command line, which looks like:
    Command line: -db com.yahoo.ycsb.db.CassandraCQLClient -P workloads/workloadc -s -p
    operationcount=500000 -p recordcount=1000000 -threads 512 -p hosts=10.0.1.1 -p
    port=9042 -p cassandra.readconsistencylevel=ONE -p cassandra.writeconsistencylevel=ONE
    -p measurementtype=raw -target 9000 -tYCSB Client 0.13.0-SNAPSHOT
    """

    logging.info("Reading file: [%s]", ifile)
    # proc = subprocess.Popen(["head","-n", "1000", ifile], stdout=subprocess.PIPE)
    # proc.wait()

    with open(ifile, "r") as f:
        for line in f.readlines(1000):
            if line.startswith("Command line:"):
                tokens = line.split(" ")
                for i in range(0, len(tokens)):
                    if tokens[i].startswith(FLAGS.aggregate_by):
                        if FLAGS.aggregate_by.endswith("="):
                            # Capturing cases like: measurementtype=raw
                            return tokens[i].split("=")[1]
                        else:
                            # Capturing cases like: -target 9000
                            print tokens[i+1]
                            return tokens[i+1]

    return None



def process_result_file(ifile, skip_first_mins):

    ret_dic = get_metric_tuples(ifile)

    index_value = get_index_by_value(ifile)

    ret_dic["file"] = ifile

    if not index_value:
        index_value = -1
        logging.error("Could not obtain group by index for file: [%s]", ifile)
    ret_dic["index"] = index_value

    return (ifile, ret_dic)

def get_ycsb_aggregates(ifiles, out_dir, out_data_file, skip_first_mins, no_out_merge=False):
    logging.info("Running [%s] [%s] [%s] [no_out_merge=%s]",
        ifiles, out_dir, out_data_file, no_out_merge)

    tasks = (joblib.delayed(process_result_file)(ifile, skip_first_mins)
            for ifile in ifiles)
    res_tuples = joblib.Parallel(n_jobs=-1, verbose=50)(tasks)

    res_tuples = sorted(res_tuples, key=lambda k: k[1]["index"])

    # total_operations = 0
    # for r in res_tuples:
    #     total_operations += r["[HdrREAD]Operations"]

    # print "TOTAL operations: ", total_operations

    if no_out_merge:

        for ifile, idata in res_tuples:
            out_file_name = os.path.basename(ifile) + ".aggregate"
            out_file_name = os.path.join(
                os.path.dirname(ifile),
                out_file_name
                )

            logging.info("Writing to file: [%s]", out_file_name)
            io_diclist2csv([idata], out_file_name, delimeter=" ")
    else:
        make_dir(out_dir)
        if not out_data_file:
            out_data_file = ifiles[0] + ".csv"
        logging.info("Writing to file: [%s]", os.path.join(out_dir, out_data_file))
        io_diclist2csv(
            [x[1] for x in res_tuples], os.path.join(
                out_dir, out_data_file), delimeter=" ")


if __name__ == '__main__':

    parser = argparse.ArgumentParser("""Script process a set of ycsb report files. For
        each file a set of aggregate values such as median, 99th, max etc, are extracted.
        The output is presented in a csv file""",
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--no-out-merge', action='store_true', default=False,
        help="""If set, files will not be merged into single output (for statistical
         plots), but instead will produce .aggreage files per input file""")

    parser.add_argument("--aggregate_by", default="-threads", type=str,
        help="Aggregated results will be sorted by this configuration option.")

    parser.add_argument("--skip_first_samples_min", default="2", type=int,
        help="Option to skip front samples, that can be associated with warm up time.")

    parser.add_argument("--slo_us", default=30000, type=int,
        help="Compute SLO violation count")

    assert False, "Deprecated Script, remove!"
    FLAGS = parser.parse_args()

    if not FLAGS.src_files:
        found_jsons = get_files_matching_mask(where="./", mask="*.ycsb")
        FLAGS.src_files = found_jsons
    if not FLAGS.out_data_file:
        FLAGS.out_data_file = "out.csv"

    ifiles = ycsb.get_source_files(FLAGS, flatten=True)
    logging.info("File Groups: [%s]", ifiles)


    get_ycsb_aggregates(ifiles, FLAGS.out_dir, FLAGS.out_data_file, FLAGS.skip_first_samples_min, FLAGS.no_out_merge)