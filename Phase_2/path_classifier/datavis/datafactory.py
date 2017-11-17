#!/usr/bin/python
from __future__ import division
import logging

from collections import defaultdict

from viscommon import *



# from dao import *

logging.basicConfig(format="(%(funcName).20s):[%(lineno)4d] %(asctime)s %(levelname)4s| %(message)s",
    datefmt='%H:%M:%S', level=logging.DEBUG)


class PairedMeasurementsContainer(object): # PMC/pmc for short
    def __init__(self, path_pair_ids, plot_name,
        frwd_msrmnts_tspairs, rvrs_msrmnts_tspairs):
        self.path_pair_ids = path_pair_ids
        self.plot_name = plot_name

        # (Rtt, timestamp_ns) pairs
        self.frwd_msrmnts_tspairs = frwd_msrmnts_tspairs
        self.rvrs_msrmnts_tspairs = rvrs_msrmnts_tspairs

    def __str__(self):
        print "%s %s %s %s" % (self.path_pair_ids, self.plot_name,
            self.frwd_msrmnts_tspairs, self.rvrs_msrmnts_tspairs)

    def get_frwd_rtts(self):
        return [x[0] for x in self.frwd_msrmnts_tspairs]

    def get_rvrs_rtts(self):
        return [x[0] for x in self.rvrs_msrmnts_tspairs]

    def sort_measurements_by_timestamp_ns(self):
        """ Sort by Timestamp just in case if values in db are not sequential"""
        self.frwd_msrmnts_tspairs = sorted(self.frwd_msrmnts_tspairs, key=lambda x :x[1])
        self.rvrs_msrmnts_tspairs = sorted(self.rvrs_msrmnts_tspairs, key=lambda x :x[1])



def getMeasurementsByTraceDirectionId(dm, id):
    td = filter(lambda x: x.id == id, dm.pdm.traces)[0]

    paths = filter(lambda x: x.source() == td.source() and
        x.destination() == td.destination(), dm.pdm.list)
    m1 = map(lambda y: y.measurements, paths)
    m2 = [val for sublist in m1 for val in sublist]
    return sorted(m2, key=lambda x: x.timestamp_ns)

# Return {(idTraceDirectionSrc, idTraceDirectionDst): [(idPathSrc, idPathDst), [x, y, z]...]...}
#  Specify whether get forward or return RTT.
def getPathPairs(dm):
    """
    Returns a dictionary key=idTraceDirection,
                       value=pair(forward path id, return path id, [list of frwrd rtts])
    """
    all_msrmnts_dic = {}
    paired_measurment_tuples = []
    tpm = defaultdict(list)
    ret = defaultdict(list)

    # <1.> get all measurements in one big dic
    for m in dm.mdm.list:
        all_msrmnts_dic[m.timestamp_ns] = m

    # <2.> iterate over the list all mes and find pairs by looking at the pair ts field
    for _, mesrmnt in all_msrmnts_dic.iteritems():

        #print mesrmnt
        #print "---", mesrmnt.pair_timestamp
        # print all_msrmnts_dic.keys()
        # if measurement has a pair,
        if mesrmnt.pair_timestamp and mesrmnt.pair_timestamp in all_msrmnts_dic:

            paired_measurment_tuples.append( (
                (mesrmnt.idPath, all_msrmnts_dic[mesrmnt.pair_timestamp].idPath), #frwd/revr pids
                mesrmnt.rtt_ns,                                                   #frwd.rtt
                mesrmnt.timestamp_ns,                                             #frwd.timestamp_ns

                all_msrmnts_dic[mesrmnt.pair_timestamp].rtt_ns,                             #revr.rtt
                all_msrmnts_dic[mesrmnt.pair_timestamp].timestamp_ns                        #rvrs.timestamp_ns
                ) )


    # <3.> group paired measurements by pids into dic
    for pmt in paired_measurment_tuples:

        pp_ids = pmt[0]

        if pp_ids not in tpm:
            tpm[pp_ids] = PairedMeasurementsContainer(
                path_pair_ids=pp_ids,
                plot_name=path2plot_name(
                    dm,
                    dm.pdm.pid2Path[pp_ids[0]]
                    ), # we use [0] the frwd pid for plot name
                frwd_msrmnts_tspairs=[], rvrs_msrmnts_tspairs=[]
                )

        if pp_ids in tpm:
            tpm[pp_ids].frwd_msrmnts_tspairs.append( (pmt[1], pmt[2]) )
            tpm[pp_ids].rvrs_msrmnts_tspairs.append( (pmt[3], pmt[4]) )


    # <4.> group lists of paired measurements by tracedir into a dic
    for pp_ids, pms_con in tpm.iteritems():
        tdid = dm.pdm.pid2Path[pms_con.path_pair_ids[0]].idTraceDirection
        ret[tdid].append(pms_con)



    # Print some stats
    for tdid, pairs in ret.iteritems():

        pairs = sorted(pairs, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)
        most_popular_pairs = []
        for i, p in enumerate(pairs):
            most_popular_pairs.append(len(p.frwd_msrmnts_tspairs))
            if i > 10:
                break

        print "[{direction}] Unique pairs [{pairs_count:4d}] top_by_count: {top_pairs}".format(
            direction=pairs[0].plot_name,
            pairs_count=len(pairs),
            top_pairs=most_popular_pairs)


    return ret


