#!/usr/bin/python
import time
import logging

import numpy as np
import config as conf

from common import *
from models.HopMeasurement import HopMeasurement

log = conf.get_logger("path_asm", conf.log_path_asm)

class NetworkPathContainer():

    def __init__(self, hops_list, trace_start_time_ns, rtt_ns, bounce_time_ns,
        owd_forward_ns, owd_reverse_ns,
        stars_match_any_ip=False):
        """
        The first hop is the src_ip and last is the dst_ip
        """
        self.hops = hops_list
        self.stars_match_any_ip = stars_match_any_ip

        self.trace_start_time_ns = trace_start_time_ns

        # Exact RTT as measured from the senders side
        self.rtt_ns = rtt_ns

        # The time when probe reached dst, based on remote wall clock
        # Approximate representation of OWD
        self.bounce_time_ns = bounce_time_ns

        # tDelta from the moment probe has been sent (based on local clock) until
        # the moment probe has arrived to remote node (based on remote clock)
        self.owd_forward_ns = owd_forward_ns

        # tDelta from the moment probe has been bounced from remote node
        #(based on remote clock), until the moment probe has came back
        #(base on local clock)
        self.owd_reverse_ns = owd_reverse_ns

        # Path ID will be assigned when the instance of this path will be commited to db
        self.pid = 0

        # Timestamp of the pair measurement
        self.pair_ts = 0


    def __eq__(self, other_path):
        if len(self.hops) != len(other_path.hops):
            return False


        for h1, h2 in zip(self.hops, other_path.hops):
            if (self.stars_match_any_ip == True and
                (h1.endswith(STAR_SUFFIX) or h2.endswith(STAR_SUFFIX))):
                # if at least one of them is a star hop, check next399M pair of hops
                continue


            if h1 != h2:
                return False

        return True


    def __neq__(self, other_path):
        return not self.__eq__(other_path)

    def __hash__(self):
        return hash("".join(self.hops))

    def set_pid(self, pid):
        self.pid = pid

    def get_hash(self):
        return hash("".join(self.hops))

    def get_dst_ip(self):
        return self.hops[-1]

    def get_src_ip(self):
        return self.hops[0]

    def __str__(self):
        # for shortness we print only last digit of each path
        # for quick visual inspection, to print use self.tostr()
        ips = self.hops
        ips_processed = []
        for ip in ips:
            ip_split = ip.split(".")
            if len(ip_split) == 4:
                ips_processed.append(ip_split[3])
            else:
                ips_processed.append(ip)
        return ".".join(ips_processed)

    def tostr(self, vertical=False):
        if vertical:
            for i, hop in enumerate(self.hops):
                print "[%d] %s" %(i, hop)
        else:
            return "[" + " ".join(self.hops) + "]"


