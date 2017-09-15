#!/usr/bin/python

import logging
import os
import random
import joblib
import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from pytools.common.common import *
from pytools.common.io import *
from pytools.experiments.exp_common import *
from pytools.plots.py_plot import *
from viscommon import *
from datafactory import *


def _add_box_plot(box_vals, box_labels, msrmnts_ns, path_pair_ids, topk):

    rtt_vals_ms = [x / E6flt for x in msrmnts_ns]
    box_labels.append(str(len(rtt_vals_ms)))
    box_vals.append(rtt_vals_ms)

    # plot hidden line to display legend
    plt.plot([0,0], [0,0], label="%i) [%i] pids: %s" %
        (topk, len(rtt_vals_ms), path_pair_ids)
        )

def plot_path_pairs(ppdic, topklim=30, show=False, bidirectional=False, out_dir="./out"):
    logging.info("Plotting Path Pairs [topklim:%i][bidir:%s][outdir:%s]",
        topklim, bidirectional, out_dir)
    for tdid, paired_mes_list in ppdic.iteritems():

        box_vals = []
        box_labels = []

        plot_name = paired_mes_list[0].plot_name # all names for one tdid should match

        pmc_list = sorted(# sort by number of matches, in case if not sorted
            paired_mes_list, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)

        get_new_figure()

        for topk, pmc  in enumerate(pmc_list):

            _add_box_plot(box_vals, box_labels,
                pmc.get_frwd_rtts(), pmc.path_pair_ids, topk)

            if bidirectional == "True" or bidirectional == "true":
                _add_box_plot(box_vals, [],
                    pmc.get_rvrs_rtts(), pmc.path_pair_ids[::-1], topk)
                box_labels.append(" ") # avoid duplicate labels on x axis

            if topk >= topklim: break


        boxes = plt.boxplot(box_vals, labels=box_labels, showfliers=True)

        plt.grid()
        ylim = suggest_plots_lims(box_vals, 0, 99)
        plt.ylim(ylim[0]-5, ylim[1]+5)
        plt.xlabel('Matched Path Pairs')
        plt.ylabel('Latency ms')
        plt.title("Path Pairs RTT "+plot_name)
        plt.xticks(rotation=45)

        if bidirectional == "True" or bidirectional == "true":
            plt.title("Path Pairs RTT "+plot_name+" Frwd(blue)/Rvrs(red) boxes")
            for i, patch in enumerate(boxes['boxes']):
                if i % 2 == 1:
                    patch.set(color=clr_darkred)


        # Place outside of the plots
        ax = plt.gca()
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            prop=make_font(size=8))

        if show:
            plt.show()
        else:

            of_name = os.path.join(out_dir, "plot_path_pairs")
            make_dir(of_name)
            of_name += "/" + plot_name + ".png"
            logging.info("Out plot file: [%s]", of_name)

            plt.savefig(of_name, bbox_inches='tight')


        close_figure()

def plot_path_persistance_cdf(dm):

    samples = random.sample(xrange(10000), 1000)

    x, y = create_ecdf_for_plot(samples, len(samples))


    plt.figure(dpi=1000, figsize=(18,10))


    plt.plot(x, y, label="sample")

    plt.grid()
    plt.xlabel('CDF')
    plt.ylabel('Random Values')
    plt.legend(loc="best")

    plt.savefig("cdf_sample.png", bbox_inches='tight')

    close_figure()