def getSmoothedPathPairs(dm):
    """
    Returns a dictionary key=idTraceDirection,
                       value=pair(forward path id, return path id, [list of frwrd rtts])
    """
    all_msrmnts_dic = {}
    paired_measurment_tuples = []
    tpm = defaultdict(list)
    ret = defaultdict(list)
    smoothed_paired_msmnts_dic = defaultdict(list)
    smoothed_paired_measurements_tuples = []

    # <1.> get all measurements in one big dic
    for m in dm.mdm.list:
        all_msrmnts_dic[m.timestamp_ns] = m

    # <2.> iterate over the list all mes and find pairs by looking at the pair ts field
    for _, mesrmnt in all_msrmnts_dic.iteritems():

        #print mesrmnt
        #print "---", mesrmnt.pair_timestamp
        # print all_msrmnts_dic.keys()
        # if measurement has a pair,
        if mesrmnt.pair_timestamp and mesrmnt.pair_timestamp in all_msrmnts_dic:

            paired_measurment_tuples.append( (
                (mesrmnt.idPath, all_msrmnts_dic[mesrmnt.pair_timestamp].idPath), #frwd/revr pids
                mesrmnt.rtt_ns,                                                   #frwd.rtt
                mesrmnt.timestamp_ns,                                             #frwd.timestamp_ns

                all_msrmnts_dic[mesrmnt.pair_timestamp].rtt_ns,                             #revr.rtt
                all_msrmnts_dic[mesrmnt.pair_timestamp].timestamp_ns                        #rvrs.timestamp_ns
                ) )



    paired_measurment_tuples = sorted(paired_measurment_tuples,key=lambda x: x[2],reverse=False)

    for pmt in paired_measurment_tuples:
        tdid = dm.pdm.pid2Path[pmt[0][0]].idTraceDirection
        smoothed_paired_msmnts_dic[tdid].append(pmt)


    smoothed_paired_measurements_list = []
    for td, pmts in smoothed_paired_msmnts_dic.iteritems():
        pmts = sorted(pmts, key=lambda t : t[2],reverse=False)
        previous = pmts[0]
        count = -1
        for index,m in enumerate(pmts):
            count = count + 1
            if m[0] != previous[0] or count == 5:
                lowerrange = index - count
                upperrange = index
                minFrwdMeasurement = min(pmts[lowerrange:upperrange], key=lambda x: x[1])
                minRvsMeasurement = min(pmts[lowerrange:upperrange], key=lambda x: x[3])
                entry = (minFrwdMeasurement[0],
                minFrwdMeasurement[1],minFrwdMeasurement[2],minRvsMeasurement[3],minRvsMeasurement[4]
                )
                for i in range(0,count):
                    smoothed_paired_measurements_list.append(entry)
                previous = m
                count = 0
            #elif count == 5:
            #    lowerrange = index - count
            #    upperrange = index
            #    minFrwdMeasurement = min(pmts[lowerrange:upperrange], key=lambda x: x[1])
            #    minRvsMeasurement = min(pmts[lowerrange:upperrange], key=lambda x: x[3])
            #    smoothed_paired_measurements_list.append((minFrwdMeasurement[0],
            #    minFrwdMeasurement[1],minFrwdMeasurement[2],minRvsMeasurement[3],minRvsMeasurement[4]
            #    )
            #    )
            #    count = 0
            #    if td == 40:
            #        print "same"
            elif m[0] == previous[0] and count != 5:
                continue

    # <3.> group paired measurements by pids into dic
    for pmt in smoothed_paired_measurements_list:

        pp_ids = pmt[0]

        if pp_ids not in tpm:
            tpm[pp_ids] = PairedMeasurementsContainer(
                path_pair_ids=pp_ids,
                plot_name=path2plot_name(
                    dm,
                    dm.pdm.pid2Path[pp_ids[0]]
                    ), # we use [0] the frwd pid for plot name
                frwd_msrmnts_tspairs=[], rvrs_msrmnts_tspairs=[]
                )

        if pp_ids in tpm:
            tpm[pp_ids].frwd_msrmnts_tspairs.append( (pmt[1], pmt[2]) )
            tpm[pp_ids].rvrs_msrmnts_tspairs.append( (pmt[3], pmt[4]) )

    # <4.> group lists of paired measurements by tracedir into a dic
    for pp_ids, pms_con in tpm.iteritems():
        tdid = dm.pdm.pid2Path[pms_con.path_pair_ids[0]].idTraceDirection
        ret[tdid].append(pms_con)



    # Print some stats
    for tdid, pairs in ret.iteritems():

        pairs = sorted(pairs, key=lambda t : len(t.frwd_msrmnts_tspairs), reverse=True)
        most_popular_pairs = []
        for i, p in enumerate(pairs):
            most_popular_pairs.append(len(p.frwd_msrmnts_tspairs))
            if i > 10:
                break

        print "[{direction}] Unique pairs [{pairs_count:4d}] top_by_count: {top_pairs}".format(
            direction=pairs[0].plot_name,
            pairs_count=len(pairs),
            top_pairs=most_popular_pairs)


    return ret


