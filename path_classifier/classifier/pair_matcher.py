#!/usr/bin/python

import logging
import time
import config as conf
import numpy as np

import dao as dao

from common import *

dm = dao.dm

log = conf.get_logger("matcher", conf.log_matcher)


def is_ppair_match(p1, p2):

    delta_ns = 0
    if p1.timestamp_ns > p2.timestamp_ns:
        delta_ns = p1.timestamp_ns - p2.timestamp_ns
    else:
        delta_ns = p2.timestamp_ns - p1.timestamp_ns

    delta_ms = delta_ns // 1000 // 1000

    # print "PAIR1-2",  p1.timestamp, p2.timestamp,  type(delta_ns),
    # (np.uint64)(delta_ms)

    # NOTE: If we do match by time, we should make sure that there are no more than 2
    # samples that could possibly be matched. Otherwise can have a chance of having
    # different pairings based on the processing order on different hosts
    if delta_ms < conf.pasm["path_pair_threshold_ms"]:
        return True


    # if delta_ms < 10000:
    #     log.debug("[PAIRS] %s %s %i %i",
    # p1, p2, delta_ms, delta_ms < conf.pasm["path_pair_threshold_ms"])


def get_timeout_measurements(msrmnts_list):
    """
    We iterate over list of Measurements to see if their creation time
    (when the probes have been sent out) is older than a limit.
    """
    ret_ids = []

    time_now_ms = (np.uint64)(time.time() * 1000)

    for i, m in enumerate(msrmnts_list):
        start_time_ms = m.timestamp_ns // 1000 // 1000
        if time_now_ms - start_time_ms > conf.pasm["old_measurement_threshold_ms"]:
            log.debug("Timedout NPC      [pid: %i]  [%s->%s]", m.idPath,
                dm.pdm.getElementById(m.idPath).hops[0],
                dm.pdm.getElementById(m.idPath).hops[-1])
            ret_ids.append(i)


    return ret_ids


def move_timedout_paths2_combuf(msrmnts_list, measurements_commit_buffer):

    timedout_msrmnts = get_timeout_measurements(msrmnts_list)
    for iid in timedout_msrmnts:
        measurements_commit_buffer.append(msrmnts_list[iid])

    delete_indexes_from_list(msrmnts_list, timedout_msrmnts)

def move_paired_msrmnts2_combuf(frwd_msrmnts_list, rvrs_msrmnts_list,
    matched_pairs_indexes, measurements_commit_buffer):

    # Before deleting from unmatched list, save paths in commit buffer
    for iid in matched_pairs_indexes[0]:
        measurements_commit_buffer.append(frwd_msrmnts_list[iid])

    # for iid in matched_pairs_indexes[1]:
    #     measurements_commit_buffer.append(rvrs_msrmnts_list[iid])

    # we need to remove fp and rp from the list of unmatched instances.
    delete_indexes_from_list(frwd_msrmnts_list, matched_pairs_indexes[0])
    delete_indexes_from_list(rvrs_msrmnts_list, matched_pairs_indexes[1])


def match_pathpairs_from_lists(frwd_msrmnts_list, rvrs_msrmnts_list):

    matched_pairs_indexes = ([], []) # fm_index, rm_index

    for fm_index, frwd_ms in enumerate(frwd_msrmnts_list):
        for rm_index, rvrs_ms in enumerate(rvrs_msrmnts_list):

            if is_ppair_match(frwd_ms, rvrs_ms):
                # remember which fp/rp indexes made a pair
                matched_pairs_indexes[0].append(fm_index)
                matched_pairs_indexes[1].append(rm_index)
                frwd_ms.pair_timestamp = rvrs_ms.timestamp_ns
                rvrs_ms.pair_timestamp = frwd_ms.timestamp_ns
                log.debug("Pair matched pids: [%3i, %3i]  [%15s->%15s]+[%15s->%15s]", frwd_ms.idPath, rvrs_ms.idPath,
                    dm.pdm.getElementById(frwd_ms.idPath).hops[0],
                    dm.pdm.getElementById(frwd_ms.idPath).hops[-1],
                    dm.pdm.getElementById(rvrs_ms.idPath).hops[0],
                    dm.pdm.getElementById(rvrs_ms.idPath).hops[-1])
    return matched_pairs_indexes

def match_pairs(
    unmatched_frwd_msrmnt_dic, unmatched_rvrs_msrmnt_dic, measurements_commit_buffer):
    """
    Two input dictionaries are dst based measurements objects (looking from our direction)
    Thus, path pairs should come from the same dst keys in 2 lists.
    Matched paths are moved from unmatched lists into the commit list
    Paths that couldn't be matched for timeout time also moved into commit list
    (to be committed without a pair)
    """

    # Iterate over all FP that we have and try to match them to the corresponding RP
    for dst_ip, frwd_msrmnts_list in unmatched_frwd_msrmnt_dic.iteritems():

        if dst_ip in unmatched_rvrs_msrmnt_dic:

            matched_pairs_indexes = match_pathpairs_from_lists(
                frwd_msrmnts_list, unmatched_rvrs_msrmnt_dic[dst_ip])

            move_paired_msrmnts2_combuf(
                frwd_msrmnts_list, unmatched_rvrs_msrmnt_dic[dst_ip],
                matched_pairs_indexes, measurements_commit_buffer)

        # Check remaining paths, for being too old to be in this list
        move_timedout_paths2_combuf(frwd_msrmnts_list, measurements_commit_buffer)

        if dst_ip in unmatched_rvrs_msrmnt_dic:
            move_timedout_paths2_combuf(
                unmatched_rvrs_msrmnt_dic[dst_ip], [])

