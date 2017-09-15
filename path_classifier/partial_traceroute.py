
import time
from dao import *
from itertools import combinations


class PairedMeasurementsContainer(object): # PMC/pmc for short
    def __init__(self, path_pair_ids,
        frwd_msrmnts_tspairs, rvrs_msrmnts_tspairs):
        self.path_pair_ids = path_pair_ids

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
                frwd_msrmnts_tspairs=[], rvrs_msrmnts_tspairs=[]
                )
            tpm[pp_ids].frwd_msrmnts_tspairs.append( (pmt[1], pmt[2]) )
        if pp_ids in tpm:
            if tpm[pp_ids].frwd_msrmnts_tspairs[0][0] > pmt[1]:
                tpm[pp_ids].frwd_msrmnts_tspairs[0] = (pmt[1], pmt[2])

    for pp_ids, pms_con in tpm.iteritems():
        tdid = dm.pdm.pid2Path[pms_con.path_pair_ids[0]].idTraceDirection
        ret[tdid].append(pms_con)

    return ret



def groupPathPairsByLatencies(pp_dict,tdid,latency_sensitivity_ms):
    measurements = pp_dict[tdid]
    pp_with_minLatency = []
    pp_temp_minLatency = []
    PathPairsMinmumLatencies = []

    for pathpairsContainer in measurements:
        pathPairMin = pathpairsContainer.frwd_msrmnts_tspairs[0][0]  / 1000000
        PathPairsMinmumLatencies.append(pathPairMin)
        pp_temp_minLatency.append((pathpairsContainer.path_pair_ids,pathPairMin))

    smallestMinimumLatency = min(PathPairsMinmumLatencies)
    largestMinimumLatency = max(PathPairsMinmumLatencies)

    latencyRange = largestMinimumLatency - smallestMinimumLatency

    for pathpair in pp_temp_minLatency:
        pp_with_minLatency.append((pathpair[0],pathpair[1] - (pathpair[1] %latency_sensitivity_ms ),pathpair[1]))

    return pp_with_minLatency


def getPathClassesByReversePath(pp_with_minLatency):
    pathClassesByRversePath = {}
    pathGroupedByRvrsAndClass = {}

    reversePathsList = [x[0][1] for x in pp_with_minLatency]
    print reversePathsList
    for rp in reversePathsList:
        matchingFrwdPaths = [x for x in pp_with_minLatency if x[0][1] == rp]
        pathClassesByRversePath[rp] = matchingFrwdPaths

    for rvrsPathID,Paths in pathClassesByRversePath.iteritems():
        values = set(map(lambda x:x[1], Paths))
        pathGroupedByRvrsAndClass[rvrsPathID] = []
        for a in values:
            newlist = [y[0][0] for y in Paths if y[1]==a]
            pathGroupedByRvrsAndClass[rvrsPathID].append((a,newlist))

    return pathGroupedByRvrsAndClass


def getPathHopsPerTD(pdm,tdid):
    paths_hops_list = [(x.id,x.hops) for x in pdm.list if x.idTraceDirection == tdid]
    longestPath = max(paths_hops_list,key=lambda x: len(x[1]))
    lengthOfLongestPath = len(longestPath[1])
    destinationIP = longestPath[1][-1]
    for path in paths_hops_list:
        if len(path[1]) < lengthOfLongestPath:
            for x in xrange(lengthOfLongestPath - len(path[1])):
                path[1].append(destinationIP)

    return paths_hops_list



def getHopsAt(paths_hops_list,ids):
    resultList = []
    for pathid,hops in enumerate(paths_hops_list):
        tempList = []
        for id in ids:
            tempList.append(hops[1][id])
        resultList.append((pathid,tempList))
    return resultList


def isListUnique(resultList):
    checklist = [' -> '.join(x[1]) for x in resultList]
    return (len(checklist) == len(set(checklist)))


def getDefiningHopForTraceDirection(paths_hops_list):
    longestPathLength = len(paths_hops_list[0][1])
    requiredTTLs = []
    continueSearching = True
    hopIndexesList = []
    for a in xrange(1,longestPathLength):
        hopsAtIndex = [x[1][a] for x in paths_hops_list]
        if len(set(hopsAtIndex)) > 1:
            hopIndexesList.append(a)
    testlist = []
    for x in xrange(len(hopIndexesList)):
        for y in combinations(hopIndexesList,x):
            testlist.append(y)
            listOfHops = getHopsAt(paths_hops_list,y)
            if isListUnique(listOfHops):
                continueSearching = False
                requiredTTLs = y
                break
        if not continueSearching:
            break
    return requiredTTLs

t1 = time.time()
pathHops = getPathHopsPerTD(pdm,1)
definingTTLs = getDefiningHopForTraceDirection(pathHops)
print (definingTTLs)
t2 = time.time()

print (t2-t1)
#pps = getPathPairs(dm)
#gpps = groupPathPairsByLatencies(pps,1,3)
#pathPerReverse = getPathClassesByReversePath(gpps)
