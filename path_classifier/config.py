# @Author: Lorenzo Corneo
# @Date:   2016-10-06T09:45:39+02:00
# @Email:  lorenzo.corneo@gmail.com
# @Last modified by:   lorenzocorneo
# @Last modified time: 2016-10-28T15:37:48+02:00



#!/usr/bin/python
import logging
import cluster as cluster_conf

SAMPLE_PERIOD_SEC = 10

db_credentials = {
    'host': '127.0.0.1',
    'db': 'koms_pre_measurements',
    'user': 'newuser',
    'passwd': 'password'
}


KER_API_PROC = 'proc'
KER_API_NETLINK = 'netlink'

# kernel_python_api
kpa = {
    'ktracer' : KER_API_PROC,
    'kfilter' : KER_API_PROC
}



construc = {
    # Timer to delete probes from memory that are older than one minute
    'probes_timeout' : 60000,
}

# path reconstruction (re-assembly)
pasm = {
    # we do not start path reconstruction until sufficient time has pass since
    # the very first probe has been sent """
    'wait4probes_ms' : 2000,

    # Sanity check, all probes in a path, should be within that time from the first probe
    'old_probes_check_ms' : 5000,

    # IF a measurement havent been matched to a pair within this period of time, it
    # is no longer considered for pairing
    'old_measurement_threshold_ms' : 5000,

    # Two traceroutes in opposite directions considered to be a pair only if
    # their delta start time is less than this value
    'path_pair_threshold_ms' : 20,
}


cluster = {
    # Port for internal communication among Path Classifiers User Space processes
    'pc_intra_com_port' : 7007,

    # If Flase, this hardcoded configuration will be used.
    # TODO: read IP list from some common location
    'regenerate' : False,
}
# cluster.py is a custom file per host, not in git
# cluster_conf.cluster = {
#     'public_ips' : [
#         {"ip" : "54.187.44.125", "end_node_name" : "CALI0", "id": -1},
#         {"ip" : "52.57.153.194", "end_node_name" : "FRAN0", "id": -1}
#         ],

#     'our_public_ip' : "52.57.153.194",
#     'our_private_ip' : "172.31.4.169",
#     'our_index' : 0,
# }

for k, v in cluster_conf.cluster.iteritems():
    cluster[k] = v


log_main_loop = {
    "file" : "./logs/main.log",
    "level" : logging.DEBUG,
    "format_prefix": "[MAIN]",
}

log_matcher = {
    "file" : "./logs/matcher.log",
    "level" : logging.DEBUG,
    "format_prefix": "[MACH]",
}

log_intracom = {
    "file" : "./logs/intracom.log",
    "level" : logging.DEBUG,
    "format_prefix": "[ICOM]",
}

log_db = {
    "file" : "./logs/db.log",
    "level" : logging.DEBUG,
    "format_prefix": "[-DB-]",
}

log_path_asm = {
    "file" : "./logs/path_assembly.log",
    "level" : logging.DEBUG,
    "format_prefix": "[PASM]",
}

log_collectors = {
    "file" : "./logs/collectors.log",
    "level" : logging.DEBUG,
    "format_prefix": "[COLL]",
}

log_patch_with_duplicates = {
    "file" : "./logs/duplicates.log",
    "level" : logging.DEBUG,
    "format_prefix": "[DUPL]",
}

log_general = {
    "file" : "./logs/general.log",
    "level" : logging.DEBUG,
    "format_prefix": "[GENERAL]",
}

def get_logger(log_name, log_conf):

    l = logging.getLogger(log_name)
    l.setLevel(log_conf["level"])

    fh = logging.FileHandler(log_conf["file"])
    fh.setLevel(log_conf["level"])
    # frmt = log_conf["format_prefix"] + \
    #     "(%(funcName).5s):[%(lineno)4d] %(asctime)s %(levelname)7s| %(message)s"
    frmt = log_conf["format_prefix"] + " %(message)s"
    fh.setFormatter(logging.Formatter(frmt, datefmt='%m.%d_%H:%M:%S'))
    l.addHandler(fh)

    return l
