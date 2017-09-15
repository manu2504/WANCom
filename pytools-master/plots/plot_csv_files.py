#!/usr/bin/python
import argparse
import logging

import pandas as pd

from pytools.plots.py_plot import *

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s", datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("plot_csv_files")


def get_separator():

    if FLAGS.delimeter == "comma":
        return ","
    elif FLAGS.delimeter == "space":
        return " "
    else:
        raise RunttimeError("Unknown separator/delimenter typ [%s]", FLAGS.delimenter)


def prase_src_file_args(f):

    tokens = f.split(",")

    ifname = tokens[0]

    x_cols = []
    y_cols = []
    for i in range(1, len(tokens), 2):
        x_cols.append(int(tokens[i]))
        y_cols.append(int(tokens[i+1]))

    return ifname, x_cols, y_cols

def plot_csv(f):

    ifname, x_cols, y_cols = prase_src_file_args(f)

    df = pd.read_csv(ifname, sep=get_separator())

    # df.names =

    # print x_cols, y_cols

    for xcol, ycol in zip(x_cols, y_cols):

        x = list(df[df.columns[xcol]])
        y = list(df[df.columns[ycol]])

        plt.plot(x, y)

    # print df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Script takes a list of files and plots various columns into a single output file.",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--out_file", default="out_csv.png", type=str,
        help="The name of the output file")


    parser.add_argument("--xlabel", default="Time", type=str,
        help="Label on the X axis")

    parser.add_argument("--ylabel", default="Y-values", type=str,
        help="Label on the Y axis")

    parser.add_argument("--title", default="Title", type=str,
        help="Title of the plot")

    parser.add_argument("--src_files", nargs='*', default=[], type=str,
        help="""List of strings of the format <file_name>,<x1_col>,<y1_col>,<x2_col>,<y2_col>""")

    parser.add_argument("--delimeter", default="comma", type=str, choices=["comma", "space"],
        help="""Type of the delimeters allowed""")

    FLAGS = parser.parse_args()


    plt.figure(dpi=1000, figsize=(10,6))



    plt.ylabel(FLAGS.ylabel)
    plt.xlabel(FLAGS.xlabel)
    plt.title(FLAGS.title)


    for f in FLAGS.src_files:
        plot_csv(f)

    plt.grid()
    log.info("Output file: {}".format(FLAGS.out_file))
    plt.savefig(FLAGS.out_file, bbox_inches='tight')