class Path:
    def __init__(self, hops=[], measurements=[], id=None, idTraceDirection=None):
        self.id = id
        self.idTraceDirection = idTraceDirection
        self.hops = hops
        self.measurements = measurements

        # TODO: make hops immutable, so we dont have to recompute hash for every compare
        self._hash = hash("".join(self.hops))

    def source(self):
        return self.hops[0]

    def destination(self):
        return self.hops[-1]

    def addMeasurement(self, m):
        self.measurements = self.measurements + [m]

    def __eq__(self, x):
        return hash("".join(self.hops)) == hash("".join(x.hops))

    def __hash__(self):
        return hash("".join(self.hops))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)

    def str_short(self):
        # for shortness we print only last digit of each path
        # for quick visual inspection, to print use self.tostr()

        ips_processed = []
        for ip in self.hops:
            ip_split = ip.split(".")
            if len(ip_split) == 4:
                ips_processed.append(ip_split[3])
            else: # Dealing with "*"
                ips_processed.append(ip)
        return ".".join(ips_processed)


    def str_full(self):
        buff = ""
        for ip in self.hops:
            buff += "%14s " % ip

        return "[#: %i]" % len(self.measurements) + buff

    # TODO: May want to check the uniqueness of the measurement when adding a new one
