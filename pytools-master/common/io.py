#!/usr/bin/python
import csv
import itertools
import numpy as np

def io_timeseries_to_unix_csv(data, fname, div=0, write_index=True):
    """
    Converts index column of a time series from timestamp to
    unix int format. For example, to be plotted with gnuplot.

    Arguments:
        data {[type]} -- pd.Series() with time as index
        fname {[type]} -- out file name
    """

    d = data.copy(deep=True)
    d.index = d.index.astype(np.int64)
    if div > 0:
    	d.index /= div
    d.to_csv(fname, sep=" ", index=write_index)


def io_dic2csv(dic, ofname, delimiter=" "):
    """Writes a dictionary of lists of a different length into a text file.
    Each column can have a different length.
    Can be used with gnuplot etc.
    """
    with open(ofname, "wb") as outfile:
        writer = csv.writer(outfile, delimiter=delimiter)
        writer.writerow(dic.keys())
        writer.writerows(itertools.izip_longest(*dic.values()))

def io_diclist2csv(dic_list, ofname, delimeter=" "):
    """Writes a list of dictionaries (containing the same keys!) into a text file.
    Each column corresponds to the values of a given key"""

    keys = dic_list[0].keys()
    with open(ofname, "wb") as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=delimeter)
        dict_writer.writeheader()
        dict_writer.writerows(dic_list)


def io_list2file(values, ofname, vertical=True):
    """ Simply writes a list vertically or horizontally into a file"""

    with open(ofname, "wb") as outfile:

        if vertical:
            for v in values:
                outfile.write("%s\n" % v)
        else:
            for v in values:
                outfile.write("%s " % v)
            outfile.write("\n")


def io_tuple_list2file(values, ofname, sep=" "):
    """ Simply writes a list vertically or horizontally into a file"""

    with open(ofname, "wb") as outfile:


        for v in values:
            for t in v:
                outfile.write("%s%s" % (t, sep))
            outfile.write("\n")