def is_oldenough2process(in_probe):

    launch_time_ms = (np.uint64)(in_probe.send_time_ns // 1000000)
    time_now_ms = (int)(time.time() * 1000) # time()->gives usec

    return time_now_ms - launch_time_ms > conf.pasm["wait4probes_ms"]


def do_timeline_sanity_check(in_probe, rcvd_probes):
    # Sanity check, all probes should be recent! TODO: is graceful failure?

    for p in rcvd_probes:
        if p.rcv_time_ns < in_probe.send_time_ns:
            log.error("Rcv time of the [%s] probe is smaller then trace init time",
                type(p))
            # assert False

        if (p.rcv_time_ns - in_probe.send_time_ns) // 1000000 > conf.pasm["old_probes_check_ms"] :
            log.error("Old [%s] probe in a buffer", type(p))
            # assert False




def get_smallest_bounced_probe(in_probe, bn_probe_dic):
    """ Function returns a single bounced probe. Out of the list of all bounced probes
    that we received, we return the one with the smallest TTL, i.e., the probe that
    corresponds to the actual distance to the destination """
    bn_probes = bn_probe_dic[in_probe.trace_tcp_seq_id]

    # 1. Check for some values in the list
    if len(bn_probes) == 0:
        return None

    # 2.
    do_timeline_sanity_check(in_probe, bn_probes)

    # 3.
    smallest_hopid_probe = bn_probes[0]
    for bnp in bn_probes:
        if bnp.hop_id < smallest_hopid_probe.hop_id:
            smallest_hopid_probe = bnp

    return smallest_hopid_probe


def get_icmp_sorted_probes(in_probe, icmp_probes_dic):

    # print "key: ", in_probe.trace_tcp_seq_id
    # print icmp_probe_dic
    ic_probes = icmp_probes_dic[in_probe.trace_tcp_seq_id]

    # 1.
    if len(ic_probes) == 0:
        return None

    # 2.
    do_timeline_sanity_check(in_probe, ic_probes)

    ic_probes.sort(key=lambda x: x.hop_id, reverse=False)

    return ic_probes



def clean_up_buffer(in_probes_list, icmp_probes_dic, bounced_probes_dic, iids_to_delete):

    # reversing to remove indexes iteratively from in_probes_list
    for iid in reversed(iids_to_delete):
        # log.debug("Removing iid [%i]", iid)

        bounced_probes_dic[ in_probes_list[iid].trace_tcp_seq_id ] = []
        icmp_probes_dic[ in_probes_list[iid].trace_tcp_seq_id ] = []
        del in_probes_list[iid]


def clean_old_probes(in_probes_list, icmp_probes_dic, bounced_probes_dic):
    inp_ids = []
    time_now_ms = (np.uint64)(time.time() * 1000)
    for i,inprobe in enumerate(in_probes_list):
        send_time_ms = inprobe.send_time_ns // 1000 // 1000
        if time_now_ms - send_time_ms > conf.construc["probes_timeout"]:
            log.debug("Timedout Init probe")
            log.debug(inprobe)
            inp_ids.append(i)
    delete_indexes_from_list(in_probes_list,inp_ids)

    for key, icmp_probes in icmp_probes_dic.iteritems():
        icmpp_ids = []
        for i,icmp_probe in enumerate(icmp_probes):
            rcv_time_ms = icmp_probe.rcv_time_ns // 1000 // 1000
            if time_now_ms - rcv_time_ms > conf.construc["probes_timeout"]:
                log.debug("Timedout ICMP probe")
                log.debug(icmp_probe)
                icmpp_ids.append(i)
        log.debug("Removing %i old probes",len(icmpp_ids))
        delete_indexes_from_list(icmp_probes,icmpp_ids)

    for key, bounced_probes in icmp_probes_dic.iteritems():
        bnp_ids = []
        for i,bounce_probe in enumerate(bounced_probes):
            rcv_time_ms = bounce_probe.rcv_time_ns // 1000 // 1000
            if time_now_ms - rcv_time_ms > conf.construc["probes_timeout"]:
                log.debug("Timedout bounced probe")
                log.debug(bounce_probe)
                bnp_ids.append(i)
        log.debug("Removing %i old probes",len(icmpp_ids))
        delete_indexes_from_list(bounced_probes,bnp_ids)



def store_new_paths_by_dst(paths_dic, new_path):

    if new_path.get_dst_ip() in paths_dic:
        paths_dic[new_path.get_dst_ip()].append(new_path)
    else:
        paths_dic[new_path.get_dst_ip()] = [new_path]
    return paths_dic




def reconstruct_full_paths(in_probes_list, icmp_probes_dic, bounced_probes_dic):

    iids_to_delete = []

    new_network_paths_dic = {}
    new_hop_measurements_dic = {}

    hop_measurements_list = []
    # log.debug("Assembling Paths sizes in/icmp/bnc[%i, %i %i]",
    #     len(in_probes_list),
    #     count_paths_in_dic(icmp_probes_dic),
    #     count_paths_in_dic(bounced_probes_dic))

    for iid, in_probe  in enumerate(in_probes_list):

        if is_oldenough2process(in_probe):

            bn_probe = get_smallest_bounced_probe(in_probe, bounced_probes_dic)

            if not bn_probe:
                iids_to_delete.append(iid)
                log.warning("Could not obtain bn_probe for in_probe [%s] (removing)",
                    in_probe)
                continue


            ic_probes = get_icmp_sorted_probes(in_probe, icmp_probes_dic)

            if not ic_probes:
                iids_to_delete.append(iid)
                log.warning("Could not obtain icmps for in_probe [%s] (removing)",
                    in_probe)
                continue

            netp = construct_network_path(in_probe, ic_probes, bn_probe)

            if netp:
                new_network_paths_dic = store_new_paths_by_dst(
                    new_network_paths_dic, netp[0])
                log.debug("Asm-ps [%s]", netp[0])
                hop_measurements_list = hop_measurements_list + netp[1]
            else:
                log.error("Failed to assemble complete Path!")

            # If we finished with assembly, we should remove used entries from tmp buffers
            iids_to_delete.append(iid)



    clean_up_buffer(in_probes_list, icmp_probes_dic, bounced_probes_dic, iids_to_delete)

    clean_old_probes(in_probes_list, icmp_probes_dic, bounced_probes_dic)

    log.debug("Assembled [%i] paths", count_paths_in_dic(new_network_paths_dic))
    return (new_network_paths_dic,hop_measurements_list)



def construct_network_path(in_probe, ic_probes, bn_probe):

    hops_list = []

    path_hop_measurements_list = []
    hops_list.append(in_probe.src_ip)


    if (in_probe.send_time_ns > bn_probe.rcv_time_ns):
        log.info("Received probe is older than sent probe. Bounced probe timestamp: %d, Sent probe timestamp %d", bn_probe.rcv_time_ns, in_probe.send_time_ns)
        return None

    # Allocate list of "*" for the total number of intermediate hops. Then replace
    # all "*" with IPs at known positions
    n_hops = bn_probe.hop_id - 1
    inter_hops = ["*"]*n_hops

    try:
        for icp in ic_probes:
            # hops_list.append(icp.hop_ip)
            print "--> ", icp.hop_id, n_hops
            inter_hops[icp.hop_id - 1] = icp.hop_ip
            if (in_probe.send_time_ns < icp.rcv_time_ns):
                hopMeasurement = HopMeasurement(ipSrc=icp.src_ip,ipDst=(inter_hops[icp.hop_id - 1]),rtt=(icp.rcv_time_ns - in_probe.send_time_ns),idMeasurement=in_probe.send_time_ns)
                path_hop_measurements_list.append(hopMeasurement)
    except IndexError as e:
        return None
    hops_list += inter_hops

    hops_list.append(bn_probe.dst_ip)

    rtt_ns = (bn_probe.rcv_time_ns - in_probe.send_time_ns)


    bounce_time_ns = bn_probe.bounce_time_ns
    owd_forward_ns = bn_probe.bounce_time_ns - in_probe.send_time_ns
    owd_reverse_ns = bn_probe.rcv_time_ns - bn_probe.bounce_time_ns

    netp = NetworkPathContainer(hops_list,
        trace_start_time_ns=in_probe.send_time_ns,
        rtt_ns=rtt_ns,
        owd_forward_ns=owd_forward_ns,
        owd_reverse_ns=owd_reverse_ns,
        bounce_time_ns=bounce_time_ns)

    print netp.tostr()

    return (netp,path_hop_measurements_list)