def getHopMeasurementsForPathPairs(dm,hdm):
    r = getPathPairs(dm)
    for tdid, pairs in r.iteritems():
        for pair in pairs:
            frwdPath = pair.path_pair_ids[0]
            reversePath = pair.path_pair_ids[1]
            updated_frwd_msrmnts_tspairs = []
            updated_rvrs_msrmnts_tspairs = []
            for fwdMeasurement in pair.frwd_msrmnts_tspairs:
                print fwdMeasurement
                hopMeasurements = [x for x in hdm.list if x.idMeasurement == fwdMeasurement[1]]
                updated_frwd_msrmnts_tspairs.append((fwdMeasurement,hopMeasurements))
            for rvrsMeasurement in pair.rvrs_msrmnts_tspairs:
                hopMeasurements = [x for x in hdm.list if x.idMeasurement == rvrsMeasurement[1]]
                updated_rvrs_msrmnts_tspairs.append((rvrsMeasurement,hopMeasurements))
            pair.frwd_msrmnts_tspairs = updated_frwd_msrmnts_tspairs
            pair.rvrs_msrmnts_tspairs = updated_rvrs_msrmnts_tspairs

    return r

############################################################################################################


def find_desired_hop(hops):
    last_star = 0
    found_star = False
    for hop in hops:
        if hop == '*':
            found_star = True
        elif found_star:
            desired_hop = hop
            break
    return (desired_hop,hops.index(desired_hop))


