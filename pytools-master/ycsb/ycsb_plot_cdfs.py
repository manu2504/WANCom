#!/usr/bin/python
import argparse
import logging
import os.path
import pandas as pd
import joblib

import matplotlib.ticker as ticker
import matplotlib
matplotlib.use('Agg')
from pytools.plots.py_plot import pyplot_colors, create_ecdf_for_plot, suggest_plots_lims
from pytools.ycsb.ycsb import *
from pytools.common.io import *
from pytools.experiments.exp_common import make_dir
from pytools.plots.py_plot import *
from pytools.common.common import *
from pytools.ycsb.ycsb_results_aggregator import get_slo_violations4df
import pytools.ycsb.parsing.parse_ycsb_file_list as ycsb_list_parser
import pytools.ycsb.ycsb_results_aggregator as aggregator

import ycsb_common as ycsb
import matplotlib.pyplot as plt
from matplotlib import dates
from ycsb import *

# number of sample points to plot CDF
PLOT_CDF_RESOLUTION=10000

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s",
    datefmt='%H:%M:%S', level=logging.DEBUG)



def get_total_slo_violations(slo_violations_dic):
    """ Function computes total SLO violations from individual ycsb files. results are
    pre-processed and passed in via the dictionary which contains total operations and total
    failed operations per ycsb file """

    total_ops = 0
    total_slo_failed_ops = 0
    for slo_dic in slo_violations_dic:
        total_ops += slo_dic["total_operation_count"]
        total_slo_failed_ops += slo_dic["slo_violations_count"]

    total_slo_violations_prcnt = total_slo_failed_ops / (total_ops / 100.0)

    return total_slo_violations_prcnt


def plot_ycsb_cdfs(file_groups, out_name, out_data_file="out.csv", pre_parsed_input=False,
    skip_first_samples_min=1, xlim=60, style_linestyle_per_group=True):

    flattened_file_list = [i for i in itertools.chain.from_iterable(file_groups)]

    parsed_dfs = ycsb_list_parser.parse_ycsb_file_list(
        flattened_file_list, pre_parsed_input, skip_first_samples_min,
        FLAGS.consider_siblings, FLAGS.n_jobs)



    # <4.> Compute SLO violations
    logging.info("Computing SLO violations at [%i ms]", FLAGS.target_latency_slo_us/1000)
    tasks = (joblib.delayed(get_slo_violations4df)(df, FLAGS.target_latency_slo_us, "latency_us")
        for df in parsed_dfs)
    slo_violations_dic = joblib.Parallel(n_jobs=1, verbose=50)(tasks)

    _plot_cdfs(file_groups, out_name, xlim, style_linestyle_per_group,
        parsed_dfs, slo_violations_dic)



def _plot_cdfs(
    file_groups, out_name, xlim, style_linestyle_per_group, parsed_dfs, slo_violations_dic):

    # PLOTTING STARTS BELOW

    plt.figure(dpi=1000, figsize=(10,6))
    plot_count = 0
    linewidth = 3
    for i_g, fgroup in enumerate(file_groups):
        for i_f, ifile in enumerate(fgroup):
            logging.info("Plotting file: [%s]",  ifile)

            # color = pyplot_colors[i % len(pyplot_colors)]

            if style_linestyle_per_group:
                linestyle = ppnext_linestyle(i_g)
                color = ppnext_color(i_f)
            dframe = parsed_dfs[plot_count]

            samples = dframe["latency_us"]
            x,y = create_ecdf_for_plot(samples, PLOT_CDF_RESOLUTION)
            x /= 1000


            length_of_experiment = \
                parsed_dfs[i_f].iloc[-1]["datetimestamp"] - parsed_dfs[i_f].iloc[0]["datetimestamp"]

            length_of_experiment_mins = (length_of_experiment.seconds/60.0)

            length_of_experiment = 10
            lines_label = "{src_fname_no_extension} slo {slo:.2f}% "\
                          "[{mops:.1f} Mops {length_min:.1f} mins]".format(
                src_fname_no_extension=os.path.basename(ifile).split('.')[0],
                slo=slo_violations_dic[plot_count]["slo_violations_percent"],
                mops=(slo_violations_dic[plot_count]["total_operation_count"] / 1000.0 / 1000.0),
                length_min=length_of_experiment_mins
                )
            plt.plot(
                x, y, label=lines_label, color=color,
                linestyle=linestyle, linewidth=linewidth)

            plot_count += 1

    plt.xlim(0, xlim)

    plt.ylabel('CDF')
    plt.xlabel('Latency ms')

    plt.title(
        "Request Completion Time. SLO [%s ms] Total SLO v. %.2f%%" % (
            (FLAGS.target_latency_slo_us / 1000),
            get_total_slo_violations(slo_violations_dic))
        )

    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 11})

    plt.grid()
    # make_dir(FLAGS.out_dir)
    if not out_name:
        out_name = file_groups[0][0] + ".cdf.png"
    logging.info("Output file: %s", out_name)
    plt.savefig(out_name, bbox_inches='tight')



if __name__ == '__main__':

    parser = argparse.ArgumentParser("""Script plot CDFs for each .ycsb file report""",
        parents=[
            ycsb.get_default_arguments(),
            ycsb_list_parser.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--xlim", default=60, type=int)
    parser.add_argument("--n_jobs", default=-1, type=int)
    parser.add_argument("--out_name", default="")
    parser.add_argument("--style_linestyle_per_group", default=True, action="store_true",
        help="""If set, all plots within each group will have one line style, note
        there are only 4 line types, thus 4 groups max""")

    FLAGS = parser.parse_args()

    if not FLAGS.src_files:
        found_jsons = get_files_matching_mask(where="./", mask="*.ycsb")
        FLAGS.src_files = found_jsons

    file_groups = ycsb.get_source_files(FLAGS, flatten=False)
    for f in file_groups:
        # sort all file names in the group, to have persistent order of files names across plots
        f.sort()
    logging.info("File Groups: [%s]", file_groups)



    if not FLAGS.out_data_file:
        FLAGS.out_data_file = "out.csv"

    plot_ycsb_cdfs(file_groups, FLAGS.out_name, FLAGS.out_data_file, FLAGS.pre_parsed_input,
        FLAGS.skip_first_samples_min,
        FLAGS.xlim, FLAGS.style_linestyle_per_group)

