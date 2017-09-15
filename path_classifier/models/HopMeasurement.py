class HopMeasurement:
    def __init__(self, _id=None, ipSrc=None, ipDst=None, idMeasurement=None, rtt=None):
        self.ipSrc = ipSrc
        self.ipDst = ipDst
        self.idMeasurement = idMeasurement
        self.rtt = rtt

    def __eq__(self, x):
        return self.ipSrc == x.ipSrc and self.ipDst == x.ipDst and self.idMeasurement == x.idMeasurement and self.rtt == x.rtt

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)
