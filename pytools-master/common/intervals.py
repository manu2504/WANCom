#!/usr/bin/python
import fnmatch
import numpy as np


def get_all_intervals_from_list(vals_list):
    intervals = []

    for i in range(1, len(vals_list)):
        val = vals_list[i] - vals_list[i-1]
        intervals.append(val)

    return intervals


def get_intervals_from_list(vals, sep_threshold_ms):
    '''Assume you have a list of timestamps. You want to detect intervals when timestamps
    spaced close to each other and intervals when they are separated by some delta time.
    '''

    # sep_threshold_ms = sep_threshold_ms
    sep_threshold_ns = (np.uint64)(sep_threshold_ms * 1000 * 1000)
    # print vals

    vals = np.asarray(vals, np.uint64)

    # list of tuples, indicating the time and the duration of continuous intervals of
    # under threshold duration (usually many small ones inside) or over (a big chunk of
    # time inbetween many small timestamps)
    under_threshold_ints = []
    over_threshold_ints = []

    current_under_int_start_time = 0

    t_last = vals[0]
    for i in range(1, len(vals)):
        t_now = vals[i]

        t_delta = (np.uint64)(t_now - t_last)


        if (t_delta < sep_threshold_ns):
            # we have a small leap since the last sample. So we either start counting a
            # new under_interval or extend an existing.

            if current_under_int_start_time == 0:
                current_under_int_start_time = t_last
            else:
                #nothing to do here, we still within the same time interval
                pass

        else: # (t_delta > sep_threshold_ns)
            # we found an interval that lasted longer than threshold, this means that
            # the previous under_interval actually finished at the t_last. and a new
            # over interval begun and consequently got finished here.

            if current_under_int_start_time > 0:
                under_threshold_ints.append(
                    (current_under_int_start_time, t_last - current_under_int_start_time)
                    )
                current_under_int_start_time = 0

            assert t_delta == t_now - t_last
            assert t_now - t_last >= sep_threshold_ns
            over_threshold_ints.append( (t_last, t_now-t_last) )

        t_last = vals[i]

    return under_threshold_ints, over_threshold_ints, get_all_intervals_from_list(vals)


