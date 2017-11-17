#!/usr/bin/python

import time
from dao import *
from itertools import combinations
import sys

hopsToPathsDictionary = {}

currentReversePathsDict = {}

pathPairsLatencyDict = {}

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


def findFinalLatencyClassesList(pathGroupedByRvrsAndClass):
    resultList = []
    listOfFragmentedPathClasses = []
    for rvrsPathID,PathClasses in pathGroupedByRvrsAndClass.iteritems():
        values = [x[1] for x in PathClasses]
        for a in values:
            listOfFragmentedPathClasses.append(a)

    print listOfFragmentedPathClasses

    tempList = listOfFragmentedPathClasses
    tempList2 = []
    checkCondition = True
    while checkCondition:
        while len(tempList) > 0:
            listOfItemsToRemove = [0]
            firstItem = tempList[0]
            for index1 in xrange(1,len(tempList)):
                if bool(set(firstItem) & set(tempList[index1])):
                    firstItem = list(set(firstItem) | set(tempList[index1]))
                    listOfItemsToRemove.append(index1)

            tempList2.append(firstItem)

            for a in sorted(listOfItemsToRemove, reverse=True):
                del tempList[a]

        checkCondition = False
        tempList = tempList2

        for a in xrange(len(tempList)):
            for b in xrange(a+1,len(tempList)):
                if set(tempList[a]) & set(tempList[b]):
                    tempList2 = []
                    checkCondition = True

    print tempList2
    return tempList2



def subtractLists(list1,list2):
    res1 = [item for item in list1 if item not in list2]
    res2 = [item for item in list2 if item in list1]
    return (res1,res2)

def subtractListofLists(list1,list2):
    result_list = []
    for a in list1:
        tempList = []
        for b in list2:
            if len(tempList) == 0:
                tempList = a
            res_tuple = subtractLists(tempList,b)
            if len(res_tuple[1]) != 0:
                result_list.append(res_tuple[1])
                if len(res_tuple[0]) != 0:
                    tempList = res_tuple[0]
                else:
                    break
    return result_list

def areTwoListsEqual(list1,list2):
    result = True
    for a in list1:
        result = False
        for b in list2:
            if set(a).issubset(b):
                result = True
                break
        if not result:
            break
    return result



#def areTwoListsEqual_backup(list1,list2):
#    result = True
#    for a in list1:
#        result = False
#        for b in list2:
#            if set(a) == set(b):
#                result = True
#                break
#        if not result:
#            break
#    return result

def getPathHopsForListOfPaths(pdm,listOfPaths):

    paths_hops_list = [(x.id,x.hops) for x in pdm.list if x.id in listOfPaths]
    longestPath = max(paths_hops_list,key=lambda x: len(x[1]))
    lengthOfLongestPath = len(longestPath[1])
    print "Longest Path has length of ",lengthOfLongestPath
    print longestPath
    destinationIP = longestPath[1][-1]
    for path in paths_hops_list:
        if len(path[1]) < lengthOfLongestPath:
            for x in xrange(lengthOfLongestPath - len(path[1])):
                path[1].append(destinationIP)

    return paths_hops_list

def getGroupedPathsPerHop(pathHops):
    listOfGroupedPathsPerHop = []
    lengthOfLongestPath = len(pathHops[0][1])
    for item in xrange(1,lengthOfLongestPath):

        itemAtIndex = [(a[0],a[1][item]) for a in pathHops]
        values = set(map(lambda x:x[1], itemAtIndex))
        newlist = [[y[0] for y in itemAtIndex if y[1]==x] for x in values]

        listOfGroupedPathsPerHop.append(newlist)
    return listOfGroupedPathsPerHop


def combineHopsLists(Lists,ttlValues):
    prevList = Lists[ttlValues[0]]
    for index,ttl in enumerate(ttlValues):
        if index == 0:
            continue
        prevList = subtractListofLists(prevList,Lists[ttlValues[index]])

    return prevList


def getUniqueHops(groupedPathsPerHop,desiredOutput):
    longestPathLength = len(groupedPathsPerHop)

    ttlsFound = False
    outputHops = []
    hopsWithUniquePaths = []
    for hopid,pathGroups in enumerate(groupedPathsPerHop):
        if len(pathGroups) > 1:
            hopsWithUniquePaths.append(hopid)


    for a in xrange(1,len(hopsWithUniquePaths)+1):
        for b in combinations(hopsWithUniquePaths,a):
            res = combineHopsLists(groupedPathsPerHop,b)
            if areTwoListsEqual(res,desiredOutput):
                outputHops = b
                ttlsFound = True
                break
        if ttlsFound:
            break

    outputHops = [d+1 for d in outputHops]
    print 'outputHops',outputHops
    return outputHops

def populateQueryDictionary(uniqueHops,desiredList,pathHops,destinationIP):
    hopsToPathsDictionary[destinationIP] = {}
    for path in pathHops:
        if path[0] in desiredList:
            hopIPs = []
            for a in uniqueHops:
                hopIPs.append(path[1][a])
            searchString = '-'.join(hopIPs)
            if searchString not in hopsToPathsDictionary[destinationIP]:
                hopsToPathsDictionary[destinationIP][searchString] = []
                hopsToPathsDictionary[destinationIP][searchString].append(path[0])
            else:
                hopsToPathsDictionary[destinationIP][searchString].append(path[0])



def getCurrentForwdPaths(searchString,destinationIP):
    try:
        return hopsToPathsDictionary[destinationIP][searchString]
    except:
        return None

def getEstimatedLatency(frwdPathsList,rvrsPathsList,destinationIP):
    for frwdPath in frwdPathsList:
        for rvrsPath in rvrsPathsList:
            tempList = [x for x in pathPairsLatencyDict[destinationIP] if x[0] == (frwdPath,rvrsPath)]
            if tempList:
                return tempList[0][2]
    return 0


def getHopsTTL_ToQuery(sourceIP,destinationIP,latency_sensitivity_ms):
    traceDirection = pdm.getTraceDirectionByIps(sourceIP,destinationIP)
    allPathPairs = getPathPairs(dm)


    pathPairsLatencyDict[destinationIP] =  groupPathPairsByLatencies(allPathPairs,traceDirection,latency_sensitivity_ms)

    pathClassesPerRvrsPath = getPathClassesByReversePath(pathPairsLatencyDict[destinationIP])

    desiredList = findFinalLatencyClassesList(pathClassesPerRvrsPath)

    print "Desired List", desiredList

    # This removes any forward path that we don't know the reverse path for it. We hope there does not exist many
    listOfConsideredPaths = [a for b in desiredList for a in b]

    print "considered paths only:", listOfConsideredPaths
    pathHops = getPathHopsForListOfPaths(pdm,listOfConsideredPaths)

    print pathHops
    numberOfPaths = len(pathHops)
    groupedPathsPerHop = getGroupedPathsPerHop(pathHops)

    uniqueHops = getUniqueHops(groupedPathsPerHop,desiredList)
    print "Unique hops at ",uniqueHops

    for a in uniqueHops:
        print groupedPathsPerHop[a]

    populateQueryDictionary(uniqueHops,listOfConsideredPaths,pathHops,destinationIP)

    print uniqueHops
    return uniqueHops