def _plot_tracedir_rtt(res_tuples, out_dir, show=False):

    for tpl in res_tuples:

        # dump data
        # TODO: probably should be separated as intensive IO might need a different N of threads
        data_name = "/"+tpl[0]+".csv"
        of_data = os.path.join(out_dir, "data_tracedir_rtt")
        make_dir(of_data)
        of_data += data_name
        io_tuple_list2file(tpl[1], ofname=of_data)
        logging.info("Out data file: [%s]", of_data)

        # plotting
        plot_name = tpl[0]
        plt.figure(dpi=1000, figsize=(18,10))


        x_data = [v[0] / E9int for v in tpl[1]]
        x_data = [datetime.datetime.utcfromtimestamp(v) for v in x_data]

        y_data = [v[1] / E6flt for v in tpl[1]]

        plt.plot(x_data, y_data, label=plot_name)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%m'))
        plt.gcf().autofmt_xdate()
        plt.grid()
        plt.ylim(0, 500)
        plt.xlabel('Time')
        plt.ylabel('Latency ms')
        plt.title("RTT "+plot_name)
        plt.legend(loc="best")


        # 4. render to screen or file
        if show:
            plt.show()
        else:
            of_name = os.path.join(out_dir, "plot_tracedir_rtt")
            make_dir(of_name)
            of_name += "/" + plot_name + ".png"
            logging.info("Out plot file: [%s]", of_name)

            plt.savefig(of_name, bbox_inches='tight')

        close_figure()


def plot_tracedir_rtt(plot_tuples, out_dir):
    logging.info("Start    plotting")

    tasks = (
            joblib.delayed(_plot_tracedir_rtt)(tuples_sublist, out_dir, show=False)
            for tuples_sublist in chunk_list_by_nsets(plot_tuples, number_of_sublists=8)
    )
    return joblib.Parallel(n_jobs=1, verbose=50)(tasks)

    logging.info("Finished plotting")


##########################################################################################
### Plot Histograms ######################################################################
##########################################################################################

def _plot_path_pair_msrmnts_histogram(samples, title, show, out_legend_buf, out_dir):

    get_new_figure()

    x = [x / E6flt for x in samples]

    nbins = int((max(x) - min(x)) * 10)


    n, bins, patches = plt.hist(x, nbins, normed=0, facecolor='green', alpha=0.75)

    for legend in out_legend_buf:
        plt.plot([0,0], [0,0], label=legend, color="k")

    plt.ylabel("Frequency")
    plt.xlabel("Latency [ms] (step 0.1 [ms])")
    plt.xlim(min(x)-10, max(x)+10)
    plt.grid()
    title = "RTT {plot_name} [nbins: {nbins}]".format(plot_name=title, nbins=nbins)
    plt.title(title)
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            prop=make_font(size=8))

    if show:
        plt.show()
    else:
        of_name = os.path.join(out_dir, "plot_path_pair_hist")
        make_dir(of_name)
        of_name += "/" + title + ".png"
        logging.info("Out plot file: [%s]", of_name)

        plt.savefig(of_name, bbox_inches='tight')

    close_figure()

def plot_path_pair_msrmnts_histogram(ppdic, tdid, plot_name, target_ppair_ids,
    show=False, out_legend_buf=[], out_dir="./out"):
    """ For a particular path pair in ppdic prints latency histogram """

    for i, pmc in enumerate(ppdic[tdid]):

        if pmc.path_pair_ids == target_ppair_ids:
            logging.info("Path Pair with pids [%s] found, plotting", target_ppair_ids)
            title = plot_name + "_[len:%i_%i_%i]" % (
                len(pmc.frwd_msrmnts_tspairs), target_ppair_ids[0], target_ppair_ids[1]
                )
            _plot_path_pair_msrmnts_histogram(
                pmc.get_frwd_rtts(), title, show, out_legend_buf, out_dir)

##########################################################################################
### Plot Path Pair Timeline ##############################################################
##########################################################################################
def _plot_path_pair_msrmnts_timeline(xy_pairs, title, show, out_legend_buf, out_dir):

    x_data = [v[1] / E9int for v in xy_pairs]
    x_data = [datetime.datetime.utcfromtimestamp(v) for v in x_data]

    y_data = [v[0] / E6flt for v in xy_pairs]

    get_new_figure()

    plt.plot(x_data, y_data, 'o', markerfacecolor="k", markeredgecolor='k',
        markersize=3)


    for legend in out_legend_buf:
        plt.plot([x_data[0]], [0], 'o', label=legend, color="k")

    plt.ylabel("RTT [ms]")
    plt.xlabel("Time")
    plt.ylim(min(y_data)-10, max(y_data)+10)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M:%S'))
    plt.gcf().autofmt_xdate()

    plt.grid()
    title = "RTT {plot_name}".format(plot_name=title)
    plt.title(title)
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            prop=make_font(size=8))

    if show:
        plt.show()
    else:
        of_name = os.path.join(out_dir, "plot_path_pair_timeline")
        make_dir(of_name)
        of_name += "/" + title + ".png"
        logging.info("Out plot file: [%s]", of_name)

        plt.savefig(of_name, bbox_inches='tight')

    close_figure()


