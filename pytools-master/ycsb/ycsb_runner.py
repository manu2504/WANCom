#!/usr/bin/python
import argparse
import json
import logging
import os

import pytools.ycsb.ycsb_common as ycsb
import pytools.experiments.exp_common as exp
import pytools.ycsb.ycsb_runner_common as rr
import pytools.experiments.job_generator as jobgen
# from pytools.ycsb.ycsb_results_aggregator import get_ycsb_aggregates
# import pytools.ycsb.ycsb_plot_timeline as ycsb_timeline
# import pytools.ycsb.ycsb_plot_cdfs as ycsb_cdfs

logging.basicConfig(format="(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s", datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger("ycsb_plot_cdfs")


def adjust_by_flags(FLAGS, conf):
    if FLAGS.host:
        conf["workload"]["host"] = FLAGS.host
    return conf

def generate_sub_exp_folder_based_on_args(FLAGS, use_non_single_args_only=True):
    prop_list = []

    if use_non_single_args_only:
        """ Here we ignoring properties that have only 1 field in arg-list, ie they do not
        change between iterative experiments, but were passed on primerily to overwrite
        default config """
        for i, p in enumerate(FLAGS.properties):

            n_args = len(FLAGS.ranges[i].split(","))
            if n_args > 1:
                prop_list.append(p)
    else:
        prop_list = FLAGS.properties

    exp_name = ".".join([x.split(".")[-1] for x in prop_list]) + FLAGS.comment
    exp_name = exp_name.replace("/", ".") # in case we have slashes

    return exp_name

if __name__ == '__main__':

    parser = argparse.ArgumentParser("""Script repeatedly runs YCSB on a given server
        based on the configuration""",
        parents=[jobgen.get_generators_argparser()],
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--out_dir", default="./out")

    parser.add_argument("--host", default="",
        help="Overwrites configuration based dst host")

    parser.add_argument("--do_load", action="store_true",
        help="Set if the data needs to be preloaded prior to first run of the experiment")

    FLAGS = parser.parse_args()

    conf = json.load(FLAGS.cfg_json)
    conf = adjust_by_flags(FLAGS, conf)

    # <1.> Generate custom json dictionary for each individual exp configurations
    json_jobs_list = jobgen.generate_jobs_configs_from_json(
        conf, FLAGS.properties, FLAGS.ranges)

    # <2.> Generate a unique folder for this given experiment based on flags


    exp_name = generate_sub_exp_folder_based_on_args(FLAGS, True)
    print "EXP NAME", exp_name
    exp_folder = exp.setup_experiment_folder(exp_name, FLAGS.out_dir, "run_last")


    # <3.> Create sub folders for each configuration of exp, and dump config.json there
    cmd = ""
    for jj in json_jobs_list:

        sub = jj["job_id"]
        if not jj["job_id"]:
            sub = "base"

        sub_folder = os.path.join(exp_folder, sub.replace("/", "."))
        exp.make_dir(sub_folder)

        with open(os.path.join(sub_folder, "%sconfig.json" % conf["ec2_region_name"]), "w") as jfile:
            jfile.write(json.dumps(jj, indent=4))


        # out_dir = os.path.join(os.getcwd(), FLAGS.out_dir)
        sub_folder = os.path.join(os.getcwd(), sub_folder)

        if FLAGS.do_load:
            rr.load_ycsb_native(jj, sub_folder)

        rr.run_ycsb_multiple_native(jj, sub_folder)

        flags = ycsb.Flags(src_dirs=[sub_folder])

        # ifiles = ycsb.get_source_files(flags, flatten=True)
        # get_ycsb_aggregates(ifiles, sub_folder, "aggregate.csv")

        # ycsb_timeline.plot_ycsb_timelines(ifiles)

        # file_groups = ycsb.get_source_files(flags)
        # ycsb_cdfs.plot_ycsb_cdfs(
        #     file_groups,
        #     os.path.join(sub_folder, "cdfs.png"),
        #     os.path.join(sub_folder, "cdfs.csv")
        # )

# echo "|||| Plotting results ||||"
# cat out.ycsb | grep " R " > actual_timestamps.data

# echo "visualize_ycsb_trace.R --intended_ts_file $TRACE --actual_ts_file actual_timestamps.data --duration 1000 --interval 1"
# visualize_ycsb_trace.R --intended_ts_file $TRACE --actual_ts_file actual_timestamps.data --duration 1000 --interval 1