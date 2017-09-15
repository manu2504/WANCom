#!/usr/bin/python

import itertools

from models.EndNode import EndNode
from models.Path import Path
from models.Measurement import Measurement

import config as conf
import dao as dao

log = conf.get_logger("db", conf.log_db)

rdm = dao.rdm
dm = dao.dm
hdm = dao.hdm
# for p in dm.pdm.list:
#     print "EP: ", p.str_short(), p.id

def init_db_end_nodes():
    # Checks that configured end nodes are in database,
    # if not, new entries are being added
    # if an entry with the same name but different ip exists, its ip is overwritten

    db_nodes = dm.ndm.getAll()

    for cfg_node in conf.cluster["public_ips"]:

        found_db_node = [n for n in db_nodes if n.name == cfg_node["end_node_name"]]

        if len(found_db_node) == 0:
            # An end node with designated name does not exist, add it and commit
            #log.warning("[DB] EndNode [%s] does not exists, adding!", cfg_node)
            # TODO: commit to db

            end_node = EndNode(ip=cfg_node["ip"], name=cfg_node["end_node_name"])
            dm.ndm.add(end_node)

            print "Result", dm.ndm.getAll()

        elif len(found_db_node) == 1:

            if found_db_node[0].ip != cfg_node["ip"]:
                log.warning("[DB] overwriting IP for EndNode [%s] to [%s]",
                    found_db_node[0], cfg_node["ip"])

                end_node = EndNode(ip=cfg_node["ip"], name=cfg_node["end_node_name"], id=found_db_node[0].id)
                dm.ndm.update(end_node)

            else:
                print found_db_node[0]
                cfg_node["id"] = (int)(found_db_node[0].id)
        else:
            assert False # node names should be unique


def init_db_trace_directions():
    """ This function checks that TraceDirections in database correspond to the EndNodes
    in the configuration. Note, EndNodes in configuration is a subset of EndNodes in DB"""

    # TODO: potentially rewrite according to new dao API
    # for db_nodes in conf.cluster["public_ips"]:
    #node_ids = [x["id"] for x in conf.cluster["public_ips"]]
    # Khalid Update: replace the above expression with new one
    node_ids = [x.id for x in dm.ndm.getAll() ]

    required_td_pairs = \
        [p for p in [x for x in itertools.product(node_ids, node_ids) ] if p[0] != p[1]]

    print required_td_pairs
    existing = [ (x[1],x[2]) for x in rdm.getTraceDirections()]
    print existing

    for r in required_td_pairs:
        if r not in existing:

            td_id = rdm.insertTraceDirection(r[0], r[1])
            # rdm.insertPath(td_id, [ r[0], r[1] ] )



    # for src_node_id, dst_node_id in required_td_pairs:


    #     print "PAIR", src_node_id, dst_node_id
    #     td = dm.getTraceDirectionByIps(
    #         dm.getEndNodeById(src_node_id)["ip"],
    #         dm.getEndNodeById(dst_node_id)["ip"])

    #     if not td:
    #         log.warning("[DB] Insertin TraceDirection [%s->%s]",
    #             src_node_id, dst_node_id)
    #         rdm.insertTraceDirection(src_node_id, dst_node_id)

    # # TODO: remove when we going to update run time state
    # dm._initTraceDirections()

def inti_db():
    init_db_end_nodes()
    init_db_trace_directions()
    #log.info("DB, Nodes and Directions are set!")


def test(tmp_path):
    log.debug("Orig: [%s][%s]", tmp_path.str_short(), tmp_path.__hash__())
    for i, pp in enumerate(dm.pdm.list):
        log.debug("Exis: [%s][%s]", pp.str_short(), pp.__hash__())


def assimilate_paths(new_nps_dic, commit2db):
    ret_measurements = {}

    for dst_ip, path_list in new_nps_dic.iteritems():
        for in_path in path_list:

            tmp_path = Path(hops=in_path.hops, id=in_path.pid)

            p = dm.pdm.pathExists(tmp_path)
            if not p:

                #test(tmp_path)

                if commit2db == True:
                    p = dm.pdm.add(tmp_path)
                else:
                    p = dm.pdm.addToMemory(tmp_path)

                #log.debug("Cmting new Path [%s][%s][pid: %i][cm_flag: %s]",
                #    p.str_short(), p.__hash__(), p.id, commit2db)
            else:

                if commit2db == False:
                    # If a path already exists in RAM (thus we dont commit to DB)
                    # Make sure that pids of what we have and what we add are the same
                    assert p.id == in_path.pid

                #log.debug("Existing   Path [%s][pid: %i][cm_flag: %s][msrmnts: %i]",
                #    tmp_path.str_short(), p.id, commit2db, len(p.measurements))

            # Set the correct pid for the incoming path, if this is the new path and
            # we to send it to the other instances, NPC should contain the correct pid
            in_path.pid = p.id

            m = Measurement(rtt_ns=in_path.rtt_ns, timestamp_ns=in_path.trace_start_time_ns,
                owd_forward_ns=in_path.owd_forward_ns, owd_reverse_ns=in_path.owd_reverse_ns,
                idPath=p.id)

            # Preserve measurements, but commit them later
            #p.addMeasurement(m)
            if dst_ip in ret_measurements:
                ret_measurements[dst_ip].append(m)
            else:
                ret_measurements[dst_ip] = [m]

    return ret_measurements




batch_commit_counter = itertools.count()
def batchcommit_measurements(measurements):
    iteration = next(batch_commit_counter)
    if iteration % 5 == 0:
        log.debug("Batch Cm Msrmns [iter: %i][msrmnts: %i]",
            iteration, len(measurements))
        dm.mdm.addMany(measurements[0])
        hdm.addMany(measurements[1])
        del measurements[0][:]
        del measurements[1][:]