def find_first_hop_before_star(hops):
        first_star_index = hops.index('*')
        return (hops[first_star_index-1],first_star_index-1)

def find_pathHops_byID(dm,idPath):
    path_hops = [x.hops for x in dm.pdm.list if x.id == idPath]
    if path_hops:
        return path_hops[0]
    else:
        return None

def getHopMeasurementsByTimeStamp(hdm,timestamp_ns):
    hdmByTS_list = [x for x in hdm.list if x.idMeasurement == timestamp_ns]
    return hdmByTS_list

def getHopMeasurementsByDst(hdmlist,dst_ip):
    hsm_measurements_list = [x for x in hdmlist if x.ipDst == dst_ip]
    return hsm_measurements_list

def getHopMeasurements(dm,pmc):
    frwdMsmnts = []
    rvrsMsmnts = []
    idFrwdPath = pmc.path_pair_ids[0]
    idRvrsPath = pmc.path_pair_ids[1]
    frwrdHops = find_pathHops_byID(dm,idFrwdPath)
    rvrsHops = find_pathHops_byID(dm,idRvrsPath)

    print frwrdHops
    print rvrsHops

    frwdFirstHopAfterStar = find_desired_hop(frwrdHops)[0]
    rvrsFirstHopAfterStar = find_desired_hop(rvrsHops)[0]

    print frwdFirstHopAfterStar
    print rvrsFirstHopAfterStar

    print pmc.frwd_msrmnts_tspairs[0]
    print pmc.frwd_msrmnts_tspairs[1]

    frwdHopMeasurements = [x for y in pmc.frwd_msrmnts_tspairs for x in y[1] if x.ipDst == frwdFirstHopAfterStar]
    rvrsHopMeasurements = [x for y in pmc.rvrs_msrmnts_tspairs for x in y[1] if x.ipDst == rvrsFirstHopAfterStar]
    return (frwdHopMeasurements,rvrsHopMeasurements)

############################################################################################################

def getAllPathPairsNormalized(dm):
    nonNormalizedPathPairs = getPathPairs(dm)
    normalizedPathPairsCombined = defaultdict(list)
    for tdid, pairs in nonNormalizedPathPairs.iteritems():
        allFwdMeasurementsPerTd = []
        allRvsMeasurementsPerTd = []

        plot_name = pairs[0].plot_name

        for pathPair in pairs:

            pathPairMinFwdRtt = pathPair.frwd_msrmnts_tspairs[0][0]
            pathPairMinRvsRtt = pathPair.rvrs_msrmnts_tspairs[0][0]

            for msmt in pathPair.frwd_msrmnts_tspairs:
                if msmt[0] < pathPairMinFwdRtt:
                    pathPairMinFwdRtt = msmt[0]

            for msmt in pathPair.rvrs_msrmnts_tspairs:
                if msmt[0] < pathPairMinRvsRtt:
                    pathPairMinRvsRtt = msmt[0]


            pathPair.frwd_msrmnts_tspairs[:] = [(float(x[0]) / float(pathPairMinFwdRtt),x[1]) for x in pathPair.frwd_msrmnts_tspairs]
            pathPair.rvrs_msrmnts_tspairs[:] = [(float(x[0]) / float(pathPairMinRvsRtt),x[1]) for x in pathPair.rvrs_msrmnts_tspairs]

            allFwdMeasurementsPerTd = allFwdMeasurementsPerTd + pathPair.frwd_msrmnts_tspairs
            allRvsMeasurementsPerTd = allRvsMeasurementsPerTd + pathPair.rvrs_msrmnts_tspairs


        normalizedPathPairsCombined[tdid] = ((allFwdMeasurementsPerTd,allRvsMeasurementsPerTd),plot_name)
    return normalizedPathPairsCombined

