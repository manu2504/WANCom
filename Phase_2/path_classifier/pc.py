#!/usr/bin/python
import argparse

import logging
import time


import collectors.api as collectors

from common import merge_dics_of_lists, dump_path_dic
import intracom.intracom as icom
import config as conf
from classifier.pair_matcher import  match_pairs

import dbapi as db


logging.basicConfig(datefmt='%H:%M:%S')

log = conf.get_logger("main", conf.log_main_loop)

unmatched_frwd_msrmnt_dic = {}
unmatched_rvrs_msrmnt_dic = {}

# List of NetworkPathContainers that represent measurements.
# All pids should be set, and matched pairs are set (if found)
measurements_commit_buffer = []

hop_measurements_commit_buffer = []

new_hop_measurements_list = []


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Path Classifier for Tectonic")

    parser.add_argument("--src_files", nargs='*', default=[], help="list of files to process")
    FLAGS = parser.parse_args()


    db.inti_db()

    collectors.init()

    icom.init_intra_sock()

    # for p in  dm.getPaths():
    #     print p["hops"]
    # exit(0)
    while True:

        # <1.> Assemble/process forward measurements
        frwdPaths_and_hopMeasurements = collectors.get_new_path_traces()
        new_frwd_nps_dic = frwdPaths_and_hopMeasurements[0]

        new_hop_measurements_list = new_hop_measurements_list + frwdPaths_and_hopMeasurements[1]

        new_frwd_msrmnt_dic = db.assimilate_paths(new_frwd_nps_dic, commit2db=True)

        unmatched_frwd_msrmnt_dic = merge_dics_of_lists(
            unmatched_frwd_msrmnt_dic, new_frwd_msrmnt_dic)


        # <2.> Send out our forward measurements
        icom.distribute_our_fward_paths(new_frwd_nps_dic)


        # <3.> Assemble/process reverse measurements
        new_rvrs_paths_dic = icom.recv_reverse_traces()

        new_rvrs_msrmnt_dic = db.assimilate_paths(new_rvrs_paths_dic, commit2db=False)

        unmatched_rvrs_msrmnt_dic = merge_dics_of_lists(
            unmatched_rvrs_msrmnt_dic, new_rvrs_msrmnt_dic)



        match_pairs(unmatched_frwd_msrmnt_dic, unmatched_rvrs_msrmnt_dic, measurements_commit_buffer)

        db.batchcommit_measurements((measurements_commit_buffer,new_hop_measurements_list))

        time.sleep(2)


        # ##########################################
        # for dst in AllDsts

        #     p = get_current_frwd_path_towards(dst)

        #     pclass = get_path_class4path(p)

        #     base_lat = get_base_latency4pclass(pclass)

        #     #################

        #     (m1, m2) = get_latest_measurement_pair_towards(dst)

        #     p1, p2 = get_path_ids(m1, m2)

        #     get_path_pair_class(p1, p2)








        #     print base_lat,




    print "Exit"
