#!/usr/bin/python
import argparse
import logging
import pandas as pd
import subprocess
import re

from pytools.plots.py_plot import pyplot_colors, create_ecdf_for_plot, suggest_plots_lims
from pytools.ycsb.ycsb import *
from pytools.common.io import *
from pytools.common.common import merge_dicts, remove_non_alphanumerics
from pytools.experiments.exp_common import make_dir


import ycsb_common as ycsb
import matplotlib.pyplot as plt
from matplotlib import dates

import pytools.ycsb.parsing.parse_ycsb_file_list as ycsb_list_parser

logging.basicConfig(
    format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s",
    datefmt='%H:%M:%S', level=logging.DEBUG)

ARGS_DELIMETER = "|"
OUTPUT_AGGRETATION_FILE = "stats.csv.aggr"

def get_metrics_from_ycsb_statistics(ifile):
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
    "[READ], p99.99,"

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
                    value_ms = float(value) / 1000.0
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


def get_slo_violations4df(df, slo_us, latency_column_name):

    original_len = len(df)
    slo_violation_count = len(df[df[latency_column_name] > slo_us ])
    slo_violation_percent = slo_violation_count / (original_len / 100.0)

    logging.info("SLO violations above [%s us] is [%s prcnt %s ops] of total operations count [%s]",
        slo_us, slo_violation_percent, slo_violation_count, original_len)

    ret = {}
    ret["total_operation_count"] = original_len
    ret["slo_violations_count"] = slo_violation_count
    ret["slo_violations_percent"] = slo_violation_percent
    return ret

def get_slo_violations4ts(ts, slo_us, skip_first_mins):

    slo_violation_count = ts[ts > slo_us ].count()
    slo_violation_percent = slo_violation_count / (len(ts) / 100.0)
    logging.info("SLO violations above [%s us] after filtering %d minutes  [%s] [%s prcnt] total operations [%s]",
        slo_us, skip_first_mins, slo_violation_count, slo_violation_percent, len(ts))

    ret = {}
    ret["total_operation_count"] = len(ts)
    ret["slo_violations_count"] = slo_violation_count
    ret["slo_violations_percent"] = slo_violation_percent
    return ret

def get_command_line_from_raw_ycsb(ifile):

    logging.info("Reading file: [%s]", ifile)
    with open(ifile, "r") as f:
        for line in f.readlines():
            if line.startswith("Command line:"):
                # print line
                return line

    return None


def get_args_from_ycsb_file(ifile, aggreate_keys):

    cmdline =get_command_line_from_raw_ycsb(ifile)
    return get_args_from_ycsb_cmd_line(cmdline, aggreate_keys)

def get_args_from_ycsb_cmd_line(cmdline, aggreate_keys):
    """
    This function parses out initial configuration from the command line, which looks like:
    Command line: -db com.yahoo.ycsb.db.CassandraCQLClient -P workloads/workloadc -s -p
    operationcount=500000 -p recordcount=1000000 -threads 512 -p hosts=10.0.1.1 -p
    port=9042 -p cassandra.readconsistencylevel=ONE -p cassandra.writeconsistencylevel=ONE
    -p measurementtype=raw -target 9000 -tYCSB Client 0.13.0-SNAPSHOT

    aggreate_keys is a list of tuples, first tuple is the target parameter name we are looking for,
    and the second element is the delimiter that separates the property from its value

    """

    tokens = re.split(' |,', cmdline)

    target_properties = []
    target_found = False

    for key, delimeter in aggreate_keys:
        for i in range(0, len(tokens)):
            if tokens[i].startswith(key):

                if delimeter == " " or delimeter == "space":
                    if i + 1 < len(tokens):
                        target_properties.append(tokens[i+1])
                        target_found = True
                        break
                    else:
                        logging.error("Expecting a token, but cmd length is exceeded!")
                        target_properties.append("XXX")
                else:
                    target_properties.append(tokens[i].split(delimeter)[1])
                    target_found = True
                    break


        if not target_found:
            logging.error("Failed to find target aggregation key [%s] in YCSB cmd ", key)

    return target_properties



def merge_props_into_df(arg_names, arg_values):

    res_dic = {}
    # for akey in aggr_keys_list:
    key = "_".join(
        [remove_non_alphanumerics(str(x)) for x in arg_names])

    values = "_".join([remove_non_alphanumerics(str(x)) for x in arg_values])
    merge_dicts(res_dic, {key:values})

    return res_dic


def get_arguments_from_command_line(ifile, aggr_targtes):


    res_dic = {}

    cmdline = get_command_line_from_raw_ycsb(ifile)
    assert cmdline != None

    for aggr in aggr_targtes:
        value_list = get_args_from_ycsb_cmd_line(cmdline, aggr)
        merge_dicts(res_dic, merge_props_into_df(aggr, value_list))

    return res_dic

def get_tracefile_offered_load_from_ycsb(ifile):
    """ This function scans through top lines of .ycsb finds tracefile that was used and then
    returnes the load that that trace file offered based on its naming """

    tracefile = get_args_from_ycsb_file(ifile, [("tracefile", "=")])[0]

    ## Trace file format is: synthetic_trace_3000_600_poisson.data_scle_1_ycsb.trace
    return os.path.basename(tracefile).split("_")[2]


def get_custom_properties(ifile, aggr_custom_targets):

    res_dic = {}
    for custom_target in aggr_custom_targets:
        if custom_target == "offered_load":
            return get_tracefile_offered_load_from_ycsb(ifile)
        else:
            raise RunTimeError("Unknown custom aggregation key [%s]", custom_target)

    return res_dic


