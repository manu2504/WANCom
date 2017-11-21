#!/usr/bin/python
import pandas as pd
import numpy as np
import logging
import subprocess
import time
import os
import psutil
import random
import itertools
import multiprocessing
import copy
from pytools.common.common import remove_repeated_spaces
from pytools.ycsb.parsing.parse_ycsb_file import cpp_parse_ycsb_file
from pytools.ycsb.ycsb_common import YCSB_MASK, PARSED_FILE_EXTENSION, PARSING_VALID_PREFIXES, \
    DEFAULT_YCSB_COLUMNS


random.seed(time.time())
def verify_token_read(tokens, column_order, dtypes_dic, allowed_strings=["READ", "RawREAD"]):
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
                if v not in allowed_strings:
                    raise RuntimeError("Not allowed string [%s]", v)
            else:
                assert False, "Cannot verify column data type [%s]" % column

        res.append(v)
    except:
        # print tokens, res
        return False

    return True


def raw_reparse_singular(lines, column_order, dtypes, verify_function, separator=","):
    """ This function attempts to deal with all sort of issues, occured due to parallel
    unsyncrhonized write to a single file, ie., we can have something like:
    5 49178 8 1490978084662906109 252
    5532796 32819 88 14909780846629834721 241
    58
    5 49166 8 1490978084663144067 264"""

    print "Processing [%d lines]" % len(lines)

    removed_lines = []
    saved_lines = []

    for line in lines:
        tokens = remove_repeated_spaces(line).rstrip().split(separator)
        if len(tokens) == len(dtypes) \
           and verify_function(tokens, column_order, dtypes):

            saved_lines.append(remove_repeated_spaces(line))
        else:
            removed_lines.append(line)

    logging.info("Number of corrupted lines found [%i]", len(removed_lines))
    # for l in removed_lines:
    #     logging.info("Corrupted line removed [%s]", l.rstrip())

    return saved_lines


def raw_reparse_singular_wrapper(args):
    return raw_reparse_singular(*args)

def raw_reparse(ifile, ofile, column_order, dtypes, verify_function, separator=","):
    """ This function attempts to deal with all sort of issues, occured due to parallel
    unsyncrhonized write to a single file, ie., we can have something like:
    5 49178 8 1490978084662906109 252
    5532796 32819 88 14909780846629834721 241
    58
    5 49166 8 1490978084663144067 264"""

    removed_lines = []
    with open(ifile) as f:
        content = f.readlines()

    n = psutil.cpu_count()
    step = int(len(content) / n)
    intervals = []
    for i in range(0, n):
        if i+1 == n:
            logging.info("%i) %i -> %i", i, i*step, len(content))
            intervals.append( (i*step, len(content)) )
        else:
            logging.info("%i) %i -> %i", i, i*step, (i+1)*step)
            intervals.append( (i*step, (i+1)*step) )


    print "STEPS ", intervals

    subs = []
    for i in intervals:
        subs.append(copy.deepcopy(content[ i[0] : i[1] ]))

    # with open(ofile, "w") as of:
    #     for line in content:
    #         tokens = remove_repeated_spaces(line).rstrip().split(separator)
    #         if len(tokens) == len(dtypes) \
    #            and verify_function(tokens, column_order, dtypes):

    #             of.write(remove_repeated_spaces(line)+"\n")
    #         else:
    #             removed_lines.append(line)

    # logging.info("Number of corrupted lines found [%i]", len(removed_lines))
    # # for l in removed_lines:
    # #     logging.info("Corrupted line removed [%s]", l.rstrip())
# column_order, dtypes, verify_function, separator=","

    pool = multiprocessing.Pool(processes=n)
    results = pool.map(raw_reparse_singular_wrapper,
        itertools.izip(
            subs,
            itertools.repeat(column_order),
            itertools.repeat(dtypes),
            itertools.repeat(verify_function),
            itertools.repeat(separator)
            )
        )

    pool.close()
    pool.join()


    with open(ofile, "w") as of:
        for r in results:
            print "Results length [%d]" % len(r)
            for l in r:
                of.write("%s\n"%l)



def load_ycsb_raw_2ts(ycsb_file, nrows2read=None):
    assert False, "Deprecated use load_ycsb_raw_2_ts"
    # logging.info("Loading raw [%s]", ycsb_file)


    # tmp_ycsb = "%s.%s" % (ycsb_file, parallel_fast_parse)
    # raw_reparse(ycsb_file, tmp_ycsb,
    #     column_order=["opcode", "timestamp", "latency_us"],
    #     dtypes={ "opcode":str, "timestamp":np.uint64, "latency_us":np.uint32},
    #     verify_function=verify_token_read
    #     )

    # print "LOADING from ", tmp_ycsb
    # return l_load_ycsb_raw_2ts(tmp_ycsb, nrows2read)


def l_load_ycsb_raw_2ts(ycsb_file, nrows2read=None):
    assert False, "Deprecated use load_ycsb_raw_2_df/ts"

    # logging.error("FUNCTION l_load_ycsb_raw_2ts is deprecated. use load_ycsb_raw_2_ts instead!")
    # df = pd.read_csv(ycsb_file, sep=",", names=["opcode", "time", "latency"],
    #     usecols=["opcode", "time", "latency"], error_bad_lines=False, nrows=nrows2read)
    # logging.info("Read values %s" % (len(df)))
    # # Removing all junk columns
    # df1 = df[df["opcode"] == "READ"]
    # df2 = df[df["opcode"] == "RawREAD"]

    # if len(df1) > len(df2):
    #     df = df1
    # else:
    #     df = df2


    # logging.info("After filtering %s" % (len(df)))

    # df["latency"] = df["latency"].astype(np.uint64)
    # df["time"] = df["time"].astype(np.float64) * 1000.0 * 1000
    # df['time'] = pd.to_datetime(df['time'])

    # logging.info("Converting dataframe to pd.Series...")
    # return pd.Series(np.asarray(df["latency"]), index=df["time"])