def generateRttVsTimeData(dm):
    """
    Generates data file for each trace direction with all (measurement, ts)
    sorted by timestamp_ns.
    """
    ret_tuples = []
    for td in dm.pdm.traces:
        paths = filter(lambda x: x.source() == td.source() and
            x.destination() == td.destination(), dm.pdm.list)
        m1 = map(lambda y: y.measurements, paths)
        m2 = [val for sublist in m1 for val in sublist]
        path_measurements = sorted(
            map(lambda x: (x.timestamp_ns, x.rtt_ns), m2),
            key=lambda x: x[0]
            )

        plot_name = tracedirection2plot_name(dm, td)

        ret_tuples.append( (plot_name, path_measurements) )
    return ret_tuples

def generateSmoothedRttVsTimeData(dm):
    #ret_tuples = []
    ret_dic = defaultdict(list)

    for td in dm.pdm.traces:
        # Trace direction measurements, sorted by time.
        tdm = getMeasurementsByTraceDirectionId(dm, td.id)
        tdm = sorted(tdm, key=lambda t : t.timestamp_ns,reverse=False)

        previous = tdm[0]
        pathsLifeTime = []

        count = -1
        for index,m in enumerate(tdm):
            count = count + 1
            if m.idPath != previous.idPath :
                lowerrange = index - count
                upperrange = index
                minMeasurement = min(tdm[lowerrange:upperrange], key=lambda x: x.rtt_ns)
                pathsLifeTime.append(minMeasurement)
                previous = m
                count = 0
            elif count == 5:
                lowerrange = index - count
                upperrange = index
                minMeasurement = min(tdm[lowerrange:upperrange], key=lambda x: x.rtt_ns)
                pathsLifeTime.append(minMeasurement)
                count = 0
            elif m.idPath == previous.idPath and count != 5:
                continue

        #path_measurements = sorted(
        #    map(lambda x: (x.timestamp_ns, x.rtt_ns), pathsLifeTime),
        #    key=lambda x: x[0]
        #    )

        #plot_name = tracedirection2plot_name(dm, td)
        #ret_tuples.append( (plot_name, path_measurements) )
        legend = "[%s]-[%s]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name
            )
        ret_dic[td] = (pathsLifeTime,legend)
    #return ret_tuples
    return ret_dic


def generateSmoothedPairsRttVsTimeData(dm):
    return None

def getNewPathFrequency(dm):
    """ Returns a list of tuples:
    tup[0] a list of timestamp_nss when new paths occurred
    tup[1] is a string containing regions of the tr dir
    tuo[2] the timestamp_ns of the last path sample on that trace direction"""
    ret_list = []
    existing_paths = []
    for td in dm.pdm.traces:
        # Trace direction measurements, sorted by time.
        tdm = getMeasurementsByTraceDirectionId(dm, td.id)
        previous = (tdm[0].timestamp_ns, tdm[0].idPath)
        new_paths_occurancies = [tdm[0].timestamp_ns]
        existing_paths.append(tdm[0].idPath)
        # Produces a list of the timestamp_ns when a different path was selected.
        for m in tdm:
            if m.idPath != previous[1] and m.idPath not in existing_paths:
                new_paths_occurancies.append(m.timestamp_ns)
                previous = (m.timestamp_ns, m.idPath)
                existing_paths.append(m.idPath)

        legend = "[%s]-[%s]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name
            )

        ret_list.append( (new_paths_occurancies, legend, m.timestamp_ns))

        print len(new_paths_occurancies)
        # break

    return ret_list




def print_unituq_paths4tracedir(dm, tid):
    # TODO: sample
    ll = []
    for p in  dm.pdm.list:
        if p.source() == "52.87.221.144" and p.destination() == "52.37.22.219":
           ll.append(p.str_short() +" -[" + str(len(p.measurements)) + "]- pid: " + str(p.id) + " hoplen: " + str(len(p.hops)))
    for l in sorted(ll):
        print l