def get_total_slo_violations_from_df(df):
    """ Function computes total SLO violations from individual ycsb files. results are
    pre-processed and passed in via the dictionary which contains total operations and total
    failed operations per ycsb file """

    total_ops = 0
    total_slo_failed_ops = 0

    for index, row in df.iterrows():

        total_ops += row["total_operation_count"]
        total_slo_failed_ops += row["slo_violations_count"]

    total_slo_violations_prcnt = total_slo_failed_ops / (total_ops / 100.0)

    return total_slo_violations_prcnt


def get_trace_length_mins(parsed_df):

    length_of_experiment = \
                parsed_df.iloc[-1]["datetimestamp"] - parsed_df.iloc[0]["datetimestamp"]

    length_of_experiment_mins = (length_of_experiment.seconds/60.0)

    return {"trace_length_min":length_of_experiment_mins}


def get_ycsb_aggregates(ifiles, aggr_targtes, aggr_custom_targets, skip_first_mins):

    parsed_dfs = ycsb_list_parser.parse_ycsb_file_list(ifiles,
            FLAGS.pre_parsed_input, FLAGS.skip_first_samples_min,
            FLAGS.consider_siblings, 1)

    tss = [convert_parsed_df_to_ts(d) for d in parsed_dfs]

    res_df = pd.DataFrame()
    for i, f in enumerate(ifiles):

        res_dic = {"filename":f}

        # <1.> Get everything we can from YCSB command line, by parsing the head of the ycsb file
        dic = get_arguments_from_command_line(f, aggr_targtes)
        merge_dicts(res_dic, dic)

        # <2.> Compute various percentiles
        dic = get_stats_percentiles_from_ts(tss[i], FLAGS.count_percentiles)
        merge_dicts(res_dic, dic)

        # <3.> Compute SLO violations etc.
        dic = get_slo_violations4ts(tss[i], FLAGS.target_latency_slo_us, skip_first_mins)
        merge_dicts(res_dic, dic)

        # <4.> Compute meta fields....
        dic = get_trace_length_mins(parsed_dfs[i])
        merge_dicts(res_dic, dic)

        # <5.> Compute custom properties
        dic = get_custom_properties(ifiles[i], aggr_custom_targets)
        merge_dicts(res_dic, dic)

        print res_dic

        df = pd.DataFrame(res_dic, index=[i])
        if res_df.empty:
            res_df = df
        else:
            res_df = pd.concat([res_df, df])

        print df

    print res_df


    total_slo_violations = get_total_slo_violations_from_df(res_df)
    res_df["total_slo_violations_prcnt"] = total_slo_violations

    res_df.to_csv(OUTPUT_AGGRETATION_FILE)


def parse_aggregateby_arguments(aggregate_by_fileds):
    """ The input is the list of strings of the form:
    ["recrodcount|=|operationcount=", "-thread| "] the output is the list of tuple lists of the form
    [ [("recordcount","="), ("operationcount", "=")], [("-thread", " ")]"""

    res_list = []
    for sub_arg in aggregate_by_fileds:
        res_list.append(_aggregate_by_string2tuple_list(sub_arg))

    return res_list


def _aggregate_by_string2tuple_list(aggregate_argument):
    """ argument is a string separated by | as an output we convert it into a list of tuples.
    Example:  "recordcount|,|-target| " will be converted to
    [("recorcdount", ","), ("-target", " ")]"""

    tokens = aggregate_argument.split(ARGS_DELIMETER)
    assert len(tokens) % 2 == 0, "Number of arguments must be even"

    tuple_list = []
    for i in range(0, len(tokens), 2):
        logging.info("Parsing aggregate_by argument '%s' --> [%s] [%s]",
            aggregate_argument, tokens[i], tokens[i+1])
        tuple_list.append((tokens[i], tokens[i+1]))

    return tuple_list


if __name__ == '__main__':

    parser = argparse.ArgumentParser("""Script process a set of ycsb report files. For
        each file a set of aggregate values such as median, 99th, max etc, are extracted.
        The output is presented in a csv file""",
        parents=[ycsb.get_default_arguments(), ycsb_list_parser.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--no-out-merge', action='store_true', default=False,
        help="""If set, files will not be merged into single output (for statistical
         plots), but instead will produce .aggreage files per input file""")

    parser.add_argument("--aggregate_by", nargs='*', default=[], type=str,
        help="""List of keys and delimeters by which to aggregate results.
        For example, to capture option 'recordcount=1000000' specify "recordcount|=" to capture by
        more than one argument, say record count and '-target 1000'
        specify "recordcount|=|-target| ". Here we have a list of tuples of the key to search for
        and a delimeter that separates the key from the value. Alternatively, you can say "space"
        if you want to specify space as a delimiter.
        """)

    parser.add_argument("--aggregate_by_custom", nargs='*', default=[], choices=["offered_load"],
        type=str, help="""An optional list of additional arguments by which to aggregate results:
        <offered_load> will look at the trace file name and will extract the offered load. Works
        with synthesized traces only.""")

    parser.add_argument("--count_percentiles", nargs='*', default=[50,90,95,99,99.9], type=float,
        help="""Adds the following percentiles to the aggregate statistics""")

    FLAGS = parser.parse_args()

    ifiles = ycsb.get_source_files(FLAGS, flatten=True)
    logging.info("File Groups: [%s]", ifiles)


    aggr_targtes = parse_aggregateby_arguments(FLAGS.aggregate_by)

    get_ycsb_aggregates(
        ifiles, aggr_targtes, FLAGS.aggregate_by_custom, FLAGS.skip_first_samples_min)
