# @Author: Lorenzo Corneo
# @Date:   2016-10-06T10:11:25+02:00
# @Email:  lorenzo.corneo@gmail.com
# @Last modified by:   lorenzocorneo
# @Last modified time: 2016-10-28T15:04:05+02:00

#!/usr/bin/python

import MySQLdb
import itertools
import config
from collections import defaultdict
from models.EndNode import EndNode
from models.Measurement import Measurement
from models.HopMeasurement import HopMeasurement
from models.Path import Path

dup_log = config.get_logger("duplicates", config.log_patch_with_duplicates)

dbname = config.db_credentials["db"]
GET_NODES_QUERY = "SELECT * FROM {}.EndNodes".format(dbname)
GET_TRACEDIRECTIONS_QUERY = "SELECT * FROM {}.TraceDirections".format(dbname)
GET_PATHS_QUERY = "SELECT * FROM {}.Paths".format(dbname)
GET_HOPS_QUERY = "SELECT * FROM {}.Hops".format(dbname)
GET_MEASUREMENTS_QUERY = "SELECT * FROM {}.Measurements".format(dbname)
GET_HOPMEASUREMENTS_QUERY = "SELECT * FROM {}.HopMeasurements".format(dbname)
INSERT_ENDNODE_QUERY = "INSERT INTO {}.EndNodes (ip, name) VALUES ('%s', '%s');".format(dbname)
UPDATE_ENDNODE_QUERY = "UPDATE {}.EndNodes set ip='%s', name='%s' where idNode = %s;".format(dbname)
INSERT_TRACEDIRECTION_QUERY = "INSERT INTO {}.TraceDirections (idSrc, idDst) VALUES (%s, %s);".format(dbname)
INSERT_PATH_QUERY  = "INSERT INTO {}.Paths (idTraceDirection) VALUES (%s);".format(dbname)
INSERT_HOP_QUERY  = "INSERT INTO {}.Hops (idPath, ipSrc, ipDst, idPredecessor) VALUES (%s, '%s', '%s', %s);".format(dbname)
INSERT_MEASUREMENT_QUERY = "INSERT INTO {}.Measurements (idPath, rtt_ns, owd_forward_ns, owd_reverse_ns, timestamp_ns, pair) VALUES (%s, %s, %s, %s, %s, %s);".format(dbname)
INSERT_HOPMEASUREMENT_QUERY = "INSERT INTO {}.HopMeasurements (ipSrc, ipDst, rtt_ns, measurementTimestamp) VALUES (%s, %s, %s, %s);".format(dbname)

class RawDataManager:
    """This class provides basic functionality for database managment and
    retrieving raw data, as well as inserting new records."""
    def __init__(self):
        self.connection = self._connect(**config.db_credentials)

    def _connect(self, host='', user='', passwd='', db=''):
        return MySQLdb.connect(host, user, passwd, db)

    def getEndNodes(self):
        cur = self.connection.cursor()
        cur.execute(GET_NODES_QUERY)
        return cur.fetchall()

    def getTraceDirections(self):
        cur = self.connection.cursor()
        cur.execute(GET_TRACEDIRECTIONS_QUERY)
        return cur.fetchall()

    def getPaths(self):
        cur = self.connection.cursor()
        cur.execute(GET_PATHS_QUERY)
        return cur.fetchall()

    def getHops(self):
        cur = self.connection.cursor()
        cur.execute(GET_HOPS_QUERY)
        return cur.fetchall()

    def getMeasurements(self):
        cur = self.connection.cursor()
        cur.execute(GET_MEASUREMENTS_QUERY)
        return cur.fetchall()

    def getHopMeasurements(self):
        cur = self.connection.cursor()
        cur.execute(GET_HOPMEASUREMENTS_QUERY)
        return cur.fetchall()

    def insertEndNode(self, ip, name):
        cur = self.connection.cursor()
        cur.execute(INSERT_ENDNODE_QUERY % (ip, name))
        self.connection.commit()
        return cur.lastrowid

    def updateEndNode(self, idNode, ip, name):
        cur = self.connection.cursor()
        cur.execute(UPDATE_ENDNODE_QUERY % (ip, name, idNode))
        self.connection.commit()

    # TEST: OK
    # EX: insertTraceDirection(1, 4)
    def insertTraceDirection(self, idSrc, idDst):
        cur = self.connection.cursor()
        cur.execute(INSERT_TRACEDIRECTION_QUERY % (idSrc, idDst))
        self.connection.commit()
        return cur.lastrowid

    # TEST: OK
    # EX: insertPath(1, [('192.168.0.4', '192.168.0.5'), ('192.168.0.5', '192.168.0.6')])
    # NOTE: This function is not atomic. It may commit the new path but not the hops.
    # hops is a list of tuples with the ip of source and destination.
    def insertPath(self, idTraceDirection, hops):
        cur = self.connection.cursor()
        # Insert path
        cur.execute(INSERT_PATH_QUERY % idTraceDirection)
        self.connection.commit()
        idPath = cur.lastrowid
        # No predecessor for the root.
        predecessor_id = "NULL"
        # # Insert the hops between a path
        for h in hops:
            predecessor_id = self.insertHop(idPath, h[0], h[1], predecessor_id)
        return idPath

    # TEST: OK
    def insertHop(self, idPath, idSrc, idDst, idPredecessor="NULL"):
        cur = self.connection.cursor()
        # print INSERT_HOP_QUERY % (idPath, idSrc, idDst, idPredecessor)
        cur.execute(INSERT_HOP_QUERY % (idPath, idSrc, idDst, idPredecessor))
        self.connection.commit()
        return cur.lastrowid

    # TEST: OK
    def insertMeasurement(self, idPath, rtt_ns, owd_forward_ns, owd_reverse_ns, timestamp_ns="NULL", pair="NULL"):
        cur = self.connection.cursor()
        cur.execute(INSERT_MEASUREMENT_QUERY % (idPath, rtt_ns, owd_forward_ns, owd_reverse_ns, timestamp_ns, pair))
        self.connection.commit()
        return cur.lastrowid

    # TEST: OK
    def insertMeasurements(self, listOfMeasurements):
		try:
			cur = self.connection.cursor()
			cur.executemany(INSERT_MEASUREMENT_QUERY, listOfMeasurements)
			self.connection.commit()
		except MySQLdb.IntegrityError:
			dup_log.info("there was an integrity error")
			dup_log.info(listOfMeasurements)
		except MySQLdb.DataError:
			dup_log.info("RTT_NS is out of range")
			dup_log.info(listOfMeasurements)

    # TEST: OK
    def insertHopMeasurements(self, hopMeasurements):
        try:
            cur = self.connection.cursor()
            cur.executemany(INSERT_HOPMEASUREMENT_QUERY, hopMeasurements)
            self.connection.commit()
        except MySQLdb.IntegrityError:
        	dup_log.info("there was an integrity error")
        	dup_log.info(hopMeasurements)

