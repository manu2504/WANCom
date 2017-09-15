#!/usr/bin/python
import argparse
import logging
import joblib
import os

from pytools.ycsb.ycsb import PARSED_FILE_EXTENSION, load_ycsb_parsed_2_df, \
    convert_df_column_ms2datetime, load_ycsb_raw_2_df, skip_df_head

logging.basicConfig(
    format="(%(funcName).10s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s",
    datefmt='%H:%M:%S', level=logging.DEBUG)


def get_parsed_ycsb_df(src_file_name, is_input_preparsed, is_consider_siblings):
    """ Function returns a parsed df from the ycsb"""

    if is_input_preparsed:
        logging.info("Input set as 'pre-parsed', reading parsed...")
        return load_ycsb_parsed_2_df(src_file_name)

    if is_consider_siblings:
        siblings_name = "%s.%s" % (src_file_name, PARSED_FILE_EXTENSION)
        if os.path.isfile(siblings_name):
            logging.info("Found sibling [%s] reading it as parsed...", siblings_name)
            return load_ycsb_parsed_2_df(siblings_name)

    logging.info("Reading & parsing [%s] ...", src_file_name)
    return load_ycsb_raw_2_df(src_file_name)



def _parse_ycsb_single_file(
    src_file, is_input_preparsed, skip_first_samples_min, is_consider_siblings):

    # <1.> get parsed dataframe
    df = get_parsed_ycsb_df(src_file, is_input_preparsed, is_consider_siblings)


    # <2.> convert timestamp column
    logging.info("Converting timestamp to date time format...[%s]", src_file)
    df = convert_df_column_ms2datetime(df, "timestamp_ms", "datetimestamp")


    # <3.> skip head of the dataframe if needed
    if skip_first_samples_min > 0:
       df = skip_df_head(df, skip_first_samples_min, timestamp_column="datetimestamp")

    return df

def parse_ycsb_file_list(
    file_list, is_input_preparsed, skip_first_samples_min, is_consider_siblings, n_jobs=-1):

    tasks = (
            joblib.delayed(_parse_ycsb_single_file)(
                src_file, is_input_preparsed, skip_first_samples_min, is_consider_siblings)
            for src_file in file_list
        )
    return joblib.Parallel(n_jobs=n_jobs, verbose=50)(tasks)


def get_default_arguments():

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--skip_first_samples_min", default=0, type=int,
        help="Option to skip front samples, that can be associated with warm up time.")

    parser.add_argument("--target_latency_slo_us", default=30000, type=int,
        help="If set, will compute SLO violations per file and add it into the title")

    parser.add_argument('--pre_parsed_input', action='store_true', default=False,
        help="""Indicates that the input files (.ycsb or any other extension) are already pre-parsed
        and can be read directly into a dataframe without additional Raw parsing procedure""")


    parser.add_argument('--consider_siblings',
        help="""If a target file, has a sibling with ".%s" extension, the script will use the
        sibling file and will consider it as it is already parsed. Note, skip_first_samples_min is
        not applied in this case""" % PARSED_FILE_EXTENSION , action='store_true')


    return parser




if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser("""Reads a list of .ycsb files and parses them in accordance
        to the configuration""",
        parents=[ycsb.get_default_arguments()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    FLAGS = parser.parse_args()
    file_list = ycsb.get_source_files(FLAGS, flatten=True)

    parse_ycsb_file_list(
        file_list, FLAGS.pre_parsed_input, FLAGS.skip_first_samples_min, FLAGS.consider_siblings,
        n_jobs=-1)
