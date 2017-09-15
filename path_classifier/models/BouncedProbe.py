#!/usr/bin/python

class BouncedProbe():

    def __init__(self, src_ip, dst_ip, bounce_time_ns, rcv_time_ns, hop_id):

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.bounce_time_ns = bounce_time_ns
        self.rcv_time_ns = rcv_time_ns
        self.hop_id = hop_id

    def __str__(self):
        return "{} {} {} {} {}".format(
            self.src_ip, self.dst_ip, self.bounce_time_ns, self.rcv_time_ns, self.hop_id)