class IdElementDataManager:
    def __init__(self, list):
        self.list = list

    def getElementById(self, id):
        r = filter(lambda x: x.id == id, self.list)
        return (r[:1] or [None])[0]

    def getElementsByAttribute(self, attribute, value):
        try:
            return filter(lambda x: x.__dict__[attribute] == value, self.list)
        except:
            return None

    def getElementByAttribute(self, attribute, value):
        r = self.getElementsByAttribute(attribute, value)
        if r == None: return None
        else: return r[0]

    def getAll(self):
        return self.list

class EndNodeDataManager(IdElementDataManager):
    def __init__(self, rdm):
        IdElementDataManager.__init__(self, [])
        self.rdm = rdm
        self.init()

    # update nodes at startup

    def init(self):
        self.list =  map(lambda x: EndNode(x[1], name = x[2], id = x[0]), list(self.rdm.getEndNodes()))

    def add(self, node):
        # check if the ip is already there, if yes, raise an exception
        node.id = self.rdm.insertEndNode(node.ip, node.name)
        self.list = self.list + [node]


    def update(self, node):
        self.rdm.updateEndNode(node.id, node.ip, node.name)

        self.getElementById(node.id).ip = node.ip
        self.getElementById(node.id).name = node.name


    def updateMany(self, nodes): pass

    def getEndNodeByIp(self, target_ip):
        end_node = filter(lambda x: x.ip == target_ip, self.list)
        assert len(end_node) == 1
        return end_node[0]