def getUniquePathCount4tracedir(dm):
    """ Function returns a list of tuples where
    tup[0] is the number of unique paths on a given trace direction
    tup[1] is a string containing ips and the same number of unique paths on the tr dir"""

    res_tuples = []


    for td in dm.pdm.traces:
        paths = filter(lambda x: x.source() == td.source() and
            x.destination() == td.destination(), dm.pdm.list)
        legend = "[%s]-[%s]-[%i]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name,
            len(paths)
            )
        res_tuples.append((len(paths), legend))
    res_tuples = sorted(res_tuples, key=lambda tup: tup[0], reverse=True)

    return res_tuples


def generatePathVsLifetime(dm):
    ret_dic = defaultdict(list)
    for td in dm.pdm.traces:
        # Trace direction measurements, sorted by time.
        tdm = getMeasurementsByTraceDirectionId(dm, td.id)
        tdm = sorted(tdm, key=lambda t : t.timestamp_ns,reverse=False)

        previous = (tdm[0].timestamp_ns, tdm[0].idPath)
        pathsLifeTime = []
        # Produces a list of the timestamp_ns when a different path was selected.
        for m in tdm:
            if m.idPath != previous[1] :
                plot_name=path2plot_name(dm,dm.pdm.pid2Path[previous[1]])
                pathsLifeTime.append([previous[1], int(m.timestamp_ns - previous[0])/1000000000 ,plot_name])
                previous = (m.timestamp_ns, m.idPath)

        legend = "[%s]-[%s]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name
            )

        ret_dic[td] = (pathsLifeTime,legend)
    return ret_dic


def generateSummerizedPathVsLifetime(dm):
    ret_list = []
    for td in dm.pdm.traces:
        # Trace direction measurements, sorted by time.
        tdm = getMeasurementsByTraceDirectionId(dm, td.id)
        tdm = sorted(tdm, key=lambda t : t.timestamp_ns,reverse=False)
        previous = (tdm[0].timestamp_ns, tdm[0].idPath)
        pathsLifeTime = []
        # Produces a list of the timestamp_ns when a different path was selected.
        for m in tdm:
            if m.idPath != previous[1] :
                pathsLifeTime.append([previous[1], int(m.timestamp_ns - previous[0])/1000000000])
                previous = (m.timestamp_ns, m.idPath)

        # Group path times by timescales
        lessThan1Hour = 0
        between1Hand4H = 0
        moreThan4H = 0
        for pathlifetime in pathsLifeTime:
            if (pathlifetime[1] < 10):
                lessThan1Hour+= pathlifetime[1]
            elif (pathlifetime[1] > 10 and pathlifetime[1] < 1000):
                between1Hand4H+= pathlifetime[1]
            elif ( pathlifetime[1] > 10000 ):
                moreThan4H+= pathlifetime[1]

        print ("Minimum path lifetime was: %i", min(pathsLifeTime))
        legend = "[%s]-[%s]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name
            )

        ret_list.append( ([lessThan1Hour,between1Hand4H,moreThan4H], legend))

    return ret_list


def getPathsPrevalance(dm):
    ret_dic = defaultdict(list)
    for td in dm.pdm.traces:
        # Trace direction measurements, sorted by time.
        tdm = getMeasurementsByTraceDirectionId(dm, td.id)
        tdm = sorted(tdm, key=lambda t : t.timestamp_ns,reverse=False)

        previous = (tdm[0].timestamp_ns, tdm[0].idPath)
        pathsLifeTime = {}
        # Produces a list of the timestamp_ns when a different path was selected.
        for m in tdm:
            if m.idPath != previous[1] :
                if previous[1] in pathsLifeTime:
                    pathsLifeTime[previous[1]] = pathsLifeTime[previous[1]] + (int(m.timestamp_ns - previous[0])/1000000000)
                elif previous[1] not in pathsLifeTime:
                    pathsLifeTime[previous[1]] = 0
                previous = (m.timestamp_ns, m.idPath)

        legend = "[%s]-[%s]" % (
            dm.ndm.getEndNodeByIp(td.source()).name,
            dm.ndm.getEndNodeByIp(td.destination()).name
            )

        ret_dic[td] = (pathsLifeTime,legend)
    return ret_dic
