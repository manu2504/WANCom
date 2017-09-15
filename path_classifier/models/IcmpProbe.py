#!/usr/bin/python

class IcmpProbe():

    def __init__(self, src_ip, dst_ip, hop_ip, rcv_time_ns, hop_id):

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.hop_ip = hop_ip
        self.rcv_time_ns = rcv_time_ns
        self.hop_id = hop_id

    def __str__(self):
        return "{} {} {} {} {}".format(
            self.src_ip, self.dst_ip, self.hop_ip, self.rcv_time_ns, self.hop_id)