class PathDataManager(IdElementDataManager):
    def __init__(self, rdm, ndm):
        IdElementDataManager.__init__(self, [])
        self.rdm = rdm
        self.ndm = ndm
        self.init()

    def init(self):
        self._endnodes = self.ndm.getAll()
        self._hops = list(self.rdm.getHops())
        self._traceDirRaw = list(self.rdm.getTraceDirections())
        self._paths = list(self.rdm.getPaths())
        self.pid2hops = {}
        colnum_ipSrc = 2
        colnum_ipDst = 3
        col_pid = 1
        col_hid = 0

        # Presort list of hops by pid, to group ranges of pids together
        self._hops = sorted(self._hops, key=lambda  h: h[col_pid])
        for key, group in itertools.groupby(self._hops, lambda x: x[col_pid]):
            # Sort list of hops where pid==key by hop id to guarantee proper order
            group_list = sorted(list(group), key=lambda h: h[col_hid])

            hops_chain = list(itertools.chain(
                *map(lambda y: (y[colnum_ipSrc], y[colnum_ipDst]), group_list)
                ))

            hops_chain = map(lambda n: n,
                [ip for i, ip in enumerate(hops_chain) if (i == 0 or i%2 == 1)])

            self.pid2hops[key] = hops_chain

        # OBS: If there are only two hops, that is a trace direction and the id is the
        # unique identifier of that!
        self.list = map(lambda x: Path(hops = [self.getTraceDirectionById(x[1])['ipSrc']] +
            self.getHopsByPathId(x[0]) + [self.getTraceDirectionById(x[1])['ipDst']], measurements=[],
                id = x[0], idTraceDirection = x[1]), self._paths)
        self.traces = map(lambda x: Path(hops = [self.getTraceDirectionById(x[0])['ipSrc']] +
            [self.getTraceDirectionById(x[0])['ipDst']], id=x[0]), self._traceDirRaw)

        self.pid2Path = {}
        for p in self.list:
            # print "ID -> ", id(p), p.id, id(p.measurements)
            self.pid2Path[p.id] = p

        del self._endnodes
        del self._hops
        del self._traceDirRaw
        del self._paths

    def add(self, path):
        td_id = self.getTraceDirectionByIps(path.source(), path.destination())
        if not td_id:
            assert False

        path.id = self.rdm.insertPath(
            td_id, self._fromListToTuplesHops(path.hops[1:len(path.hops) - 1]))

        self.addToMemory(path)

        # return the new path instance.
        return path

    def addToMemory(self, path):
        assert path.id # has to be pre-set!

        self.list += [path]
        return path


    def getTraceDirectionByIps(self, ipSrc, ipDst):
        print rdm.getTraceDirections()
        return [ x[0] for x in rdm.getTraceDirections()
            if x[1]==self.ndm.getElementByAttribute("ip", ipSrc).id and
               x[2]==self.ndm.getElementByAttribute("ip", ipDst).id
            ][0]



    # path must be a models.Path instance!
    def pathExists(self, path):
        for p in self.list:
            if p == path: return p
        return None

    def _fromListToTuplesHops(self, list):
        listOfTuples = []
        for i in range(1, len(list), 1):
            listOfTuples.append((list[i-1], list[i]))
        return listOfTuples

    def _fromRawToTraceDirection(self, raw):
        return {'id': raw[0], 'ipSrc': self.ndm.getElementById(raw[1]).ip, 'ipDst': self.ndm.getElementById(raw[2]).ip}

    def getTraceDirectionById(self, id):
        r = [self._fromRawToTraceDirection(x) for x in self._traceDirRaw if x[0] == id]
        return (r[:1] or [None])[0]

    def getTraceDirectionByPathId(self, id):
        r = [self.getTraceDirectionById(x[1]) for x in self._paths if x[0] == id]
        return (r[:1] or [None])[0]

    # Return all the intermediate hops for a path.
    def getHopsByPathId(self, id):
        if self.getTraceDirectionByPathId(id) == None:
            return None
        return self.pid2hops[id]
        # colnum_idPath = 1
        # colnum_ipSrc = 2
        # colnum_ipDst = 3
        # hops_chain = list(itertools.chain(
        #     *map(lambda y: (y[colnum_ipSrc], y[colnum_ipDst]),
        #         filter(lambda z: id == z[colnum_idPath], self._hops)))
        # )
        # return map(lambda n: n,
        #     [ip for i, ip in enumerate(hops_chain) if (i == 0 or i%2 == 1)])

class MeasurementDataManager(IdElementDataManager):
    def __init__(self, rdm):
        IdElementDataManager.__init__(self, [])
        self.rdm = rdm
        self.list = map(lambda x: Measurement(
            rtt_ns=x[2],
            owd_forward_ns=x[3],
            owd_reverse_ns=x[4],
            timestamp_ns=x[5],
            pair=x[6],
            idPath=x[1]
            ),
        rdm.getMeasurements())

    def addMany(self, measurements):
        rdm.insertMeasurements(tuple(map(lambda x: (x.idPath, x.rtt_ns, x.owd_forward_ns, x.owd_reverse_ns, x.timestamp_ns, x.pair_timestamp), measurements)))

class HopMeasurementDataManager(IdElementDataManager):
    def __init__(self, rdm):
        self.rdm = rdm
        self.list = map(lambda x: HopMeasurement(_id=x[0], ipSrc=x[1],
            ipDst=x[2], idMeasurement=x[4], rtt=x[3]), rdm.getHopMeasurements())
        self.dict = defaultdict(list)
        for i in self.list:
            self.dict[i.idMeasurement].append(i)

    def addMany(self, hopMeasurements):
        self.rdm.insertHopMeasurements(tuple(map(lambda x: (x.ipSrc, x.ipDst, x.rtt, x.idMeasurement), hopMeasurements)))

class DataManager2:
    def __init__(self, ndm, pdm, mdm):
        self.ndm = ndm
        self.pdm = pdm
        self.mdm = mdm
        self.init()

    def init(self):
        self.endnodes = self.ndm.getAll()
        self.paths = self.pdm.getAll()

        for m in self.mdm.list:
            self.pdm.pid2Path[m.idPath].measurements.append(m)

import time
start = time.time()

def getTime():
    return time.time() - start

print "Start  ", getTime()
rdm = RawDataManager()
print "End Raw   %0.3f" % getTime()

ndm = EndNodeDataManager(rdm)
print "End EndNode   %0.3f" % getTime()


pdm = PathDataManager(rdm, ndm)
print "End Path   %0.3f" % getTime()

hdm = HopMeasurementDataManager(rdm)
print "End HopMeasurement   %0.3f" % getTime()

mdm = MeasurementDataManager(rdm)
print "End Meas   %0.3f" % getTime()


dm = DataManager2(ndm, pdm, mdm)
print "End Manager2   %0.3f" % getTime()
