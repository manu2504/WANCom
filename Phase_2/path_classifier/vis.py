#!/usr/bin/python

import argparse
import logging

from datavis.datafactory import *
from datavis.plotter import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Data Visualizer for Tectonic")

    parser.add_argument("--out_dir", type=str, default="./out",
        help="The output location for produced files")

    parser.add_argument("--plot_tracedir_rtt", action="store_true",
        help="""For each trace direction in the src database, produces a single plot
        containing all latency (RTT) measurements. No separation by forward path""")

    parser.add_argument("--plot_smoothed_tracedir_rtt", action="store_true",
        help="""For each trace direction in the src database, produces a single plot
        containing all latency (RTT) measurements. No separation by forward path""")

    parser.add_argument("--plot_path_pairs_boxes", nargs='*', default=[],
        help="""Plot path pairs boxplots, args[topklim, bidirectional(True/False)
        example 30 True""")

    parser.add_argument("--plot_smoothed_path_pairs_boxes", nargs='*', default=[],
        help="""Plot path pairs boxplots, args[topklim, bidirectional(True/False)
        example 30 True""")

    parser.add_argument("--plot_all_path_pairs_boxes", nargs='*', default=[],
        help="""Plot path pairs boxplots, args[topklim, bidirectional(True/False)
        example 30 True""")

    parser.add_argument("--plot_path_pairs_hist", nargs='*', default=[],
        help="""Plot path pairs measurements histogram for pairs of path ids ,
        args[frwrd_pid-1, rvrs_pid-1, frwrd_pid-2, rvrs_pid-2]
        example 20 30""")

    parser.add_argument("--plot_path_pairs_timeline", nargs='*', default=[],
        help="""Same as plot_tracedir_rtt but at the precision of a single path pair,
        args[frwrd_pid-1, rvrs_pid-1, frwrd_pid-2, rvrs_pid-2]
        example 20 30""")

    parser.add_argument("--rtt_timeline_hop_after_stars", nargs='*', default=[],
        help="""Same as plot_tracedir_rtt but at the precision of a single path pair and only for hops after the star,
        args[frwrd_pid-1, rvrs_pid-1, frwrd_pid-2, rvrs_pid-2]
        example 20 30""")

    parser.add_argument("--plot_smoothed_path_pairs_timeline", nargs='*', default=[],
        help="""Same as plot_tracedir_rtt but at the precision of a single path pair,
        args[frwrd_pid-1, rvrs_pid-1, frwrd_pid-2, rvrs_pid-2]
        example 20 30""")

    parser.add_argument("--plot_path_pairs_timeline_top", nargs='*', default=[],
        help="""See plot_path_pairs_timeline, plots topK most popular path pairs.""")

    parser.add_argument("--plot_total_unique_paths_cdf", action="store_true",
        help="""Creates a CDF plot, where each point corresponds to the total number
        unique paths found in each trace direction""")

    parser.add_argument("--plot_new_paths_frequencies", action="store_true",
        help="""Shows the frequency of observing new paths on each trace direction""")

    parser.add_argument("--plot_paths_stability", action="store_true",
        help="""Shows the average time spent by network paths that lasted for certain perioud""")

    parser.add_argument("--plot_paths_prevalance", action="store_true",
        help="""Shows the percentage of time spent by the most prevalant paths""")

    parser.add_argument("--plot_paths_lifetime", action="store_true",
        help="""Shows the average time spent by network paths that lasted for certain perioud""")


    FLAGS = parser.parse_args()

    from dao import *

    # print_unituq_paths4tracedir(dm, 1)
    # plot_path_persistance_cdf(dm)
    # print_unituq_paths4tracedir(dm, 0)

    if FLAGS.plot_tracedir_rtt:

        plot_tuples = generateRttVsTimeData(dm)

        plot_tracedir_rtt(plot_tuples, out_dir=FLAGS.out_dir)

    if FLAGS.plot_smoothed_tracedir_rtt:
        plot_tuples = generateSmoothedRttVsTimeData(dm)
        plot_tracedir_rtt(plot_tuples, out_dir=FLAGS.out_dir)


    if len(FLAGS.plot_path_pairs_boxes):

        r = getPathPairs(dm)

        # TODO: dump in readable form

        plot_path_pairs(
            r,
            topklim=int(FLAGS.plot_path_pairs_boxes[0]),
            show=False,
            bidirectional=FLAGS.plot_path_pairs_boxes[1],
            out_dir=FLAGS.out_dir
            )


    if len(FLAGS.plot_smoothed_path_pairs_boxes):

        r = getSmoothedPathPairs(dm)

        # TODO: dump in readable form

        plot_path_pairs(
            r,
            topklim=int(FLAGS.plot_smoothed_path_pairs_boxes[0]),
            show=False,
            bidirectional=FLAGS.plot_smoothed_path_pairs_boxes[1],
            out_dir=FLAGS.out_dir
            )


    if len(FLAGS.plot_all_path_pairs_boxes):

        #r = getAllPathPairsNormalized(dm)

        # TODO: dump in readable form

        #plot_all_path_pairs_normalized(
        #    r,
        #    topklim=int(FLAGS.plot_all_path_pairs_boxes[0]),
        #    show=False,
        #    bidirectional=FLAGS.plot_all_path_pairs_boxes[1],
        #    out_dir=FLAGS.out_dir
        #    )
        r = getAllPathPairsNormalized(dm)
        plot_all_path_pairs_normalized_cdf(r,out_dir=FLAGS.out_dir)


    if len(FLAGS.plot_path_pairs_hist):
        logging.info("plot_path_pairs_hist: pids: %s", FLAGS.plot_path_pairs_hist)

        r = getPathPairs(dm)

        for i in range(0, len(FLAGS.plot_path_pairs_hist), 2):
            target_path_pair_ids = (
                int(FLAGS.plot_path_pairs_hist[i]),
                int(FLAGS.plot_path_pairs_hist[i+1])
                )
            out_legend_buf = path_pair_ids2legend_names(dm, target_path_pair_ids)

            path = dm.pdm.pid2Path[target_path_pair_ids[0]]
            tdid = path.idTraceDirection

            plot_name=path2plot_name(dm, dm.pdm.pid2Path[target_path_pair_ids[0]])

            plot_path_pair_msrmnts_histogram(
                r,
                tdid=tdid,
                plot_name=plot_name,
                target_ppair_ids = target_path_pair_ids,
                out_legend_buf=out_legend_buf,
                out_dir=FLAGS.out_dir
                )

    if len(FLAGS.plot_path_pairs_timeline):
        logging.info("plot_path_pairs_timeline: pids: %s", FLAGS.plot_path_pairs_timeline)

        r = getPathPairs(dm)

        for i in range(0, len(FLAGS.plot_path_pairs_timeline), 2):
            target_path_pair_ids = (
                int(FLAGS.plot_path_pairs_timeline[i]),
                int(FLAGS.plot_path_pairs_timeline[i+1])
                )


            plot_path_pair_msrmnts_timeline(
                dm,
                r,
                target_ppair_ids = target_path_pair_ids,
                out_dir=FLAGS.out_dir
                )

    if len(FLAGS.plot_smoothed_path_pairs_timeline):
        logging.info("plot_smoothed_path_pairs_timeline: pids: %s", FLAGS.plot_smoothed_path_pairs_timeline)

        r = getSmoothedPathPairs(dm)

        for i in range(0, len(FLAGS.plot_smoothed_path_pairs_timeline), 2):
            target_path_pair_ids = (
                int(FLAGS.plot_smoothed_path_pairs_timeline[i]),
                int(FLAGS.plot_smoothed_path_pairs_timeline[i+1])
                )

            plot_path_pair_msrmnts_timeline(
                dm,
                r,
                target_ppair_ids = target_path_pair_ids,
                out_dir=FLAGS.out_dir
                )

    if len(FLAGS.rtt_timeline_hop_after_stars):
        logging.info("rtt_timeline_hop_after_stars: pids: %s", FLAGS.rtt_timeline_hop_after_stars)

        r = getHopMeasurementsForPathPairs(dm,hdm)
        for i in range(0, len(FLAGS.rtt_timeline_hop_after_stars), 2):
            target_path_pair_ids = (
                int(FLAGS.rtt_timeline_hop_after_stars[i]),
                int(FLAGS.rtt_timeline_hop_after_stars[i+1])
                )

            plot_path_pair_hops_msrmnts_timeline(
                dm,
                r,
                target_ppair_ids = target_path_pair_ids,
                out_dir=FLAGS.out_dir
                )

    if len(FLAGS.plot_path_pairs_timeline_top) == 1:

        r = getPathPairs(dm)
        topklim = int(FLAGS.plot_path_pairs_timeline_top[0])

        plot_path_pair_msrmnts_timeline_topk(
            dm, r, topklim=topklim, out_dir=FLAGS.out_dir)

    if FLAGS.plot_total_unique_paths_cdf:
        logging.info("plot_total_unique_paths_cdf")

        res_tuples = getUniquePathCount4tracedir(dm)
        plot_total_unique_paths_cdf(res_tuples, FLAGS.out_dir)

    if FLAGS.plot_new_paths_frequencies:
        logging.info("plot_new_paths_frequencies")

        res_tuples = getNewPathFrequency(dm)

        plot_newpaths_frequency(res_tuples, FLAGS.out_dir)


    if FLAGS.plot_paths_stability:
        logging.info("plot_paths_stability")
        plot_tuples = generateSummerizedPathVsLifetime(dm)
        plot_paths_stability(plot_tuples, out_dir=FLAGS.out_dir)


    if FLAGS.plot_paths_prevalance:
        logging.info("plot_paths_prevalance")
        plot_tuples = getPathsPrevalance(dm)
        plot_paths_prevalance(plot_tuples, out_dir=FLAGS.out_dir)


    if FLAGS.plot_paths_lifetime:
        logging.info("plot_paths_lifetime")
        plot_tuples = generatePathVsLifetime(dm)
        plot_paths_lifetime_boxplot(plot_tuples, out_dir=FLAGS.out_dir)
        plot_paths_lifetime_cdf(plot_tuples,out_dir=FLAGS.out_dir)
