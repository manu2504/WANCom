#!/usr/bin/python

class EndNode:
    def __init__(self, ip, name="", id=None):
        self.id = id
        self.ip = ip
        self.name = name


    def __eq__(self, y):
        return self.ip == y.ip and self.name == y.name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)
