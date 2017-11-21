#!/usr/bin/python

import argparse
import joblib
import logging
import multiprocessing
import ntpath
import os.path
import pandas as pd
import subprocess
import time

from pytools.plots.py_plot import pyplot_colors, create_ecdf_for_plot, suggest_plots_lims
from pytools.ycsb.ycsb import *

from pytools.experiments.exp_common import make_dir
from ycsb_common import get_source_files
import matplotlib.pyplot as plt
from matplotlib import dates
import ycsb_common as ycsb

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s", datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("plot_ycsb_hist")


def plot_reservoir_cdf(reservoir, label, title="", scale=1/1000.0):

    if len(reservoir) == 0:
        return
    x, y = create_ecdf_for_plot(reservoir*scale, 1000)
    plt.step(x, y, label=label)

    if len(FLAGS.latency_lims):
        plt.xlim(FLAGS.latency_lims[0], FLAGS.latency_lims[1])
    else:
        xmin, xmax = suggest_plots_lims([reservoir*scale], 0, 99.9)
        plt.xlim(xmin, xmax)

    plt.grid()
    plt.xlabel("Latency [ms]")
    plt.ylabel("CDF")
    plt.title(title)
    plt.legend(loc="lower right")

def plot_reservoir_hist(reservoir, label, scale=1/1000.0):

    _,_,_ = plt.hist(
        reservoir*scale, FLAGS.hist_buckets, normed=0, facecolor='green', alpha=0.75)

    if len(reservoir) == 0:
        return

    if len(FLAGS.latency_lims):
        plt.xlim(FLAGS.latency_lims[0], FLAGS.latency_lims[1])
    else:
        xmin, xmax = suggest_plots_lims([reservoir*scale], 0, 99.9)
        plt.xlim(xmin, xmax)

    plt.xlabel('Latency [ms]')
    plt.ylabel('Frequency')


    plt.grid(True)

def plot_reservoir_series(ts, p, res_size, label, ax, scale=1/1000.0):


    x_min_time = p - res_size/2
    x_max_time = p + res_size/2 + res_size

    plot_data = ts[x_min_time.to_timestamp(): x_max_time.to_timestamp()]
    plt.plot(plot_data.index, plot_data*scale, "k.", label=label)

    if len(plot_data) == 0:
        return


    plt.plot([ p.to_timestamp(), p.to_timestamp()], [0, 1000000], color="r", label="Res border",  )
    plt.plot([ (p+res_size).to_timestamp(), (p+res_size).to_timestamp()], [0, 1000000], color="g", label="Res border" )



    if len(FLAGS.latency_lims):
        plt.ylim(FLAGS.latency_lims[0], FLAGS.latency_lims[1])
    else:
        ymin, ymax = suggest_plots_lims([plot_data*scale], 0, 99.9)
        plt.ylim(ymin, ymax)

    plt.xlabel("Time")
    plt.ylabel("Latency [ms]")
    plt.grid()
    hfmt = dates.DateFormatter('%H:%M:%S')




    ax.xaxis.set_major_locator(dates.SecondLocator())
    ax.xaxis.set_major_formatter(hfmt)
    plt.xticks(rotation=45)
    # .gcf().autofmt_xdate()
    # plt.legend(loc="best")



def ts2triple_plot(ts, period, res_size, index):
    """
    Plots 3 sub-plots, CDF, Histogram, and Timesires
    """

    ts_data = ts[period.to_timestamp(): (period+res_size).to_timestamp()]

    plt.figure(figsize=(FLAGS.figure_size_dpi[0],FLAGS.figure_size_dpi[1]),
        dpi=FLAGS.figure_size_dpi[2])

    title = "[frame_step_ms: %i][res_size_ms: %i]" % (FLAGS.step_ms, FLAGS.res_size_ms)
    ax = plt.subplot(3,1,1)

    label = "[samples: {size}]".format(size=len(ts_data))
    plot_reservoir_cdf(ts_data.values, label=label, title=title)

    ax = plt.subplot(3,1,2)

    label="Hist"
    plot_reservoir_hist(ts_data.values, label=label)

    ax = plt.subplot(3,1,3)

    plot_reservoir_series(ts, period, res_size, "Samples", ax)



    plt_out_file = FLAGS.out_image_frmt_name % index
    if not os.path.exists(FLAGS.out_dir):
        os.mkdir(FLAGS.out_dir)
    of_name = os.path.join(FLAGS.out_dir, plt_out_file)
    plt.savefig(of_name)
    logging.debug("Plotting [%s]", of_name)

    plt.cla()
    plt.clf()
    plt.close()

