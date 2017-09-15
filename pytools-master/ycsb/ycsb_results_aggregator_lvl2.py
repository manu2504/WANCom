#!/usr/bin/python
import argparse
import logging
import pandas as pd
import numpy as np

from pytools.common.io import io_tuple_list2file

import ycsb_common as ycsb


logging.basicConfig(
    format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s",
    datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("ycsb_results_aggregator_lvl3")


def combine_individual_results_into_df(ifiles):
    df = pd.DataFrame()

    for f in ifiles:
        d = pd.read_csv(f, index_col=0)
        if df.empty:
            df = d
        else:
            df = pd.concat([df, d])


    # Manual re-indexing
    df.index = list(range(0, len(df)))
    df.reindex()
    print df

    return df

def aggregate_ycsb_aggr_files_lvl2(ifiles):

    df = combine_individual_results_into_df(ifiles)

    y_value_col_name = FLAGS.yaxis_column
    x_value_col_name = FLAGS.xaxis_column

    out_2plot_median_tuples = []
    out_2plot_all_tuples = []

    distinct_measurements = list(set(df[x_value_col_name]))

    for key in distinct_measurements:

        d = df[df[x_value_col_name] == key]

        # Note, we do not remove duplicate entries here, because it does not affect the measurement
        values = (list(d[y_value_col_name]))

        median_target = np.percentile(values, 50)
        print median_target

        for v in values:
            out_2plot_all_tuples.append((key, v))

        out_2plot_median_tuples.append((key,median_target))


    out_2plot_all_tuples = sorted(out_2plot_all_tuples, key=lambda x: int(x[0]))
    out_2plot_median_tuples = sorted(out_2plot_median_tuples, key=lambda x: int(x[0]))

    print out_2plot_median_tuples

    print out_2plot_all_tuples

    io_tuple_list2file(out_2plot_median_tuples, "medians.csv")
    io_tuple_list2file(out_2plot_all_tuples, "all.csv")


if __name__ == '__main__':

    parser = argparse.ArgumentParser("""  --- """,
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--xaxis_column", type=str, default="modelintervalms",
        help="What wales to be displayed across X-axis")
    parser.add_argument("--yaxis_column", type=str, default="total_slo_violations_prcnt",
        help="What wales to be displayed across Y-axis")

    FLAGS = parser.parse_args()

    ifiles = ycsb.get_source_files(FLAGS, flatten=True)
    logging.info("File Groups: [%s]", ifiles)


    aggregate_ycsb_aggr_files_lvl2(ifiles)


