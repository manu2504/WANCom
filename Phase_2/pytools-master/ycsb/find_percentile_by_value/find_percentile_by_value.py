#!/usr/bin/python
import argparse
import os
import joblib
import logging
import numpy as np
import scipy as sc

import coloredlogs
coloredlogs.install()

from pytools.ycsb.ycsb_results_aggregator_lvl1 import get_args_from_ycsb_file, \
    get_tracefile_offered_load_from_ycsb, get_metrics_from_ycsb_statistics

from pytools.common.io import io_tuple_list2file
from pytools.ycsb.parsing.parse_ycsb_file import cpp_parse_ycsb_file
from pytools.ycsb.ycsb import skip_ts_head, load_ycsb_raw_2_ts, load_ycsb_parsed_2_ts
import pytools.ycsb.ycsb_common as ycsb
from pytools.ycsb.ycsb_common import PARSED_FILE_EXTENSION, PARSING_VALID_PREFIXES


def get_achieved_load(ifile):

    res_dic = get_metrics_from_ycsb_statistics(ifile)

    if "[OVERALL]Throughput(ops/sec)" not in res_dic:
        logging.error("""YCSB file does not contain OVERALL statistics at the back.
            Cannot determine achieved throughput!""")
        return 0

    return res_dic["[OVERALL]Throughput(ops/sec)"]


def _find_percentile(ts, target_value_us, offset):

    logging.info("Searching percentile for value [%s] offset [%s]", target_value_us, offset)
    res_percentile = sc.stats.percentileofscore(np.asarray(ts.values), target_value_us - offset)

    return (res_percentile, 100.0 - res_percentile, target_value_us - offset, offset)


def find_target_percentile4file(
    ifile, target_value_us, offsets_us, percentiles, skip_first_samples_min, reuse_parsed_files):

    ## Parse file into time series
    out_file_name = "%s.%s" % (ifile, PARSED_FILE_EXTENSION)

    # It might be possible that the file has been parsed already, so we can skip this process
    if reuse_parsed_files and os.path.isfile(out_file_name):
        logging.info("Parsed file [%s] already exists, loading it ...", load_ycsb_parsed_2_ts)
        ts = load_ycsb_parsed_2_ts(out_file_name)

    else:

        cpp_parse_ycsb_file(ifile, out_file_name, valid_prefixes=PARSING_VALID_PREFIXES)

        ts = load_ycsb_raw_2_ts(out_file_name)

        ts = skip_ts_head(ts, skip_first_samples_min)

    tasks = (joblib.delayed(_find_percentile)(ts, target_value_us, offset)
             for offset in offsets_us)
    res_tuples = joblib.Parallel(n_jobs=-1, verbose=50)(tasks)
    res = []
    for r in res_tuples:
        res.append(list(r))
    res_tuples = res

    # <2.> Find target percentiles
    pers = []
    for p in percentiles:
        print "Searchign for percentile, ", p, "value ", np.percentile(ts, p)
        pers.append(np.percentile(ts, p))


    offered_load = get_tracefile_offered_load_from_ycsb(ifile)
    achieved_load = get_achieved_load(ifile)


    for r in res_tuples:
        print pers
        r.append(float(offered_load))
        r.append(float(achieved_load))
        r +=  pers

    return res_tuples


def compute_average_median_values(res_tuple_list, n_files):

    # <1.> compute dictionary containing average value
    sum_dic = {}
    for t in res_tuple_list:
        offset = t[3] # this is index containing the found percentiles

        if offset not in sum_dic:
            sum_dic[offset] = t[0]
        else:
            sum_dic[offset] += t[0]

    # <2.> compute average percentile
    for k, v in sum_dic.iteritems():
        sum_dic[k] = 1.0 * v / n_files

    # <3.> set the average percentile based on the offset. Hence, even if there are multiple entries
    # per offset, they all will get the same average.
    for t in res_tuple_list:
        t.append(sum_dic[t[3]])
        t.append(100.0 - sum_dic[t[3]])

    return res_tuple_list



def find_target_percentile4files(
    ifiles, target_value_us, offsets_us, percentiles, skip_first_samples_min, reuse_parsed_files):

    res_tuples = []
    for ifile in ifiles:
        res_tuples += find_target_percentile4file(
            ifile, target_value_us, offsets_us, percentiles,
            skip_first_samples_min, reuse_parsed_files
            )

    res_tuples = compute_average_median_values(res_tuples, len(ifiles))

    return res_tuples

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Script searches for a percentile that corresponds to a supplied value.",
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--target_value_us", default=30000, type=int,
        help="A value to which to match the percentile")

    parser.add_argument("--skip_first_samples_min", default=0, type=int,
        help="""Option to skip front samples, that can be associated with warm up time.
        Note, this property will not work if --reuse_parsed_files is used. """)

    parser.add_argument("--offsets_us", nargs='*', default=[0], type=int,
        help="""The offset is used to find percentile that are matched for remote nodes.""")

    parser.add_argument("--percentiles", nargs='*', default=[50], type=int,
        help="""We can also measure and output a list of percentiles""")

    parser.add_argument('--reuse_parsed_files', action='store_true', default=False,
        help="""If file name with *.%s extension will be found in the folder where *.ycsb file
        resides. The parsed version will be used instead. That will save parsing time. Note, in
        this case the --skip_first_samples_min property will
        not be applied.""" % PARSED_FILE_EXTENSION)

    FLAGS = parser.parse_args()

    file_groups = ycsb.get_source_files(FLAGS, flatten=True)
    logging.info("File Groups: [%s]", file_groups)

    if not FLAGS.out_data_file:
        FLAGS.out_data_file = "out.csv"

    res_tuples = find_target_percentile4files(
        file_groups, FLAGS.target_value_us, FLAGS.offsets_us,
        FLAGS.percentiles, FLAGS.skip_first_samples_min, FLAGS.reuse_parsed_files)

    print "___RESULTS___"
    for t in res_tuples:
        print t

    data = []
    for t in res_tuples:
        data.append(tuple(t))

    io_tuple_list2file(data, FLAGS.out_data_file, ",")