def count_intervals_in_ts(ts, period_len_ms):

    ts_len_ns = (ts.index[-1]-ts.index[0]).to_timedelta64()
    ts_len_ms = ts_len_ns / 1000 / 1000

    return ts_len_ms / period_len_ms


def _ts2triple_plot(ts, start_period, start_index, end_index):

    for i in xrange(start_index, end_index):
        ts2triple_plot(ts, start_period+i*FLAGS.step_ms, FLAGS.res_size_ms, index=i)

if __name__ == '__main__':


    parser = argparse.ArgumentParser("""Plot YCSB Raw Histogram""",
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--n_jobs", default=multiprocessing.cpu_count(), type=int, help="CPU threads to use")


    parser.add_argument("--out_image_frmt_name", default="img_%04i.png")
    parser.add_argument("--ffmpeg_image_frmt_name", default="img_%04d.png")


    parser.add_argument("--step_ms", default=100, type=int,
        help="Time step per frame [ms]")

    parser.add_argument("--res_size_ms", default=1000, type=int,
        help="How many samples to keep in a reservoir (based on time interval) [ms]")

    parser.add_argument("--hist_buckets", default=100, type=int,
        help="Number of buckets in the histogram")

    parser.add_argument("--latency_lims", nargs='*', default=[], type=int,
        help="Two values, defining the min and max latency values, if not set the best\
        fit will be used dynamically")


    parser.add_argument("--figure_size_dpi", default=[7,7,200], type=int,
        help="Three number defining the size of the figure per plot + dpi resolution")

    parser.add_argument("--make_video", default=True, action="store_true",
        help="Convert YCSB output into a video and store in designated location")




    FLAGS = parser.parse_args()
    assert FLAGS.n_jobs > 0

    assert (FLAGS.out_dir != "./")
    assert (FLAGS.out_dir != ".")
    make_dir(FLAGS.out_dir)

    src_ycsb_files = get_source_files(FLAGS, flatten=True)
    for ylogs in src_ycsb_files:

        ts = load_ycsb_raw_2_ts(ylogs)

        starting_period = pd.Period(ts.index[0], "S")
        starting_period += 60*5
        ts = ts[:starting_period.to_timestamp()]

        period = pd.Period(ts.index[0], "L") # note: L stands for Millisecond

        total_intervals = count_intervals_in_ts(ts, FLAGS.step_ms)
        logging.info("Total number of intervals: [%i]", total_intervals)

        range_per_thread = total_intervals / FLAGS.n_jobs
        logging.info("Images per thread: [%i]", range_per_thread)

        time.sleep(0.5)

        if os.path.isdir(FLAGS.out_dir):
            print FLAGS.out_dir
            subprocess.check_call("rm {} -rf".format(FLAGS.out_dir), shell=True)

        tasks = (
                joblib.delayed(_ts2triple_plot)(ts, period,
                    i*range_per_thread,
                    (i+1)*range_per_thread)
                for i in range(0, FLAGS.n_jobs)
        )
        joblib.Parallel(n_jobs=FLAGS.n_jobs, verbose=0)(tasks)


        if FLAGS.make_video:
            src_image_files = os.path.join(FLAGS.out_dir, FLAGS.ffmpeg_image_frmt_name)
            out_avi_file = ylogs + ".mp4"
            # os.path.join(
            #     os.path.dirname(ylogs),
            #     path.basename(ylogs) + ".mp4")

            logging.info("Creating AVI from location: %s", src_image_files)
            logging.info("AVI output file: [%s]", out_avi_file)

            subprocess.check_call(
                "ffmpeg -r 30 -start_number 0 -i {}  -c:v libx264  -pix_fmt yuv420p {} -y".format(
                    src_image_files,
                    out_avi_file), shell=True)

