def plot_path_pair_msrmnts_timeline(dm, ppdic, target_ppair_ids,
    show=False, out_dir="./out"):

    for _, pmc_list in ppdic.iteritems():

        pmc_list = sorted(# sort by number of matches, in case if not sorted
            pmc_list, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)

        for topk, pmc in enumerate(pmc_list):

            if pmc.path_pair_ids == target_ppair_ids:
                logging.info("Path Pair with pids [%s] found, plotting", target_ppair_ids)

                pmc.sort_measurements_by_timestamp_ns()

                title = pmc.plot_name + "_timeline_[top:%i_len:%i_%i_%i]" % (topk,
                    len(pmc.frwd_msrmnts_tspairs), target_ppair_ids[0], target_ppair_ids[1]
                    )

                out_legend_buf = path_pair_ids2legend_names(dm, target_ppair_ids)

                _plot_path_pair_msrmnts_timeline(
                    pmc.frwd_msrmnts_tspairs, title, show, out_legend_buf, out_dir)

def plot_path_pair_msrmnts_timeline_topk(dm, ppdic, topklim, out_dir):


    for _, pmc_list in ppdic.iteritems():

        pmc_list = sorted(# sort by number of matches, in case if not sorted
            pmc_list, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)

        for topk, pmc in enumerate(pmc_list):

            logging.info("Ploit top:%i path pair, pids [%s]", topk, pmc.path_pair_ids)

            pmc.sort_measurements_by_timestamp()

            title = pmc.plot_name + "_timeline_[top:%i_len:%i_%i_%i]" % (topk,
                len(pmc.frwd_msrmnts_tspairs), pmc.path_pair_ids[0], pmc.path_pair_ids[1]
                )

            out_legend_buf = path_pair_ids2legend_names(dm, pmc.path_pair_ids)

            _plot_path_pair_msrmnts_timeline(
                pmc.frwd_msrmnts_tspairs, title, False, out_legend_buf, out_dir)

            if topk >= topklim: break


##########################################################################################
### Plot Path Pair Hops Timeline ##############################################################
##########################################################################################

def plot_path_pair_hops_msrmnts_timeline(dm, ppdic, target_ppair_ids,
    show=False, out_dir="./out"):

    for _, pmc_list in ppdic.iteritems():

        #pmc_list = sorted(# sort by number of matches, in case if not sorted
        #    pmc_list, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)

        for topk, pmc in enumerate(pmc_list):

            if pmc.path_pair_ids == target_ppair_ids:
                logging.info("Path Pair with pids [%s] found, plotting", target_ppair_ids)

                measurements = getHopMeasurements(dm,pmc)
                print measurements
                pmc.sort_measurements_by_timestamp_ns()

                title = pmc.plot_name + "_timeline_[top:%i_len:%i_%i_%i]" % (topk,
                    len(pmc.frwd_msrmnts_tspairs), target_ppair_ids[0], target_ppair_ids[1]
                    )

                out_legend_buf = path_pair_ids2legend_names(dm, target_ppair_ids)

                _plot_path_pair_msrmnts_timeline(
                    pmc.frwd_msrmnts_tspairs, title, show, out_legend_buf, out_dir)


##########################################################################################
### plot_total_unique_paths_cdf ##########################################################
##########################################################################################

