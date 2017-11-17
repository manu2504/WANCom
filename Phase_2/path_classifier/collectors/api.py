#!/usr/bin/python

import collector_netlink_kfilter as cnetf
import collector_proc_ktracer as cproct

from common import *
from constructor import *
import logging

import config as conf



initiated_probes = []
""" For each traceroute we likely to have multiple bounced probes (ttl overshoot) and
multiple ICMP TE probes (1 per hop), they presorted in dic based on tcp_seq_id 0->255 """
bounced_probes = {}
icmp_probes = {}


def init():

    for tcp_seq_id in range(0, 256):
        bounced_probes[tcp_seq_id] =  []
        icmp_probes[tcp_seq_id] =  []



def get_new_path_traces():


    get_report_ktracer(initiated_probes)

    get_report_kfilter(icmp_probes, bounced_probes)


    # dump_unsorted_buff()
    new_nps_and_hopMeasurements = reconstruct_full_paths(initiated_probes, icmp_probes, bounced_probes)


    return new_nps_and_hopMeasurements






    # print "List len", len(initiated_probes)


def get_report_ktracer(init_plist):



    """ This function retrieves data from Tectonic's tracerouting module that
    sends probes """
    cfg_api = conf.kpa["ktracer"]

    if cfg_api == conf.KER_API_PROC:
        cproct.read_tracer_msgs(init_plist)
    elif cfg_api == conf.KER_API_NETLINK:
        raise NotImplementedError("ktracer kpa [%s]", cfg_api)
    else:
        raise RuntimeError("Undefined Configuration for kpa [%s]", cfg_api)



def get_report_kfilter(icmp_pdic, bnc_plist):

    cfg_api = conf.kpa["kfilter"]

    if cfg_api == conf.KER_API_PROC:
        cproct.read_filter_msgs(icmp_pdic, bnc_plist)
    elif cfg_api == conf.KER_API_NETLINK:
        cnetf.read_filter_msgs(icmp_pdic, bnc_plist)
    else:
        raise RuntimeError("Undefined Configuration for kpa [%s]", cfg_api)


def dump_unsorted_buff():
    print "Unsorted buffer ---------------------------------"
    print "Initiated:"
    for probe in initiated_probes:
        print probe

    print "\nICMPs:"
    for k in range(0, 255):
        val = icmp_probes[k]
        if len(val):
            for i, v in enumerate(val):
                if i == 0:
                    print "[%i]   %s" % (k, v)
                else:
                    print "     ", v

    print "\nBounced:"
    for k in range(0, 255):
        val = bounced_probes[k]
        if len(val):
            for i, v in enumerate(val):
                if i == 0:
                    print "[%i] %s" % (k, v)
                else:
                    print "     ", v
