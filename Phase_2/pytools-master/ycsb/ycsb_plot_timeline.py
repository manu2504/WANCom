#!/usr/bin/python
import argparse
import logging
import os.path
import pandas as pd
import joblib

from pytools.plots.py_plot import pyplot_colors, create_ecdf_for_plot, suggest_plots_lims
from pytools.ycsb.ycsb import *
from pytools.common.io import *
import ycsb_common as ycsb

import matplotlib.pyplot as plt
from matplotlib import dates

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s", datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("plot_ycsb_timeline")


def plot_timeseries(ts, of_name):

    plt.figure(figsize=(12,12), dpi=500)

    ts.plot(style='k--', label='Series')

    plt.ylabel('CDF')
    plt.xlabel('Latency ms')
    plt.title('Request Completion Time')
    plt.legend(loc="best")

    log.info("Output file: {}".format(of_name))
    plt.savefig(of_name)

def _proc(ycsb_log):

    logging.debug("Processing: [%s]", ycsb_log)

    ts = load_ycsb_raw_2_ts(ycsb_log)

    plot_timeseries(ts, ycsb_log + "timeline.png")

    io_timeseries_to_unix_csv(ts, ycsb_log+".timeline.csv")

def plot_ycsb_timelines(ifiles):

    tasks = (
        joblib.delayed(_proc)(ifile)
        for ifile in ifiles
    )
    joblib.Parallel(n_jobs=-1, verbose=50)(tasks)


if __name__ == '__main__':

    parser = argparse.ArgumentParser("Plot YCSB Raw Timeline",
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    FLAGS = parser.parse_args()

    ifiles = ycsb.get_source_files(FLAGS, flatten=True)
    logging.info("File Groups: [%s]", ifiles)

    plot_ycsb_timelines(ifiles)