def plot_total_unique_paths_cdf(res_tuples, out_dir):

    plt.figure(dpi=1000, figsize=(18,10))

    data = [x[0] for x in res_tuples]
    x, y = create_ecdf_for_plot(data, len(data)*10)
    plt.plot(x, y)

    for _, leg in res_tuples:
        plt.plot([0,0],[0,0], label=leg)


    # Place outside of the plots
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
        prop=make_font(size=8))

    plt.grid()
    plt.xlabel('Unique Paths')
    plt.ylabel('CDF')
    plt.title("Number of unique paths per trace direction")

    plot_name = "unique_paths_cdf"

    of_name = os.path.join(out_dir, "total_unique_paths")
    make_dir(of_name)
    of_name += "/" + plot_name + ".png"

    logging.info("Out plot file: [%s]", of_name)
    plt.savefig(of_name, bbox_inches='tight')


    close_figure()


##########################################################################################
### plot_frequencies of new paths ########################################################
##########################################################################################


def plot_newpaths_frequency(res_tuples, out_dir):
    """ see getNewPathFrequency for the input data format"""

    for samples, legend, last_timestamp in res_tuples:

        xdata_timestamps = samples + [last_timestamp]

        ydata_cmm_paths = range(1, len(samples)+1)
        # We add one more sample, which correspond to the very last timestamp to mark
        # the end of the X axis, however, the total number of unique paths is the same
        ydata_cmm_paths.append(len(samples)+1)

        plt.figure(dpi=1000, figsize=(18,10))

        plt.plot(xdata_timestamps, ydata_cmm_paths)

        plt.title("New paths frequency " + legend)

        plt.grid()
        plt.ylabel('Total # of unique paths')
        plt.xlabel('Time')


        plot_name = "newpaths_freq"+legend

        of_name = os.path.join(out_dir, "unique_paths_frequency")
        make_dir(of_name)
        of_name += "/" + plot_name + ".png"

        logging.info("Out plot file: [%s]", of_name)
        plt.savefig(of_name, bbox_inches='tight')

        close_figure()


##########################################################################################
### plot_paths_stability of all directions ###############################################
##########################################################################################


def plot_paths_stability(res_tuples, out_dir):
    """ see generatePathVsLifetime for the input data format"""

    for samples, legend in res_tuples:

        n_groups = 3
        fig, ax = plt.subplots()

        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.4

        rects1 = plt.bar(index, samples, bar_width,
                 alpha=opacity,
                 color='b',
                 label=legend)


        ax.set_xticklabels(('less than 1 hour', '1 - 4 hours','more than 4 hours'))
        ax.set_ylabel('Total time spent by paths of certain path duration')
        ax.set_title('Path stability indicator between ' + legend)
        ax.set_xticks(index + bar_width / 2)

        ax.legend((rects1), (legend))

        plot_name = "path_stability_"+legend

        of_name = os.path.join(out_dir, "paths_stability")
        make_dir(of_name)
        of_name += "/" + plot_name + ".png"

        logging.info("Out plot file: [%s]", of_name)
        plt.savefig(of_name, bbox_inches='tight')

        close_figure()


##########################################################################################
### plot_paths_prevalance of all directions ###############################################
##########################################################################################

def _plot_prevalance_per_direction(topPrevalantPathslifeTime,plot_name,out_dir):
    n_groups = 10
    fig, ax = plt.subplots()

    samples = topPrevalantPathslifeTime[0:10]
    index = np.arange(n_groups)
    bar_width = 0.1
    opacity = 0.4

    rects1 = plt.bar(index, samples, bar_width,
             alpha=opacity,
             color='b',
             label='')


    #ax.set_xticklabels(('less than 1 hour', '1 - 4 hours','more than 4 hours'))
    ax.set_ylabel('Amount of time spent by most prevalant paths in seconds')
    ax.set_title('Top 10 most prevalant paths in direction ' + plot_name)
    ax.set_xticks(index + bar_width / 2)

    ax.legend((rects1), (plot_name))

    plot_name = "plot_paths_prevalance"+plot_name

    of_name = os.path.join(out_dir, "plot_paths_prevalance")
    make_dir(of_name)
    of_name += "/" + plot_name + ".png"

    logging.info("Out plot file: [%s]", of_name)
    plt.savefig(of_name, bbox_inches='tight')

    close_figure()

