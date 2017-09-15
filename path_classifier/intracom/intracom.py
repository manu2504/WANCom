#!/usr/bin/python

import socket

import config as conf
import logging
import pickle
"""
This class is responsible for internal communication among Path Classifier's Instances.
"""
log = conf.get_logger("icom", conf.log_intracom)

RCV_BUFF_SIZE = 1024

isock = None

def init_intra_sock():
    # Prepare to send data via socket
    global isock

    isock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        log.error("Binding socket, wait...",)
        isock.bind((conf.cluster["our_private_ip"], conf.cluster["pc_intra_com_port"]))
    except socket.error:
        log.error("Failed to bound Socket to [%s:%i]",
            conf.cluster["our_private_ip"], conf.cluster["pc_intra_com_port"])
        assert False

    isock.setblocking(False)

    log.info("Socket bound to [%s:%i]",
        conf.cluster["our_private_ip"], conf.cluster["pc_intra_com_port"])


def store_new_paths_by_src(paths_dic, new_path):

    if new_path.get_src_ip() in paths_dic:
        paths_dic[new_path.get_src_ip()].append(new_path)
    else:
        paths_dic[new_path.get_src_ip()] = [new_path]
    return paths_dic



# TODO: set protocol to HIGHEST_PROTOCOL
def recv_reverse_traces():
    global isock
    new_rvrs_paths_dic = {}
    while True:  # rcv until there is something to receive
        try:
            data, _ = isock.recvfrom(RCV_BUFF_SIZE)
            rcv_len = len(data)

            rp = pickle.loads(data) # load into reverse path object
            log.debug("Rcvd from: [src: %15s][pid: %3i][bytes: %4i]",
                rp.get_src_ip(), rp.pid, rcv_len)
            new_rvrs_paths_dic = store_new_paths_by_src(new_rvrs_paths_dic, rp)

        except socket.error:
            break # this is ok, run out of stuff to read
        except TypeError as e:
            log.warning("TypeError in intracom[%s]", e)
        except EOFError as e:
            log.warning("EOFError in intracom[%s] [RCV_BUFF_SIZE(%i)-rcv_len(%i)] ",
                e, RCV_BUFF_SIZE, rcv_len)
    return new_rvrs_paths_dic


def distribute_our_fward_paths(nps_dic):

    for dst_ip, nps in nps_dic.iteritems():
        for np in nps:
            assert dst_ip == np.get_dst_ip()
            _send_npath_to(np, np.get_dst_ip())



def _send_npath_to(np, dst_ip):
    global isock

    data = pickle.dumps(np, protocol=pickle.HIGHEST_PROTOCOL)
    isock.sendto(data, (dst_ip, conf.cluster["pc_intra_com_port"]))               
    log.debug("Sent to:   [src: %15s][pid: %3i]", dst_ip, np.pid)


