#!/usr/bin/python

import socket
import os
import time
import logging
import numpy as np
import netaddr
import logging

from struct import *
from common import *

# see ktracer.h, these values must match kernel module
TRC_BOUNCED_PROBE = 10
TRC_ICMPTE_PROBE = 20

TRC_BOUNCE_PROBE_LEN = 24 # Excluding 1 byte msg type
TRC_ICMPTE_PROBE_LEN = 24

NETLINK_KFILTER_GROUP = 31



kfltr_sock = None

def init_socket():
    global kfltr_sock
    kfltr_sock = socket.socket(socket.AF_NETLINK, socket.SOCK_DGRAM, socket.NETLINK_USERSOCK)

    kfltr_sock.bind((0, 0))

    kfltr_sock.setblocking(False)

    # 270 is SOL_NETLINK and 1 is NETLINK_ADD_MEMBERSHIP
    kfltr_sock.setsockopt(270, 1, NETLINK_KFILTER_GROUP)

def read_filter_msgs(icmp_pdic, bnc_plist):

    if kfltr_sock is None:
        init_socket()


    while True:

        try:
            offset = 16
            val = kfltr_sock.recvfrom(256)[0]


            # print "Total length [%i] [%i]" % \
            # (len(val), len(val) - offset - TRC_ICMPTE_PROBE_LEN)


            msg_type = unpack("<I", val[offset:offset+4])[0]
            offset += 4


            (unused1, trace_tcp_seq_id, ttl, rqst_magic) = unpack(
                                                        "<BBBB", val[offset : offset+4])
            offset += 4

            # print "Type[%i][%i %i %i %i]" % (msg_type, unused1, trace_tcp_seq_id, ttl, rqst_magic)

            if msg_type == TRC_ICMPTE_PROBE:

                src_ip, dst_ip, hop_ip, rcv_time_ns = parse_icmp_probe(val, offset)

                icmp_pdic[trace_tcp_seq_id].append(
                    IcmpProbe(src_ip, dst_ip, hop_ip, rcv_time_ns, ttl)
                    )

            elif msg_type == TRC_BOUNCED_PROBE:

                src_ip, dst_ip, bounce_time_ns, rcv_time_ns = parse_bounced_probe(
                                                                            val, offset)

                bnc_plist[trace_tcp_seq_id].append(
                    BouncedProbe(src_ip, dst_ip, bounce_time_ns, rcv_time_ns, ttl)
                    )

            else:
                logging.warning("Rcv unknown msg type from kernel netlink [%s]", msg_type)


        except socket.error:
            break


def parse_icmp_probe(val, offset):

    (src_ip, dst_ip, hop_ip) = \
        unpack("<III", val[offset : offset+TRC_ICMPTE_PROBE_LEN-8-4])

    rcv_time_ns = np.uint64()
    rcv_time_ns = unpack("<Q", val[-8:])[0]

    src_ip = socket.inet_ntoa(pack('!L', src_ip))
    dst_ip = socket.inet_ntoa(pack('!L', dst_ip))
    hop_ip = socket.inet_ntoa(pack('!L', hop_ip))

    # print "Icmp : ", src_ip, dst_ip, hop_ip, tcp_seq, rcv_time_ns
    return (src_ip, dst_ip, hop_ip, rcv_time_ns)




def parse_bounced_probe(val, offset):

    rcv_time_ns = np.uint64()
    bounce_time_ns = np.uint64()

    (src_ip, dst_ip, bounce_time_ns, rcv_time_ns) = \
        unpack("<IIQQ", val[offset : offset+TRC_ICMPTE_PROBE_LEN])

    src_ip = socket.inet_ntoa(pack('!L', src_ip))
    dst_ip = socket.inet_ntoa(pack('!L', dst_ip))


    # print "Bounce: ", src_ip, dst_ip, bounce_time_ns, rcv_time_ns
    return (src_ip, dst_ip, bounce_time_ns, rcv_time_ns)