def plot_paths_prevalance(all_lifetimes_dic, out_dir):
    logging.info("Plotting top 10 most prevalant paths and storing output in [outdir:%s]",
          out_dir)

    get_new_figure()
    for td, pathslifetime  in all_lifetimes_dic.iteritems():

        topPrevalantPathslifeTime = sorted(pathslifetime[0].values(), reverse=True)
        _plot_prevalance_per_direction(topPrevalantPathslifeTime, pathslifetime[1],out_dir)





##########################################################################################
### plot_paths_lifetime of all directions ###############################################
##########################################################################################


def plot_paths_lifetime_boxplot(lifetime_dic,  out_dir="./out"):
    logging.info("Plotting Path lifetime [outdir:%s]",
          out_dir)

    box_vals = []
    box_labels = []

    plot_name = "Path lifetime for all paths in different trace directions"
    get_new_figure()
    for td, measurements  in lifetime_dic.iteritems():

        lifetimes = [x[1] for x in measurements[0]]
        print lifetimes

        tracedirToText = []
        plt.plot([0,0], [0,0], label="%s" %
            (measurements[1])
            )
        box_labels.append(measurements[1])
        box_vals.append(lifetimes)


    boxes = plt.boxplot(box_vals, labels=box_labels, showfliers=True)

    plt.grid()
    ylim = suggest_plots_lims(box_vals, 0, 99)
    plt.ylim(ylim[0]-5, ylim[1]+5)
    plt.xlabel('Trace directions')
    plt.ylabel('Paths lifetime in seconds')
    plt.title(plot_name)
    plt.xticks(rotation=45)

        # Place outside of the plots
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
        prop=make_font(size=8))

    of_name = os.path.join(out_dir, "plot_path_lifetime")
    make_dir(of_name)
    of_name += "/" + plot_name + ".png"
    logging.info("Out plot file: [%s]", of_name)

    plt.savefig(of_name, bbox_inches='tight')

    close_figure()


##########################################################################################
### plot_paths_lifetime_cdf ##########################################################
##########################################################################################

def plot_paths_lifetime_cdf(lifetime_dic, out_dir):

    all_lifetimes = []
    for td, measurements  in lifetime_dic.iteritems():

        lifetimes = [x[1] for x in measurements[0]]
        print lifetimes
        all_lifetimes = all_lifetimes + lifetimes

    plt.figure(dpi=1000, figsize=(18,10))
    data = sorted(all_lifetimes,reverse=True)

    x, y = create_ecdf_for_plot(data, max(data))
    plt.plot(x, y)


    # Place outside of the plots
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
        prop=make_font(size=8))

    plt.grid()
    plt.xlabel('Paths lifetimes in seconds')
    plt.ylabel('CDF')
    plt.title("CDF for the paths lifetimes before network paths change")

    plot_name = "paths_lifetime_cdf"

    of_name = os.path.join(out_dir, "plot_path_lifetime")
    make_dir(of_name)
    of_name += "/" + plot_name + ".png"

    logging.info("Out plot file: [%s]", of_name)
    plt.savefig(of_name, bbox_inches='tight')


    close_figure()


##########################################################################################
### plot_normalized_RTT figures ##########################################################
##########################################################################################

