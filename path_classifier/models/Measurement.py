class Measurement:
    def __init__(self, rtt_ns, owd_forward_ns, owd_reverse_ns, timestamp_ns, pair=None, idPath=None):
        self.idPath = idPath
        self.rtt_ns = rtt_ns
        self.owd_forward_ns = owd_forward_ns
        self.owd_reverse_ns = owd_reverse_ns        
        self.timestamp_ns = timestamp_ns
        self.pair_timestamp = pair
        
        

    def __eq__(self, x):
        return self.timestamp == x.timestamp and self.rtt_ns == x.rtt_ns

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)
