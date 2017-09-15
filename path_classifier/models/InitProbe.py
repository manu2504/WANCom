#!/usr/bin/python

class InitProbe():

    def __init__(self, src_ip, dst_ip, trace_tcp_seq_id, send_time_ns):

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.trace_tcp_seq_id = trace_tcp_seq_id
        self.send_time_ns = send_time_ns

    def __str__(self):
        return "{} {} {} {}".format(
            self.src_ip, self.dst_ip, self.trace_tcp_seq_id, self.send_time_ns)
