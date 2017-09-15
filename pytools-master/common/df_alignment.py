#!/usr/bin/python
import logging
import joblib
import psutil
import itertools
import numpy as np
import pandas as pd
import multiprocessing
from datetime import timedelta
from datetime import datetime
from pytools.common.common import get_duplicate_values_in_list

def is_match_by_abs_seconds(dt_stamp1, dt_stamp2, time_margin):
    return abs( (dt_stamp1 - dt_stamp2 ).total_seconds()) <= time_margin

def is_match_by_abs_timedelta(dt_stamp1, dt_stamp2, tdelta):
    return abs(dt_stamp1 - dt_stamp2) <= tdelta

def is_match_by_future_timedelta(dt_stamp1, dt_stamp2, tdelta):
    return (dt_stamp2 >= dt_stamp1) and (dt_stamp2 - dt_stamp1 <= tdelta)

def is_match_by_exact_value(dt_stamp1, dt_stamp2, tdelta):
    return dt_stamp1 == dt_stamp2

# def parallel_get_df_alligment_correlction_nonunique(*args, **kwargs):
def parallel_get_df_alligment_correlction_nonunique(df1, df2, col1, col2, time_margin,
    within_time_range_f, is_mathing_rows_f=None,
    strict_time_order=False, assert_on_duplicates_matches=True):
    """ This is a parallelized version of the alignment function. Basically we subdivide
    df1 into chunks based on the number of available cores, then using quick search we
    look for an appropriate starting point in df2 to begin alignment, and then we
    use multiprocessors to share the load. Note, joblib doesnt work with big dataframes"""

    n = psutil.cpu_count()
    step = int(len(df1) / n)
    intervals = []
    for i in range(0, n):
        if i+1 == n:
            logging.info("%i) %i -> %i", i, i*step, len(df1))
            intervals.append( (i*step, len(df1)) )
        else:
            logging.info("%i) %i -> %i", i, i*step, (i+1)*step)
            intervals.append( (i*step, (i+1)*step) )



    dfs1 = []
    dfs2 = []
    for i in intervals:
        sub_df = df1[ i[0]:i[1] ]
        dfs1.append(sub_df)


        time_offset = type(time_margin)(0) if strict_time_order else time_margin
        ts = sub_df.iloc[0][col1] - time_offset

        # It is possible that df2_starting_index will be the same for several dfs1 this
        # can happen when one of the dfs has a lot of samples that not appearing in
        # another one at all, this should not be considered a problem
        df2_starting_index = find_starting_index(ts, df2, col2)
        dfs2.append(df2[df2_starting_index:])



    pool = multiprocessing.Pool(processes=n)
    result = pool.map(get_df_alligment_correlction_nonunique_wrapper,
        itertools.izip(
            dfs1,
            dfs2,
            itertools.repeat(col1),
            itertools.repeat(col2),
            itertools.repeat(time_margin),
            itertools.repeat(within_time_range_f),
            itertools.repeat(is_mathing_rows_f),
            itertools.repeat(strict_time_order),
            itertools.repeat(assert_on_duplicates_matches)
            )
        )

    pool.join()
    pool.close()


    # list of lists of tuples into 1D list
    return [item for sublist in result for item in sublist]



