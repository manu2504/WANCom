#!/usr/bin/python

import logging
import numpy as np
import os
import socket
import struct
import subprocess
import config as conf

from common import *

from models.InitProbe import InitProbe
from models.BouncedProbe import BouncedProbe
from models.IcmpProbe import IcmpProbe


log = conf.get_logger("collectors", conf.log_collectors)

PROC_KTRACER_SENDER_FNAME = "ktracer.sender.log"
PROC_KTRACER_BOUNCE_FNAME = "ktracer.bounce.log"
PROC_KTRACER_ICMP_FNAME = "ktracer.receiver.log"

ktracer_initprobes_log_fpath = os.path.join("/proc", PROC_KTRACER_SENDER_FNAME)
ktracer_bounce_log_fpath = os.path.join("/proc", PROC_KTRACER_BOUNCE_FNAME)
ktracer_icmp_log_fpath = os.path.join("/proc", PROC_KTRACER_ICMP_FNAME)


def read_tracer_msgs(init_plist):

    pid = subprocess.Popen(["cat", ktracer_initprobes_log_fpath], stdout=subprocess.PIPE)

    for line in pid.stdout:

        tokens = line.rstrip().split(" ")

        if len(tokens) != 5:
            log.error("Skipping non parsable proc line [%s]", tokens)
            continue


        src_ip = tokens[0]
        dst_ip = tokens[1]
        trace_tcp_seq_id = (int)(tokens[2])

        # '<' indicate that we are dealing with little endian this is how we pass to proc
        src_ip = socket.inet_ntoa(struct.pack('<L', int(src_ip)))
        dst_ip = socket.inet_ntoa(struct.pack('<L', int(dst_ip)))
        send_time_ns = np.uint64(tokens[3])

        init_plist.append(InitProbe(src_ip, dst_ip, trace_tcp_seq_id, send_time_ns))

        # print src_ip, dst_ip, trace_tcp_seq_id, send_time_ns



def read_filter_msgs(icmp_pdic, bnc_plist):

    read_bounce_probes(bnc_plist)

    read_icmp_probes(icmp_pdic)



def read_bounce_probes(bnc_plist):

    pid = subprocess.Popen(["cat", ktracer_bounce_log_fpath], stdout=subprocess.PIPE)

    bnc_probes_tcp_ids = []

    for line in pid.stdout:

        tokens = line.rstrip().split(" ")

        if len(tokens) != 7:
            log.error("Skipping non parsable bounce proc line [%s]", tokens)
            continue

        ignored_type = tokens[0]


        trace_tcp_seq_id = (int)(tokens[1])
        val = struct.pack("I", trace_tcp_seq_id)
        (unused1, trace_tcp_seq_id, ttl, rqst_magic) = struct.unpack("<BBBB", val)
        # print "Type[%i %i %i %i]" % (unused1, trace_tcp_seq_id, ttl, rqst_magic)

        src_ip = tokens[2]
        dst_ip = tokens[3]

        src_ip = socket.inet_ntoa(struct.pack('>L', int(src_ip)))
        dst_ip = socket.inet_ntoa(struct.pack('>L', int(dst_ip)))

        bounce_time_ns = np.uint64(tokens[4])
        rcv_time_ns = np.uint64(tokens[5])
        unused_rtt_ns = np.uint64(tokens[6]) # TODO: see if you need this.

        bnc_plist[trace_tcp_seq_id].append(
            BouncedProbe(src_ip, dst_ip, bounce_time_ns, rcv_time_ns, ttl)
            )
        bnc_probes_tcp_ids.append((str)(trace_tcp_seq_id))

        # print src_ip, dst_ip, trace_tcp_seq_id, bounce_time_ns, rcv_time_ns


    if len(bnc_probes_tcp_ids):
        log.debug("Collected Bounced tcp_ids [%s]", " ".join(set(bnc_probes_tcp_ids)))



def read_icmp_probes(icmp_pdic):

    pid = subprocess.Popen(["cat", ktracer_icmp_log_fpath], stdout=subprocess.PIPE)

    for line in pid.stdout:

        tokens = line.rstrip().split(" ")

        if len(tokens) != 6:
            log.error("Skipping non parsable icmp proc line [%s]", tokens)
            continue

        ignored_type = tokens[0]


        trace_tcp_seq_id = (int)(tokens[1])
        val = struct.pack("I", trace_tcp_seq_id)
        (unused1, trace_tcp_seq_id, ttl, rqst_magic) = struct.unpack("<BBBB", val)
        # print "Type[%i %i %i %i]" % (unused1, trace_tcp_seq_id, ttl, rqst_magic)

        src_ip = tokens[2]
        dst_ip = tokens[3]
        hop_ip = tokens[4]

        src_ip = socket.inet_ntoa(struct.pack('>L', int(src_ip)))
        dst_ip = socket.inet_ntoa(struct.pack('>L', int(dst_ip)))
        hop_ip = socket.inet_ntoa(struct.pack('>L', int(hop_ip)))

        rcv_time_ns = np.uint64(tokens[5])

        icmp_pdic[trace_tcp_seq_id].append(
            IcmpProbe(src_ip, dst_ip, hop_ip, rcv_time_ns, ttl)
            )

        # print "Icmp : ", src_ip, dst_ip, hop_ip, trace_tcp_seq_id, rcv_time_ns