def convert_df_column_ms2datetime(df, src_column_ms="timestamp_ms", dst_column="datetimestamp"):
    """ Function takes a dataframe, then takes src_column and create dst_column that contains
    datetime timestamp """

    df[dst_column] = df[src_column_ms] * 1000.0 * 1000
    df[dst_column] = pd.to_datetime(df[dst_column])

    return df

def bash_filter_pattern(
    ifile, tmp_folder="/tmp/", allowed_patterns=["READ"], excluded_patterns=["Intended"]):

    tmp_file = "%s.%d" % (os.path.basename(ifile), random.randint(0,10000))
    tmp_file = os.path.join(tmp_folder, tmp_file)

    grep_string = '| grep -E "'
    for pattern in allowed_patterns:
        grep_string = "%s%s|" % (grep_string, pattern)
    grep_string = grep_string[:-1]
    grep_string += '"'


    exclude_string = ""
    if excluded_patterns:
        exclude_string = '| grep -v "'
        for pattern in excluded_patterns:
            exclude_string = "%s%s|" % (exclude_string, pattern)
        exclude_string = exclude_string[:-1]
        exclude_string += '"'


    cmd = "cat {ifile} {grep} {exclude} > {tmp_file}".format(
        ifile=ifile, grep=grep_string, tmp_file=tmp_file, exclude=exclude_string)

    logging.info("Executing [%s]", cmd)

    subprocess.check_call(cmd, shell=True)

    logging.info("Bash filter complete")

    return tmp_file




####################################################################################################
## YCSB --> TO DATAFRAMES
####################################################################################################
# RAW
def load_ycsb_raw_2_df(ycsb_file, columns=DEFAULT_YCSB_COLUMNS, nrows2read=None):
    """This function parses out """
    out_file_name = "%s.%s" % (ycsb_file, PARSED_FILE_EXTENSION)

    cpp_parse_ycsb_file(
        ycsb_file, out_file_name,
        valid_prefixes=PARSING_VALID_PREFIXES)

    df = load_ycsb_parsed_2_df(out_file_name, columns, nrows2read)

    return df

# PARSED
def load_ycsb_parsed_2_df(
    parsed_ycsb_file, columns=DEFAULT_YCSB_COLUMNS, nrows2read=None):
    """ Reads parsed YCSB file of the format
    ...
    READ,1503069594211,1919843
    READ,1503069594211,1844322
    READ,1503069594211,1844352
    ...
    """
    df = pd.read_csv(parsed_ycsb_file,
        names=columns,
        dtype={"opcode":str, "timestamp_ms":np.uint64, "latency_us":np.uint64},
        usecols=[0,1,2],
        nrows=nrows2read)
    return df

# SKIP FRONT HEAD
def skip_df_head(df, skip_first_mins=1, timestamp_column="timestamp"):
    """ Function takes a dataframe and a column that is converted to a datetime format, based on
    this column initial samples are skipped """

    starting_period =  pd.Period(df[timestamp_column][0], "S")

    offset_period = starting_period + 60 * skip_first_mins

    logging.info("DF start %s, offset to %s",
        df[timestamp_column][0],  offset_period)

    shortened_df = df[df[timestamp_column] > offset_period.to_timestamp()]

    logging.info("First %s minutes was skipped, Total length reduction %s %s prcnt",
        skip_first_mins,
        len(df)-len(shortened_df),
        (len(df)-len(shortened_df)) / (len(df)/100)
    )

    return shortened_df

####################################################################################################
## YCSB --> TO TIME SERIES
####################################################################################################
# RAW
def load_ycsb_raw_2_ts(ycsb_file, nrows2read=None):
    """This function parses out """
    out_file_name = "%s.%s" % (ycsb_file, PARSED_FILE_EXTENSION)

    cpp_parse_ycsb_file(
        ycsb_file, out_file_name,
        valid_prefixes=["READ", "UPDATE", "RawREAD", "RawUPDATE"])

    ts = load_ycsb_parsed_2_ts(out_file_name, DEFAULT_YCSB_COLUMNS, nrows2read)

    return ts

# PARSED
def load_ycsb_parsed_2_ts(parsed_ycsb_file, columns=DEFAULT_YCSB_COLUMNS, nrows2read=None):

    df = load_ycsb_parsed_2_df(parsed_ycsb_file, columns, nrows2read)

    df = convert_df_column_ms2datetime(df)

    # ts = pd.Series(np.asarray(df["latency_us"]), index=df["datetimestamp"])
    ts = convert_parsed_df_to_ts(df)

    return ts


def convert_parsed_df_to_ts(df, latency_column="latency_us", timestamp_column="datetimestamp"):

    return pd.Series(np.asarray(df[latency_column]), index=df[timestamp_column])

# SKIP FRONT HEAD
def skip_ts_head(ts, skip_first_mins=1):

    starting_period = pd.Period(ts.index[0], "S")

    offset_period = starting_period + 60 * skip_first_mins

    logging.info("TS start %s, ts end %s, offset to %s",
        ts.index[0], ts.index[-1], offset_period)

    shortened_ts = ts[offset_period.to_timestamp():]

    logging.info("First %s minutes was skipped, Total length reduction %s %s prcnt",
        skip_first_mins,
        len(ts)-len(shortened_ts),
        (len(ts)-len(shortened_ts)) / (len(ts)/100)
    )

    assert len(shortened_ts)>0, "Too few samples!"

    return shortened_ts