def find_starting_index(ts, df2, col2):
    """ This function is an implementation of the quick search, we want to find an index
    in df2, such that within time margin from timestamp ts. Each step we divide the range
    in two and step closer to the target timestamp. Function will guarantee to return a
    timestamp that is earlier than ts, or at most smallest possible index of df2"""

    left_index = df2.index[0]
    right_index = df2.index[-1]
    mid_index = -1

    # An index that is guaranteed to be earlier than our possible deadline, returned
    # at the end of the searching no matter what.
    best_earliers_index = left_index

    max_attempts = 32
    for i in range(0, max_attempts):
        # Compute new mid point, if the new point is the same as before, then we already
        # found the best possible index we could, break the loop and return it
        new_mid_index = int( left_index + (right_index - left_index) // 2)
        if new_mid_index == mid_index:
            break
        else:
            mid_index = new_mid_index

        # print "Indexes: [%i %i] trying index [%i] times [%s %s] delta [%.2f]" % (
        # left_index, right_index, mid_index, ts, df2.ix[mid_index, col2],
        #     abs((ts - df2.ix[mid_index, col2]).total_seconds()) )

        if df2.ix[mid_index, col2] < ts:
            # Our found index is too far in the past move left border
            left_index = mid_index
            best_earliers_index = left_index
        elif df2.ix[mid_index, col2] >= ts:
            # we are too far into the future, adjust right index
            #
            # When timestamps converted from nanoseconds to datetime, they are stored with
            # microsecond precision, thus it is possible to get the same timestamp here
            # however, it is very unlikely that nanosecond timestamps are also equal.
            # To be on the safe side we consider identialc timestamps case to the case
            # being in the future and looking backwards
            right_index = mid_index

            if df2.ix[mid_index, col2] == ts and \
                (type(ts) == timedelta or type(ts) == pd.tslib.Timestamp):
                logging.warning("Exactly the same datetime timestamps [%s %s] at "
                    "indx [%i]. Potentially lost precision due to conversion from ns"
                    " to micros",
                    df2.ix[mid_index, col2],  ts, mid_index
                    )

    if type(ts) == timedelta or type(ts) == pd.tslib.Timestamp:
        delta = abs((ts - df2.ix[best_earliers_index, col2]).total_seconds())
    else:
        delta = abs(ts - df2.ix[best_earliers_index, col2])
    logging.info("FINAL left df range[%i %i] right df range[%i %i] times [%s %s] delta [%s] attempts [%i]",
        left_index, right_index,
        best_earliers_index, len(df2),
        ts, df2.ix[best_earliers_index, col2],
        delta, i)

    return best_earliers_index


def get_df_alligment_correlction_nonunique_wrapper(args):
    return get_df_alligment_correlction_nonunique(*args)

def get_df_alligment_correlction_nonunique(df1, df2, col1, col2, time_margin,
    within_time_range_f, is_mathing_rows_f=None,
    strict_time_order=False, assert_on_duplicates_matches=True):
    """ Functions matches rows in 2 dataframes. col1 and col2 are the names of the
    timestamp columns that are used for matching and time margin is the the delta time
    (i.e., range) in which two timestamps considered to be equal (i.e., match). Format of
    the timestamp and the units of the time_margin can be anything and depends on the
    within_time_range_f function pointer.

    -within_time_range_f compares timestamps in two rows based on the time_margin and
    returns true if two rows considered to be in time range (close enough). See sample
    functions defined above this one.

    -is_mathing_rows_f can be supplied, it takes 1 raw from each DF and returns true if
    these rows match based on some additional criteria. For example it could be an
    id column that has to match or the key column etc. If no is_mathing_rows_f is passed,
    then only timestamps will be used for matching.

    -strict_time_order defines the ends of the window in the second df of where we are
    looking for the matched values. If set to true, then the next row that we going to
    pick up from df2 will be strictly in the future. If false, then the next row in df2
    can be as far back in the past as time_margin. Note, if the within_time_range_f
    function is strictly looks for the future based matches (i.e., does not uses abs() )
    then there is no point to set strict_time_order=False, as it will have no effect but
    will only slow down the performance as we have to iterate over longer window to find
    matches.

    -assert_on_duplicates_matches tells us if we want to stop execution when duplicate
    matches found. If we are ok to take the risk, there is a function below to remove
    duplicates, you should never use duplicate entries, they are most certainly wrong!

    Assumptions: indexes are uniformly increasing in both input data frames.
    """
    index1 = df1.index[0]
    index2 = df2.index[0]
    index1_max = df1.index[-1] + 1
    index2_max = df2.index[-1] + 1
    logging.info("Start alignment from indexes:[%i %i] to indexes:[%i %i]",
        index1, index2, index1_max, index2_max)

    # if type(time_margin) == datetime.timedelta:

    matching_pairs = []
    while index1 < index1_max and index2 < index2_max:
        found = False
        row1 = df1.ix[index1]
        row2 = df2.ix[index2]

        # <1.> Adjust index2 until it is in the future of index1
        time_offset = type(time_margin)(0) if strict_time_order else time_margin

        if row1[col1] - time_offset > row2[col2]:
            index2 += 1
            continue

        # # <1.a> Check: at this stage two rows of two dfs _must_ be within time range
        # assert within_time_range_f(row1[col1], row2[col2], time_margin), \
        #     "strict_time_order option does not match within_time_range_f! [%i %i]" % (
        #         index1, index2)

        # <2.> Look in the window from index2 find matching row within acceptable range
        window_index2 = index2

        # logging.info("Compare indexes [%i, %i] times[%s %s] in range[%i] match[%i]",
        #     index1, window_index2,
        #     row1[col1], df2.ix[window_index2][col2],
        #     within_time_range_f(
        #         row1[col1], df2.ix[window_index2][col2], time_margin),
        #     is_mathing_rows_f(row1, df2.ix[window_index2]),
        #     )

        # First condition is just to make sure we won't get into index overflow
        while window_index2 < index2_max and \
            within_time_range_f(row1[col1], df2.ix[window_index2][col2], time_margin):

            # logging.info("Sub-com indexes [%i, %i] keys[%s == %s][%i]",
            #     index1, window_index2,
            #     row1.key, df2.ix[window_index2].key,
            #     is_mathing_rows_f(df2.ix[window_index2], row1))

            if is_mathing_rows_f == None or \
               is_mathing_rows_f(row1, df2.ix[window_index2]):

                # Here we found two corresponding rows in two dataframes that both within
                # our time margin and match by IDs
                matching_pairs.append( (index1, window_index2) )
                # logging.info("Matched indexes %i [%i %i]",
                #     len(matching_pairs), index1, window_index2)
                found = True
                break
            else:
                window_index2 += 1

        if not found:
            logging.debug("Not Found match for left column index [%i] ts [%s] ",
                index1, row1[col1])
        index1 += 1

    # We are done, do validation and return
    # We can get duplicates if for example, two incoming requests are close by and
    # next stage time stamp can be accounted for either of them. You can assert on this
    # or remove duplicates, otherwise there is no guarantee if we did a correct match.
    # Try to keep the number of duplicates at near zero if possible.
    if not verify_no_duplicate_matches(df1, df2, matching_pairs):
        logging.warning("Duplicate row matches found! Perhaps adjust time margin!")
        assert not assert_on_duplicates_matches

    return matching_pairs


def verify_no_duplicate_matches(df1, df2, matching_pairs):

    duplicate_found = False
    for z in get_duplicate_values_in_list([x[0] for x in matching_pairs]):
        duplicate_found =True
        for mp in matching_pairs:
            if mp[0] == z:
                print "MP-0 ", mp, df1.ix[mp[0]].datetime, df2.ix[mp[1]].datetime
                print df1.ix[mp[0]]
                print df2.ix[mp[1]]
                print "-------------------------"

    for z in get_duplicate_values_in_list([x[1] for x in matching_pairs]):
        duplicate_found =True
        for mp in matching_pairs:
            if mp[1] == z:
                print "MP-1 ", mp, df1.ix[mp[0]].datetime, df2.ix[mp[1]].datetime
                print df1.ix[mp[0]]
                print df2.ix[mp[1]]
                print "-------------------------"

    return not duplicate_found

def remove_duplicates_if_only_few(matching_pairs, accepted_fraction=0.001):
    dup0 = get_duplicate_values_in_list([x[0] for x in matching_pairs])
    dup1 = get_duplicate_values_in_list([x[1] for x in matching_pairs])

    assert (len(dup0) + len(dup1)) <= accepted_fraction * len(matching_pairs), \
        "Too many duplicate entries! Unacceptable precision %i < %i total %i " % (
            (len(dup0) + len(dup1)), accepted_fraction * len(matching_pairs), len(matching_pairs))

    allowed_matches = []

    for mp in matching_pairs:
        if mp[0] not in dup0 and mp[1] not in dup1:
            allowed_matches.append(mp)

    return allowed_matches