def plot_all_path_pairs_normalized(ppdic, topklim=30, show=False, bidirectional=True, out_dir="./out"):
    logging.info("Plotting Path Pairs [topklim:%i][bidir:%s][outdir:%s]",
        topklim, bidirectional, out_dir)

    box_vals = []
    box_labels = []

    plot_name = "Normalized RTT value for all paths in different trace directions"
    get_new_figure()
    for td, measurements  in ppdic.iteritems():

        frwdRTTs = [x[0] for x in measurements[0][0]]
        rvsRTTs = [x[0] for x in measurements[0][1]]


        tracedirToText = []
        plt.plot([0,0], [0,0], label="%s" %
            (measurements[1])
            )
        box_labels.append(" ")
        box_vals.append(frwdRTTs)
        if bidirectional == "True" or bidirectional == "true":
            plt.plot([0,0], [0,0], label="%s" %
                (measurements[1])
                )
            box_labels.append(" ") # avoid duplicate labels on x axis
            box_vals.append(rvsRTTs)


    boxes = plt.boxplot(box_vals, labels=box_labels, showfliers=True)

    plt.grid()
    ylim = suggest_plots_lims(box_vals, 0, 99)
    plt.ylim(ylim[0]-1, ylim[1]+1)
    plt.xlabel('Matched Path Pairs')
    plt.ylabel('Latency ms')
    plt.title("Path Pairs RTT "+plot_name)
    plt.xticks(rotation=45)

    if bidirectional == "True" or bidirectional == "true":
        plt.title("Normzlied Path Pairs RTT All trace directions Frwd(blue)/Rvrs(red) boxes")
        for i, patch in enumerate(boxes['boxes']):
            if i % 2 == 1:
                patch.set(color=clr_darkred)


        # Place outside of the plots
    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
        prop=make_font(size=8))

    if show:
        plt.show()
    else:

        of_name = os.path.join(out_dir, "plot_path_pairs_normalized")
        make_dir(of_name)
        of_name += "/" + plot_name + ".png"
        logging.info("Out plot file: [%s]", of_name)

        plt.savefig(of_name, bbox_inches='tight')


    close_figure()


def plot_all_path_pairs_normalized_cdf(ppdic, out_dir="./out"):
    logging.info("Plotting Normalized network delay CDF figures")

    all_vals = []

    for td, measurements  in ppdic.iteritems():

        frwdRTTs = [x[0] for x in measurements[0][0]]
        frwdRTTs = sorted(frwdRTTs,reverse=True)

        print frwdRTTs[0:10]

        print min(frwdRTTs)
        print max(frwdRTTs)

        plot_name = measurements[1]

        all_vals = all_vals + frwdRTTs

        get_new_figure()
        ecdf = sm.distributions.ECDF(frwdRTTs)

        x = np.linspace(min(frwdRTTs), 2, num=max(frwdRTTs))
    	y = ecdf(x)
        x, y = create_ecdf_for_plot(frwdRTTs, max(frwdRTTs))
        plt.plot(x, y)

        ax = plt.gca()
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                prop=make_font(size=8))
        plt.grid()

        plt.xlabel('Measured network delay normalized to the smallest measured network delay for each network path')
        plt.ylabel('CDF')
        plt.title("CDF for the network paths delay normalized to the smallest measured netwok delay for all network paths in direction " + measurements[1])

        of_name = os.path.join(out_dir, "plot_path_pairs_normalized")
        make_dir(of_name)
        of_name += "/" + plot_name + ".png"

        logging.info("Out plot file: [%s]", of_name)
        plt.savefig(of_name, bbox_inches='tight')

        close_figure()

    get_new_figure()
    all_vals = sorted(all_vals,reverse=True)
    x, y = create_ecdf_for_plot(all_vals, max(all_vals))
    plt.plot(x, y)

    print all_vals[0:30]

    ax = plt.gca()
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            prop=make_font(size=8))
    plt.grid()

    plt.xlabel('Measured network delay normalized to the smallest measured network delay for each network path')
    plt.ylabel('CDF')
    plt.title("CDF for the network paths delay normalized to the smallest measured netwok delay for all network paths in all directions")

    plot_name = "normalized_rtt_cdf_all_directions"
    of_name = os.path.join(out_dir, "plot_path_pairs_normalized")
    make_dir(of_name)
    of_name += "/" + plot_name + ".png"

    logging.info("Out plot file: [%s]", of_name)
    plt.savefig(of_name, bbox_inches='tight')

    close_figure()
